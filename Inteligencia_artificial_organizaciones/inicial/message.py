import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SenderAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="jaimesf@jabbers.one")     # Instantiate the message -> Poner cuenta del que recive
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.set_metadata("ontology", "myOntology")  # Set the ontology of the message content
            msg.set_metadata("language", "OWL-S")       # Set the language of the message content
            msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!. El mensaje enviado es:", msg.body)

            # set exit_code for the behaviour
            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        self.b = self.InformBehav()
        self.add_behaviour(self.b)


if __name__ == "__main__":
    agent = SenderAgent("", "") # Poner cuenta y contraseña para que funcione
    future = agent.start()
    future.result()

    while agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            agent.stop()
            break
    print("Agent finished with exit code: {}".format(agent.b.exit_code))