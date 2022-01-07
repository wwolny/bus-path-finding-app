#
# do_celu
#
# Copyright 2022 Agenty 007
#

from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class ManagerAgent(agent.Agent):
    class ReceiveAvailableDriversRequest(OneShotBehaviour):
        async def run(self):
            print('Receiving available drivers request...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving available drivers request successful - Body: {}".format(msg.body))
                # TODO trigger getting driver data
            else:
                print("Receiving available drivers request failed after 30 seconds")

    class RequestDriverData(OneShotBehaviour):
        async def run(self):
            print('Requesting driver data...')
            msg = Message(to='driver@localhost') #TODO send to all available drivers
            msg.set_metadata('performative', 'request')
            # msg.body = #TODO
            await self.send(msg)
            print('Requesting driver data successful')

    class ReceiveDriverData(OneShotBehaviour):
        async def run(self):
            print('Receiving driver data...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving driver data successful - Body: {}".format(msg.body))
                # TODO trigger getting best paths (maybe after x seconds after first respond) - prob move to other behavior
            else:
                print("Receiving driver data failed after 30 seconds")

    class RequestBestPaths(OneShotBehaviour):
        async def run(self):
            print('Requesting best paths...')
            msg = Message(to='mathematician@localhost')
            msg.set_metadata('performative', 'request')
            # msg.body = #TODO
            await self.send(msg)
            print('Requesting best paths successful')

    class ReceiveBestPaths(OneShotBehaviour):
        async def run(self):
            print('Receiving best paths...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving best paths successful - Body: {}".format(msg.body))
                #TODO send to client
            else:
                print("Receiving best paths failed after 30 seconds")

    class InformClientBestPaths(OneShotBehaviour):
        async def run(self):
            print('Informing client about best paths...')
            msg = Message(to='client@localhost') #TODO select good client
            msg.set_metadata('performative', 'inform')
            # msg.body = #TODO
            await self.send(msg)
            print('Informing client about best paths successful')

    class CFPClientChoosePath(OneShotBehaviour):
        async def run(self):
            print('Call for proposal client choosing path...')
            msg = Message(to='client@localhost') #TODO select good client
            msg.set_metadata('performative', 'call_for_proposal') #TODO check performative
            # msg.body = #TODO
            await self.send(msg)
            print('Call for proposal client choosing path successful')

    class ReceiveClientPathProposal(OneShotBehaviour):
        async def run(self):
            print('Receiving client path proposal...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving client path proposal successful - Body: {}".format(msg.body))
                #TODO send info to driver
                #TODO after that accept proposal
            else:
                print("Receiving client path proposal failed after 30 seconds")

    class InformDriverPathChange(OneShotBehaviour):
        async def run(self):
            print('Informing driver about path change...')
            msg = Message(to='driver@localhost') #TODO select good driver
            msg.set_metadata('performative', 'inform')
            # msg.body = #TODO
            await self.send(msg)
            print('Informing driver about path change successful')

    class AcceptClientPathProposal(OneShotBehaviour):
        async def run(self):
            print('Accepting client path proposal...')
            msg = Message(to='client@localhost') #TODO select good client
            msg.set_metadata('performative', 'accept_proposal') #TODO check performative
            # msg.body = #TODO
            await self.send(msg)
            print('Accepting client path proposal successful')

    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))
