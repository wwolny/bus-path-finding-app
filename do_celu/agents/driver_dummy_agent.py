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
from spade.message import Message


class DummyAgent(agent.Agent):
    my_behaviour: 'MyBehaviour'

    class MyBehaviour(CyclicBehaviour):
        iterator = 0

        async def run(self):
            msg = Message(to='driver@localhost')
            msg.set_metadata("performative", 'inform')  # Set the "inform" FIPA performative
            msg.set_metadata("ontology", 'DoCeluMainOntology')  # Set the ontology of the message content
            msg.set_metadata("language", "JSON")  # Set the language of the message content
            msg.set_metadata("selector", "path_change")
            msg.body = json.dumps({'iterator': self.iterator, 'path': 'new_path'})
            try:
                await self.send(msg)
                print(f'Message send! Iteration {self.iterator}')
            except Exception:
                return
            if self.iterator > 1 and self.iterator % 5 == 0:
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(2)
            self.iterator += 1

        async def on_end(self) -> None:
            await self.agent.stop()
            print(f'Behaviour finished with exit code {self.exit_code}.')

    async def setup(self):
        print('Agent starting...')
        self.my_behaviour = self.MyBehaviour()
        self.add_behaviour(self.my_behaviour)


if __name__ == '__main__':
    dummy = DummyAgent("manager@localhost", "manager_password")
    future = dummy.start()
    future.result()

    print('Wait until user interrupts with ctrl+c')
    while dummy.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    dummy.stop()
    quit_spade()
