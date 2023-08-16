from spade import agent, quit_spade

class tableAgent(agent.Agent):

    async def setup(self):
        print("Agent starting . . .")

'''Crear instancias del tablero, ciudades, enferemedades, movimientos (ciudades proximas a otra)'''