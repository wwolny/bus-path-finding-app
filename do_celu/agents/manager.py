#
# do_celu
#
# Copyright 2022 Agenty 007
#

from spade import agent
from spade.behaviour import CyclicBehaviour


class ManagerAgent(agent.Agent):
    class RequestDriverData(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class RequestBestPath(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class InformBestPath(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class InformPathChange(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class AcceptProposalClientPath(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class InformExtraCharge(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class SubscribeDriver(CyclicBehaviour):
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
