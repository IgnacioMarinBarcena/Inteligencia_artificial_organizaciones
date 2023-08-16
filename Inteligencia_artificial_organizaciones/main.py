import time

from Tablero import AgenteTablero
from Jugador_Nacho import JugadorAgent_Nacho
from Jugador_Martin import JugadorAgent_Martin
from Jugador_Diego import JugadorAgent_Diego
from Jugador_Jaime import JugadorAgent_Jaime
from Jugador_Antonio import JugadorAgent_Antonio
#from Jugador_Alberto import JugadorAgent_Alberto


import global_

if __name__ == "__main__":

    agentetablero = AgenteTablero("tablerog5@jabbers.one", "Tablerouc3m")
    future_tablero = agentetablero.start()
    time.sleep(8)

    """agentejugador = JugadorAgent_Nacho("100432039@jabbers.one", "Nmbp12714")
    future_jugador = agentejugador.start()"""

    """agentejugador = JugadorAgent_Martin("0432055@jabbers.one", "Alumnouc3m")
    future_jugador = agentejugador.start()"""

    """agentejugador = JugadorAgent_Diego("100432074@jabbers.one", "Montaraz_2013")
    future_jugador = agentejugador.start()"""

    agentejugador = JugadorAgent_Jaime("100432147@jabbers.one", "123456789")
    future_jugador = agentejugador.start()

    """agentejugador = JugadorAgent_Antonio("100432147@jabbers.one", "123456789")
    future_jugador = agentejugador.start()"""

    """agentejugador = JugadorAgent_Alberto("100432147@jabbers.one", "123456789")
    future_jugador = agentejugador.start()"""

    future_tablero.result()
    future_jugador.result()

    while agentetablero.is_alive():
        try:
            if global_.parar == True:
                agentetablero.stop()
                agentejugador.stop()
                break
            time.sleep(1)
        except KeyboardInterrupt:
            agentetablero.stop()
            agentejugador.stop()
            break
    print("Ejecucion terminada")
