#
# do_celu
#
# Copyright 2022 Agenty 007
#
import asyncio
import json
import time

from spade import agent, quit_spade
from spade.behaviour import CyclicBehaviour

from do_celu.messages.driver import DriverDataMessage, PathChangeMessage


class DummyAgent(agent.Agent):
    path_change: 'PathChange'
    driver_data: 'DriverData'

    class PathChange(CyclicBehaviour):
        iterator = 0

        async def run(self):
            msg = PathChangeMessage(to='driver@localhost')
            msg.body = json.dumps({'iterator': self.iterator, 'path': 'new_path'})
            try:
                await self.send(msg)
                print(f'Message PathChange send! Iteration {self.iterator}')
            except Exception:
                return
            if self.iterator > 1 and self.iterator % 5 == 0:
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(1)
            self.iterator += 1

        async def on_end(self) -> None:
            await self.agent.stop()
            print(f'Behaviour finished with exit code {self.exit_code}.')

    class DriverData(CyclicBehaviour):
        iterator = 0

        async def run(self):
            msg = DriverDataMessage(to='driver@localhost')
            msg.body = json.dumps({
                'iterator': self.iterator,
            })
            try:
                await self.send(msg)
                print(f'Message DriverData send! Iteration {self.iterator}')
            except Exception:
                return
            if self.iterator > 1 and self.iterator % 5 == 0:
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(2)
            self.iterator += 1

        async def on_end(self) -> None:
            await self.agent.stop()
            print(f'Behaviour finished with exit code {self.exit_code}.')

    async def setup(self):
        print('Agent starting...')


if __name__ == '__main__':
    dummy = DummyAgent("manager@localhost", "manager_password")
    future = dummy.start()
    dummy.path_change = dummy.PathChange()
    dummy.driver_data = dummy.DriverData()
    dummy.add_behaviour(dummy.path_change)
    dummy.add_behaviour(dummy.driver_data)
    future.result()

    print('Wait until user interrupts with ctrl+c')
    while dummy.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    dummy.stop()
    quit_spade()
