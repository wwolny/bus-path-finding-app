#
# do_celu
#
# Copyright 2022 Agenty 007
#

from spade import agent, quit_spade


class DummyAgent(agent.Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))


dummy = DummyAgent("client@localhost", "client_password")
future = dummy.start()
future.result()

dummy.stop()
quit_spade()
