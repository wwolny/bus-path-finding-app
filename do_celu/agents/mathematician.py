#
# do_celu
#
# Copyright 2022 Agenty 007
#

from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message


graph=[ [ 0 , 4 ,20 ,16 ,14 ,17 , 3 , 8 ,19 ,19 ],
        [ 4 , 0 , 6 ,11 ,20 , 1 ,13 ,10 , 8 , 3 ],
        [ 20 , 6 , 0 , 1 , 1 , 7 , 5 ,19 ,13 ,19],
        [ 16 ,11 , 1 , 0 ,10 ,15 , 4 , 2 ,10 , 6],
        [ 14 ,20 , 1 ,10 , 0 , 3 , 8 , 7 , 8 , 5],
        [ 17 , 1 , 7 ,15 , 3 , 0 , 3 ,15 , 7 ,12],
        [ 3 ,13 , 5 , 4 , 8 , 3 , 0 ,15 ,12 , 6 ],
        [ 8 ,10 ,19 , 2 , 7 ,15 ,15 , 0 ,15 ,11 ],
        [19 , 8 ,13 ,10 , 8 , 7 ,12 ,15 , 0 , 9 ],
        [19 , 3 ,19 , 6 , 5 ,12 , 6 ,11 , 9 , 0 ]]



class MathAgent(agent.Agent):
    class InformBestPath(BaseOneShotBehaviour):
        async def run(self):
            
            pass

        async def run(self):
            pass

        async def on_end(self):
            pass

    class RecvRequestBestPath(BaseOneShotBehaviour):
        
        
        async def on_start(self):
            pass
            


        async def tsp(needed, busroutes):
            nbuses = len(busroutes)
            for i in range (len(needed)):
                temp = 0
                mincost = 9999
                for j in range (nbuses):
                    currcost = 0
                    busroute = busroutes[j]
                    if len(busroutes[j]) == 1:
                        temp = j
                        break
                    else:
                        temp2 = needed[i]
                        for k in range (len(busroutes[j])-1):
                            currcost += graph[busroute[k]][busroute[k+1]]
                        if temp2[0] == busroute[len(busroute)-1]:
                            currcost = currcost + graph[busroute[len(busroute)-1]][needed[i][1]]
                        else:
                            currcost = currcost + graph[busroute[len(busroute)-1]][needed[i][0]] + graph[needed[i][0]][needed[i][1]]
                        if currcost<mincost:
                            mincost = currcost
                            temp = j

            busroute = busroutes[temp]
            temp2 = needed[i]
            if busroute[len(busroute)-1] != temp2[0]:
                busroute.append(0)
                busroute[len(busroute)-1] = temp2[0]
            busroute.append(0)
            busroute[len(busroute)-1] = temp2[1]
            busroutes.pop(temp)
            busroutes.insert(temp,busroute)
            return busroutes

        async def run(self):
            print("Calculating the best route.")
            busroutes = tsp()
            msg = Message(to=Config.MANAGER_JID)
            msg.set_metadata("performative", Performatives.REQUEST)
            #msg.body = 
            
        async def on_end(self):
            pass

        
    
    class ReceiveAvailableDriversRequest(BaseOneShotBehaviour):
        async def run(self):
            print('Receiving available drivers request...')
            msg = await self.receive(timeout=30)
            if msg:
                print("Receiving available drivers request successful - Body: {}".format(msg.body))
                # TODO trigger getting driver data (find all available drivers and RequestDriverData)
            else:
                print("Receiving available drivers request failed after 30 seconds")


    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))
        self.my_behav = self.MyBehav()
        self.add_behaviour(self.my_behav)
