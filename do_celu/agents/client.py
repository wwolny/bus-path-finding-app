#
# do_celu
#
# Copyright 2022 Agenty 007
#
from datetime import datetime

from typing import Optional
from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from do_celu.entities.connection import ConnectionRequest, ConnectionResponse, Connection


class ClientAgent(agent.Agent):
    def __init__(self, start_date: datetime, origin, destination, jid: str, password: str):
        super().__init__(jid, password)
        self.start_date = start_date
        self.origin = origin
        self.destination = destination
        self.best_connections: Optional[ConnectionResponse] = None
        self.chosen_connection: Optional[Connection] = None
        self.reservation_available = False
        self.connection_accepted = False

    class RequestAvailableConnections(OneShotBehaviour):
        async def run(self):
            print("Request available connections")
            msg = Message(to="receiver@your_xmpp_server")
            msg.set_metadata("performative", "request")
            msg.body = ConnectionRequest(self.agent.start_date, self.agent.origin, self.agent.destination)

            await self.send(msg)
            print("Message sent!")

    # there is no sense that it will be CyclicBehaviour, because of one-time information about available connections
    class ReceiveInformBestConnections(OneShotBehaviour):
        async def run(self):
            print("Waiting for the best connections")
            msg = await self.receive(timeout=30)
            if msg:
                print("Message received with content: {}".format(msg.body))
                self.agent.best_connections = msg.body
            else:
                print("Did not received any message after 30 seconds")

    class ReceiveAvailabilityForReservation(OneShotBehaviour):
        async def run(self):
            print("Waiting for availability for reservation")
            msg = await self.receive(timeout=30)
            if msg:
                print("Message received with content: {}".format(msg.body))
                self.agent.reservation_available = True
            else:
                print("Did not received any message after 30 seconds")

    class ProposeChosenConnection(OneShotBehaviour):
        async def run(self):
            print("Propose chosen connection")
            msg = Message(to="receiver@your_xmpp_server")
            msg.set_metadata("performative", "propose")
            # todo: set chosen connection
            msg.body = self.agent.chosen_connection

            await self.send(msg)
            print("Message sent!")

    class ReceiveAcceptProposalClientPath(OneShotBehaviour):
        async def run(self):
            print("Waiting for ACK chosen connection")
            msg = await self.receive(timeout=30)
            if msg:
                print("Message received with content: {}".format(msg.body))
                self.agent.connection_accepted = True
            else:
                print("Did not received any message after 30 seconds")

    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))
        my_behav = self.RequestAvailableConnections()
        self.add_behaviour(my_behav)

