#
# do_celu
#
# Copyright 2022 Agenty 007
#

from time import sleep
from logging import Logger
from spade import agent, quit_spade
from spade.message import Message
from do_celu.utils.performatives import Performatives
from do_celu.behaviours import BaseOneShotBehaviour
from do_celu.config import Config, get_config
from do_celu.context import get_logger
from do_celu.utils.job_exit_code import JobExitCode

LOGGER_NAME = get_config().MANAGER_LOGGER_NAME


class ManagerAgent(agent.Agent):
    # Behaviours:
    receive_welcome_driver_msg: 'ReceiveWelcomeDriverMsg'
    receive_available_drivers_request: 'ReceiveAvailableDriversRequest'
    request_driver_data: 'RequestDriverData'
    receive_driver_data: 'ReceiveDriverData'
    request_best_paths: 'RequestBestPaths'
    receive_best_paths: 'ReceiveBestPaths'
    inform_client_best_paths: 'InformClientBestPaths'
    cfp_client_choose_path: 'CFPClientChoosePath'
    receive_client_path_proposal: 'ReceiveClientPathProposal'
    inform_driver_path_change: 'InformDriverPathChange'
    accept_client_path_proposal: 'AcceptClientPathProposal'
    # Agent state:

    _logger: Logger
    _config: Config

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security=verify_security)
        self._config = get_config()
        self._logger = get_logger(LOGGER_NAME)

    class ReceiveWelcomeDriverMsg(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Receiving welcome driver msg...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving welcome driver msg successful - Body: {}".format(msg.body))
                # TODO add to driver list (contacts)
            else:
                print("Receiving welcome driver msg failed after 30 seconds")

    class ReceiveAvailableDriversRequest(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Receiving available drivers request...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving available drivers request successful - Body: {}".format(msg.body))
                # TODO trigger getting driver data (find all available drivers and RequestDriverData)
            else:
                print("Receiving available drivers request failed after 30 seconds")

    class RequestDriverData(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        def __init__(self,):
            super().__init__(LOGGER_NAME)

        async def on_start(self):
            self._logger.debug('RequestDriverData running...')

        async def run(self):
            msg = Message(to='driver@localhost')  # TODO send to all available drivers
            msg.set_metadata('performative', Performatives.REQUEST)
            # msg.body = #TODO
            await self.send(msg)

        async def on_end(self):
            self.exit_code = JobExitCode.SUCCESS
            self._logger.debug(f'RequestDriverData ended with status: {self.exit_code.name}')

    class ReceiveDriverData(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Receiving driver data...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving driver data successful - Body: {}".format(msg.body))
                # TODO trigger getting best paths (maybe after x seconds after first respond)
                # - prob move to other behavior
            else:
                print("Receiving driver data failed after 30 seconds")

    class RequestBestPaths(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Requesting best paths...')
            msg = Message(to=Config.MATHEMATICIAN_JID)
            msg.set_metadata('performative', Performatives.REQUEST)
            # msg.body = #TODO
            await self.send(msg)
            print('Requesting best paths successful')

    class ReceiveBestPaths(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Receiving best paths...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving best paths successful - Body: {}".format(msg.body))
                # TODO send to client
            else:
                print("Receiving best paths failed after 30 seconds")

    class InformClientBestPaths(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Informing client about best paths...')
            msg = Message(to='client@localhost')  # TODO select good client
            msg.set_metadata('performative', Performatives.INFORM)
            # msg.body = #TODO
            await self.send(msg)
            print('Informing client about best paths successful')

    class CFPClientChoosePath(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Call for proposal client choosing path...')
            msg = Message(to='client@localhost')  # TODO select good client
            msg.set_metadata('performative', Performatives.CALL_FOR_PROPOSAL)
            # msg.body = #TODO
            await self.send(msg)
            print('Call for proposal client choosing path successful')

    class ReceiveClientPathProposal(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Receiving client path proposal...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving client path proposal successful - Body: {}".format(msg.body))
                # TODO send info to driver
                # TODO after that accept proposal
            else:
                print("Receiving client path proposal failed after 30 seconds")

    class InformDriverPathChange(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Informing driver about path change...')
            msg = Message(to='driver@localhost')  # TODO select good driver
            msg.set_metadata('performative', Performatives.INFORM)
            # msg.body = #TODO
            await self.send(msg)
            print('Informing driver about path change successful')

    class AcceptClientPathProposal(BaseOneShotBehaviour):
        agent: 'ManagerAgent'

        async def run(self):
            print('Accepting client path proposal...')
            msg = Message(to='client@localhost')  # TODO select good client
            msg.set_metadata('performative', Performatives.ACCEPT_PROPOSAL)
            # msg.body = #TODO
            await self.send(msg)
            print('Accepting client path proposal successful')

    async def setup(self):
        self._logger.info('ManagerAgent started')
        self.add_behaviour((self.RequestDriverData())) #TODO temp remove


if __name__ == '__main__':
    config = get_config()
    logger = get_logger(config.MANAGER_LOGGER_NAME)
    manager = ManagerAgent(
        config.MANAGER_JID,
        config.MANAGER_PASSWORD,
    )

    future = manager.start()
    future.result()

    while manager.is_alive():
        try:
            sleep(1)
        except KeyboardInterrupt:
            break

    manager.stop()
    logger.debug('Manager agent stopped')
    quit_spade()
