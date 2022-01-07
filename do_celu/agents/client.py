#
# do_celu
#
# Copyright 2022 Agenty 007
#
from datetime import datetime

from typing import Optional
from spade import agent
from do_celu.behaviours import BaseOneShotBehaviour
from do_celu.utils.performatives import Performatives
from do_celu.config import Config
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

    class RequestAvailableConnections(BaseOneShotBehaviour):
        async def run(self):
            print("Request available connections")
            msg = Message(to=Config.MANAGER_JID)
            msg.set_metadata("performative", Performatives.REQUEST)
            msg.body = ConnectionRequest(self.agent.start_date, self.agent.origin, self.agent.destination)

            await self.send(msg)
            print("Request for available connections sent!")
            self.kill()

    # there is no sense that it will be CyclicBehaviour, because of one-time information about available connections
    class ReceiveInformBestConnections(BaseOneShotBehaviour):
        async def run(self):
            await self.agent.req_available_connections_behav.join()

            print("Waiting for the best connections")
            msg = await self.receive(timeout=30)
            if msg:
                print("Message received with content: {}".format(msg.body))
                self.agent.best_connections = msg.body
            else:
                print("Did not received any message after 30 seconds")

            self.kill()

    class ReceiveAvailabilityForReservation(BaseOneShotBehaviour):
        async def run(self):
            await self.agent.req_available_connections_behav.join()

            print("Waiting for availability for reservation")
            msg = await self.receive(timeout=30)
            if msg:
                print("Message received with content: {}".format(msg.body))
                self.agent.reservation_available = True
            else:
                print("Did not received any message after 30 seconds")

            self.kill()

    class ProposeChosenConnection(BaseOneShotBehaviour):
        async def run(self):
            print("Propose chosen connection")
            msg = Message(to=Config.MANAGER_JID)
            msg.set_metadata("performative", Performatives.PROPOSE)
            msg.body = self.agent.chosen_connection

            await self.send(msg)
            print("Propose with chosen connection sent!")

            self.kill()

    class ReceiveAcceptProposalClientPath(BaseOneShotBehaviour):
        async def run(self):
            await self.agent.prop_chosen_connection_behav.join()

            print("Waiting for ACK chosen connection")
            msg = await self.receive(timeout=30)
            if msg:
                print("Message received with content: {}".format(msg.body))
                self.agent.connection_accepted = True
            else:
                print("Did not received any message after 30 seconds")

            self.kill()

    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))
        req_available_connections_behav = self.RequestAvailableConnections(Config.CLIENT_LOGGER_NAME)
        self.add_behaviour(req_available_connections_behav)

        rec_inf_best_connections_behav = self.ReceiveInformBestConnections(Config.CLIENT_LOGGER_NAME)
        self.add_behaviour(rec_inf_best_connections_behav)

        rec_availability_reservation_behav = self.ReceiveAvailabilityForReservation(Config.CLIENT_LOGGER_NAME)
        self.add_behaviour(rec_availability_reservation_behav)

    def choose_connection(self, connection):
        self.chosen_connection = connection
        prop_chosen_connection_behav = self.ProposeChosenConnection(Config.CLIENT_LOGGER_NAME)
        self.add_behaviour(prop_chosen_connection_behav)

        rec_available_connections_behav = self.ReceiveAcceptProposalClientPath(Config.CLIENT_LOGGER_NAME)
        self.add_behaviour(rec_available_connections_behav)


