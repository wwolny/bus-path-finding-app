#
# do_celu
#
# Copyright 2022 Agenty 007
#

from spade import agent
from spade.behaviour import CyclicBehaviour


class ClientAgent(agent.Agent):
    class RequestAvailableConections(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class ProposeChoosenConection(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class RecvInformBestPath(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class Recv(CyclicBehaviour):
        async def on_start(self):
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class RecvAcceptProposalClientPath(CyclicBehaviour):
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
