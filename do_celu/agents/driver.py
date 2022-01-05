#
# do_celu
#
# Copyright 2022 Agenty 007
#

from spade import agent
from spade.behaviour import CyclicBehaviour


class DriverAgent(agent.Agent):
    class InformDriverData(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class RecvRequestDriverData(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class RecvInformPathChange(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))
        self.my_behav = self.MyBehav()
        self.add_behaviour(self.my_behav)
