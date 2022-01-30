#
# do_celu
#
# Copyright 2022 Agenty 007
#

import json
from logging import Logger
from time import sleep
from typing import List, Tuple

from spade import agent, quit_spade

from do_celu.behaviours import BaseOneShotBehaviour, BaseCyclicBehaviour
from do_celu.messages.manager import ReceiveBestRoutesMessage, ReceiveBestPathsBody
from do_celu.messages.mathematic import RequestBestPathsBody, RequestBestPathsTemplate
from do_celu.utils.dataclass_json_encoder import DataclassJSONEncoder
from do_celu.utils.job_exit_code import JobExitCode
from do_celu.config import Config, get_config
from do_celu.context import get_logger

graph = [[0, 4, 20, 16, 14, 17, 3, 8, 19, 19], [4, 0, 6, 11, 20, 1, 13, 10, 8, 3], [20, 6, 0, 1, 1, 7, 5, 19, 13, 19],
         [16, 11, 1, 0, 10, 15, 4, 2, 10, 6], [14, 20, 1, 10, 0, 3, 8, 7, 8, 5], [17, 1, 7, 15, 3, 0, 3, 15, 7, 12],
         [3, 13, 5, 4, 8, 3, 0, 15, 12, 6], [8, 10, 19, 2, 7, 15, 15, 0, 15, 11], [19, 8, 13, 10, 8, 7, 12, 15, 0, 9],
         [19, 3, 19, 6, 5, 12, 6, 11, 9, 0]]

LOGGER_NAME = get_config().MATHEMATICIAN_LOGGER_NAME


class MathematicianAgent(agent.Agent):
    # Behaviours:
    receive_best_paths: 'ReceiveRequestBestPaths'
    receive_best_paths_template: RequestBestPathsTemplate
    inform_best_paths: 'InformBestPaths'

    # Agent state:
    _logger: Logger
    _config: Config

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security=verify_security)
        self._config = get_config()
        self._logger = get_logger(LOGGER_NAME)

    class ReceiveRequestBestPaths(BaseCyclicBehaviour):
        agent: 'MathematicianAgent'

        def __init__(self,):
            super().__init__(LOGGER_NAME)

        async def on_start(self):
            self._logger.debug('ReceiveRequestBestPath running...')

        async def run(self):
            msg = await self.receive()
            if msg:
                self._logger.debug(f'ReceiveRequestBestPath msg received with body: {msg.body}')
                sender = str(msg.sender).split('/')[0]
                body = json.loads(msg.body)
                data = RequestBestPathsBody(**body)
                self._logger.debug(f'Sender: {sender} - Driver data: {vars(data)}')
                self.agent._add_inform_best_paths(sender=sender, request=data)
                self.exit_code = JobExitCode.SUCCESS

        async def on_end(self):
            self._logger.debug(f'ReceiveRequestBestPath ended with status: {self.exit_code.name}')

    class InformBestPaths(BaseOneShotBehaviour):
        agent: 'MathematicianAgent'
        _bus_routes: List[List[int]]
        _new_rides: List[Tuple[int, int]]
        _receiver_jid: str

        def __init__(self, receiver_jid: str, bus_routes: List[List[int]], new_rides: List[Tuple[int, int]]):
            super().__init__(LOGGER_NAME)
            self._bus_routes = bus_routes
            self._new_rides = new_rides
            self._receiver_jid = receiver_jid

        async def on_start(self):
            self._logger.debug('InformBestPath running...')

        def tsp(self, needed: List[Tuple[int, int]], busroutes: List[List[int]]):
            nbuses = len(busroutes)
            for i in range(len(needed)):
                temp = 0
                mincost = 9999
                for j in range(nbuses):
                    currcost = 0
                    busroute = busroutes[j]
                    if len(busroutes[j]) == 1:
                        temp = j
                        break
                    else:
                        temp2 = needed[i]
                        for k in range(len(busroutes[j]) - 1):
                            currcost += graph[busroute[k]][busroute[k + 1]]
                        if temp2[0] == busroute[len(busroute) - 1]:
                            currcost = currcost + graph[busroute[len(busroute) - 1]][needed[i][1]]
                        else:
                            currcost = currcost + graph[busroute[len(busroute) -
                                                                 1]][needed[i][0]] + graph[needed[i][0]][needed[i][1]]
                        if currcost < mincost:
                            mincost = currcost
                            temp = j

                busroute = busroutes[temp]
                temp2 = needed[i]
                if busroute[len(busroute) - 1] != temp2[0]:
                    busroute.append(0)
                    busroute[len(busroute) - 1] = temp2[0]
                busroute.append(0)
                busroute[len(busroute) - 1] = temp2[1]
                busroutes.pop(temp)
                busroutes.insert(temp, busroute)
            return busroutes

        async def run(self):
            self._logger.debug("Calculating the best route.")

            busroutes = self.tsp(needed=self._new_rides, busroutes=self._bus_routes)
            msg = ReceiveBestRoutesMessage(to=self._receiver_jid)
            msg.body = json.dumps(ReceiveBestPathsBody(best_paths=busroutes), cls=DataclassJSONEncoder)
            try:
                await self.send(msg)
                self._logger.debug("Sending the best routes! - Best Routes: {0}".format(busroutes))
            except Exception as e:
                self._logger.error(e)
                self.kill(JobExitCode.FAILURE)
                return

        async def on_end(self):
            self._logger.debug('InformBestPath ended')

    async def setup(self):
        self._logger.info('MathematicianAgent started')
        self._add_receive_best_paths()

    def _add_receive_best_paths(self):
        self.receive_best_paths = self.ReceiveRequestBestPaths()
        self.receive_best_paths_template = RequestBestPathsTemplate()
        self.add_behaviour(self.receive_best_paths, self.receive_best_paths_template)

    def _add_inform_best_paths(self, sender: str, request: RequestBestPathsBody):
        self.inform_best_paths = self.InformBestPaths(receiver_jid=sender,
                                                      bus_routes=request.bus_routes,
                                                      new_rides=request.new_rides)
        self.add_behaviour(self.inform_best_paths)


if __name__ == '__main__':
    config = get_config()
    logger = get_logger(config.MATHEMATICIAN_LOGGER_NAME)
    mathematician = MathematicianAgent(
        config.MATHEMATICIAN_JID,
        config.MATHEMATICIAN_PASSWORD,
    )

    future = mathematician.start()
    future.result()

    while mathematician.is_alive():
        try:
            sleep(1)
        except KeyboardInterrupt:
            break

    mathematician.stop()
    logger.debug('Mathematician agent stopped')
    quit_spade()
