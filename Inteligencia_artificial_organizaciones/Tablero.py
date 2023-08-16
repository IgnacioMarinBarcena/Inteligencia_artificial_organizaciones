import random
from abc import ABC

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import global_

MAXJUGADORES = 7

class Partida:
    jugadores = []  # Jugadores que se encuentran al principio en una partida
    creencias = []  # Lista de creencias del agente tablero
    mazo = [] # Mazo de Cartas disponibles
    mazo_descartes = [] # Mazo con las cartas descartadas
    # Ciudades del tablero
    ciudades = ["Madrid", "Londres", "Nueva York", "Sao Paulo", "Los Angeles", "Ciudad de Mexico", "Tokyo", "Pekin", "Sidney", "Bagdad", "El Cairo", "Moscu", "Paris",
                "Montreal", "Washington", "Atlanta", "Miami", "Chicago", "San Francisco", "Bogota", "Lima", "Santiago de Chile", "Buenos Aires", "Milan", "San Petersburgo",
                "Estambul", "Argel", "Riad", "Jartum", "Lagos", "Kinsasa", "Johannesburgo", "Teheran", "Nueva Delhi", "Calcuta", "Bombay", "Karachi", "Madras",
                "Bangkok", "Hong Kong", "Taipei", "Seul", "Osaka", "Manila", "Yakarta", "Ho Chi Minh", "Essen", "Shangai"]
    ciudades_obj = [] #Lista de los objetos ciudades (donde se encuentra el nombre, los centros, los cubos, los personajes y las conexiones de cada ciudad)
    # Lista de roles posibles dentro de la partida
    roles = ["Medico", "ExpertoEnOperaciones", "PlanificadorDeContigencia",
             "CoordinadorDeEfectivos", "Analista", "EspecialistaEnCuarentenas", "Genetista"]
    # Jugador con su rol y cartas asignadas
    lista_jugadores_roles = []
    class Jugador:
        def __init__(self, nombre):
            self.nombre = nombre
            self.rol = ""
            self.cartas = []
    # Clase con las ciudades
    class Ciudad:
        def __init__(self, nombre, centro, cubos, color):
            self.nombre = nombre
            self.personajes = []
            self.centro = centro
            self.cubos = cubos
            self.conexiones = []  
            self.color = color 

    # Clase que representa las cartas del juego
    class Carta:
        def __init__(self, nombre, tipo):
            self.nombre = nombre
            self.tipo = tipo  # El tipo de carta puede ser de evento, Rojo o Azul
    
    # Clase con los frascos de enfermedad
    class Enfermedad:
        def __init__(self, color):
            self.color = color
 
    n_evento = ["Una noche tranquila", "Pronostico", "Subvencion del gobierno"]
    for titulo_evento in n_evento:
        i = Carta(titulo_evento, "Evento")
        mazo.append(i)
         
    # Creación de objetos Ciudad y Cartas de ciudad
    cont_color = 0
    global_.ciudades.clear()
    for ciudad in ciudades:
        if cont_color < len(ciudades)//2:  
            color = "Azul"
        else: 
            color = "Rojo"
        carta = Carta(ciudad, color)
        mazo.append(carta)
        cubos = random.randint(0,3)
        if ciudad == "Madrid" or ciudad == "Paris":
            obj_ciudad = Ciudad(ciudad, 1, cubos, color)
            personaje = "Martin"
            obj_ciudad.personajes.append(personaje)
        else:
            obj_ciudad = Ciudad(ciudad, 0, cubos, color)
        ciudades_obj.append(obj_ciudad)
        cont_color +=1
        global_.ciudades.append(obj_ciudad)

    # Conexiones de San Francisco
    ciudades_obj[ciudades.index("San Francisco")].conexiones.append("Chicago")
    ciudades_obj[ciudades.index("San Francisco")].conexiones.append("Los Angeles")
    ciudades_obj[ciudades.index("San Francisco")].conexiones.append("Tokyo")
    ciudades_obj[ciudades.index("San Francisco")].conexiones.append("Manila")

    # Conexiones de Chicago
    ciudades_obj[ciudades.index("Chicago")].conexiones.append("Atlanta")
    ciudades_obj[ciudades.index("Chicago")].conexiones.append("Ciudad de Mexico")
    ciudades_obj[ciudades.index("Chicago")].conexiones.append("Montreal")
    ciudades_obj[ciudades.index("Chicago")].conexiones.append("Los Angeles")
    ciudades_obj[ciudades.index("Chicago")].conexiones.append("San Francisco")
    
    # Conexiones de los Angeles
    ciudades_obj[ciudades.index("Los Angeles")].conexiones.append("Ciudad de Mexico")
    ciudades_obj[ciudades.index("Los Angeles")].conexiones.append("Chicago")
    ciudades_obj[ciudades.index("Los Angeles")].conexiones.append("San Francisco")
    ciudades_obj[ciudades.index("Los Angeles")].conexiones.append("Sidney")

    # Conexiones de Ciudad de Mexico
    ciudades_obj[ciudades.index("Ciudad de Mexico")].conexiones.append("Los Angeles")
    ciudades_obj[ciudades.index("Ciudad de Mexico")].conexiones.append("Chicago")
    ciudades_obj[ciudades.index("Ciudad de Mexico")].conexiones.append("Miami")
    ciudades_obj[ciudades.index("Ciudad de Mexico")].conexiones.append("Bogota")
    ciudades_obj[ciudades.index("Ciudad de Mexico")].conexiones.append("Lima")

    # Conexiones de Atlanta
    ciudades_obj[ciudades.index("Atlanta")].conexiones.append("Chicago")
    ciudades_obj[ciudades.index("Atlanta")].conexiones.append("Miami")
    ciudades_obj[ciudades.index("Atlanta")].conexiones.append("Washington")

    # Conexionees de Montreal
    ciudades_obj[ciudades.index("Montreal")].conexiones.append("Chicago")
    ciudades_obj[ciudades.index("Montreal")].conexiones.append("Washington")
    ciudades_obj[ciudades.index("Montreal")].conexiones.append("Nueva York")

    # Conexiones de Washington
    ciudades_obj[ciudades.index("Washington")].conexiones.append("Montreal")
    ciudades_obj[ciudades.index("Washington")].conexiones.append("Atlanta")
    ciudades_obj[ciudades.index("Washington")].conexiones.append("Nueva York")
    ciudades_obj[ciudades.index("Washington")].conexiones.append("Miami")

    # Conexiones de Nueva york
    ciudades_obj[ciudades.index("Nueva York")].conexiones.append("Londres")
    ciudades_obj[ciudades.index("Nueva York")].conexiones.append("Madrid")
    ciudades_obj[ciudades.index("Nueva York")].conexiones.append("Washington")
    ciudades_obj[ciudades.index("Nueva York")].conexiones.append("Montreal")
    
    # Conexiones de Miami
    ciudades_obj[ciudades.index("Miami")].conexiones.append("Washington")
    ciudades_obj[ciudades.index("Miami")].conexiones.append("Atlanta")
    ciudades_obj[ciudades.index("Miami")].conexiones.append("Ciudad de Mexico")
    ciudades_obj[ciudades.index("Miami")].conexiones.append("Bogota")

    # Conexiones de Bogota
    ciudades_obj[ciudades.index("Bogota")].conexiones.append("Miami")
    ciudades_obj[ciudades.index("Bogota")].conexiones.append("Ciudad de Mexico")
    ciudades_obj[ciudades.index("Bogota")].conexiones.append("Lima")
    ciudades_obj[ciudades.index("Bogota")].conexiones.append("Sao Paulo")
    ciudades_obj[ciudades.index("Bogota")].conexiones.append("Buenos Aires")

    # Conexiones de Lima
    ciudades_obj[ciudades.index("Lima")].conexiones.append("Bogota")
    ciudades_obj[ciudades.index("Lima")].conexiones.append("Ciudad de Mexico")
    ciudades_obj[ciudades.index("Lima")].conexiones.append("Santiago de Chile")

    # Conexiones Santiago de Chile
    ciudades_obj[ciudades.index("Santiago de Chile")].conexiones.append("Lima")

    # Conexiones de Buenos Aires
    ciudades_obj[ciudades.index("Buenos Aires")].conexiones.append("Bogota")
    ciudades_obj[ciudades.index("Buenos Aires")].conexiones.append("Sao Paulo")

    # Conexiones de Sao Paulo
    ciudades_obj[ciudades.index("Sao Paulo")].conexiones.append("Buenos Aires")
    ciudades_obj[ciudades.index("Sao Paulo")].conexiones.append("Bogota")
    ciudades_obj[ciudades.index("Sao Paulo")].conexiones.append("Lagos")
    ciudades_obj[ciudades.index("Sao Paulo")].conexiones.append("Madrid")

    # Conexiones de Lagos
    ciudades_obj[ciudades.index("Lagos")].conexiones.append("Sao Paulo")
    ciudades_obj[ciudades.index("Lagos")].conexiones.append("Kinsasa")
    ciudades_obj[ciudades.index("Lagos")].conexiones.append("Jartum")

    # Conexiones de Jartum
    ciudades_obj[ciudades.index("Jartum")].conexiones.append("Lagos")
    ciudades_obj[ciudades.index("Jartum")].conexiones.append("Kinsasa")
    ciudades_obj[ciudades.index("Jartum")].conexiones.append("Johannesburgo")
    ciudades_obj[ciudades.index("Jartum")].conexiones.append("El Cairo")

    # Conexiones de Kinsasa
    ciudades_obj[ciudades.index("Kinsasa")].conexiones.append("Jartum")
    ciudades_obj[ciudades.index("Kinsasa")].conexiones.append("Johannesburgo")
    ciudades_obj[ciudades.index("Kinsasa")].conexiones.append("Lagos")

    # Conexiones de Johannesburgo
    ciudades_obj[ciudades.index("Johannesburgo")].conexiones.append("Kinsasa")
    ciudades_obj[ciudades.index("Johannesburgo")].conexiones.append("Jartum")
    
    # Conexiones de Madrid
    ciudades_obj[ciudades.index("Madrid")].conexiones.append("Nueva York")
    ciudades_obj[ciudades.index("Madrid")].conexiones.append("Sao Paulo")
    ciudades_obj[ciudades.index("Madrid")].conexiones.append("Londres")
    ciudades_obj[ciudades.index("Madrid")].conexiones.append("Paris")
    ciudades_obj[ciudades.index("Madrid")].conexiones.append("Argel")

    # Conexiones de Londres
    ciudades_obj[ciudades.index("Londres")].conexiones.append("Nueva York")
    ciudades_obj[ciudades.index("Londres")].conexiones.append("Madrid")
    ciudades_obj[ciudades.index("Londres")].conexiones.append("Paris")
    ciudades_obj[ciudades.index("Londres")].conexiones.append("Essen")

    # Conexiones de Paris
    ciudades_obj[ciudades.index("Paris")].conexiones.append("Londres")
    ciudades_obj[ciudades.index("Paris")].conexiones.append("Madrid")
    ciudades_obj[ciudades.index("Paris")].conexiones.append("Argel")
    ciudades_obj[ciudades.index("Paris")].conexiones.append("Milan")
    ciudades_obj[ciudades.index("Paris")].conexiones.append("Essen")

    # Conexiones de Essen
    ciudades_obj[ciudades.index("Essen")].conexiones.append("Londres")
    ciudades_obj[ciudades.index("Essen")].conexiones.append("Paris")
    ciudades_obj[ciudades.index("Essen")].conexiones.append("Milan")
    ciudades_obj[ciudades.index("Essen")].conexiones.append("San Petersburgo")

    # Conexiones de Milan
    ciudades_obj[ciudades.index("Milan")].conexiones.append("Paris")
    ciudades_obj[ciudades.index("Milan")].conexiones.append("Estambul")
    ciudades_obj[ciudades.index("Milan")].conexiones.append("Essen")

    # Conexiones de San Petersburgo
    ciudades_obj[ciudades.index("San Petersburgo")].conexiones.append("Essen")
    ciudades_obj[ciudades.index("San Petersburgo")].conexiones.append("Estambul")
    ciudades_obj[ciudades.index("San Petersburgo")].conexiones.append("Moscu")
    
    # Conexiones de Argel
    ciudades_obj[ciudades.index("Argel")].conexiones.append("El Cairo")
    ciudades_obj[ciudades.index("Argel")].conexiones.append("Estambul")
    ciudades_obj[ciudades.index("Argel")].conexiones.append("Paris")
    ciudades_obj[ciudades.index("Argel")].conexiones.append("Madrid")

    # Conexiones de Estambul
    ciudades_obj[ciudades.index("Estambul")].conexiones.append("Milan")
    ciudades_obj[ciudades.index("Estambul")].conexiones.append("San Petersburgo")
    ciudades_obj[ciudades.index("Estambul")].conexiones.append("Moscu")
    ciudades_obj[ciudades.index("Estambul")].conexiones.append("Argel")
    ciudades_obj[ciudades.index("Estambul")].conexiones.append("El Cairo")

    # Conexiones de Moscu
    ciudades_obj[ciudades.index("Moscu")].conexiones.append("San Petersburgo")
    ciudades_obj[ciudades.index("Moscu")].conexiones.append("Estambul")
    ciudades_obj[ciudades.index("Moscu")].conexiones.append("Teheran")

    # Conexiones de El Cairo
    ciudades_obj[ciudades.index("El Cairo")].conexiones.append("Jartum")
    ciudades_obj[ciudades.index("El Cairo")].conexiones.append("Riad")
    ciudades_obj[ciudades.index("El Cairo")].conexiones.append("Argel")
    ciudades_obj[ciudades.index("El Cairo")].conexiones.append("Estambul")
    ciudades_obj[ciudades.index("El Cairo")].conexiones.append("Bagdad")

    # Conexiones de Bagdad
    ciudades_obj[ciudades.index("Bagdad")].conexiones.append("Estambul")
    ciudades_obj[ciudades.index("Bagdad")].conexiones.append("El Cairo")
    ciudades_obj[ciudades.index("Bagdad")].conexiones.append("Teheran")
    ciudades_obj[ciudades.index("Bagdad")].conexiones.append("Karachi")
    ciudades_obj[ciudades.index("Bagdad")].conexiones.append("Riad")

    # Conexiones de Riad
    ciudades_obj[ciudades.index("Riad")].conexiones.append("Bagdad")
    ciudades_obj[ciudades.index("Riad")].conexiones.append("El Cairo")
    ciudades_obj[ciudades.index("Riad")].conexiones.append("Karachi")

    # Conexiones de Teheran
    ciudades_obj[ciudades.index("Teheran")].conexiones.append("Moscu")
    ciudades_obj[ciudades.index("Teheran")].conexiones.append("Bagdad")
    ciudades_obj[ciudades.index("Teheran")].conexiones.append("Karachi")
    ciudades_obj[ciudades.index("Teheran")].conexiones.append("Nueva Delhi")

    # Conexiones de Karachi
    ciudades_obj[ciudades.index("Karachi")].conexiones.append("Teheran")
    ciudades_obj[ciudades.index("Karachi")].conexiones.append("Bagdad")
    ciudades_obj[ciudades.index("Karachi")].conexiones.append("Riad")
    ciudades_obj[ciudades.index("Karachi")].conexiones.append("Bombay")
    ciudades_obj[ciudades.index("Karachi")].conexiones.append("Nueva Delhi")

    # Conexiones de Bombay
    ciudades_obj[ciudades.index("Bombay")].conexiones.append("Karachi")
    ciudades_obj[ciudades.index("Bombay")].conexiones.append("Nueva Delhi")
    ciudades_obj[ciudades.index("Bombay")].conexiones.append("Madras")

    # Conexiones de Nueva Delhi
    ciudades_obj[ciudades.index("Nueva Delhi")].conexiones.append("Teheran")
    ciudades_obj[ciudades.index("Nueva Delhi")].conexiones.append("Karachi")
    ciudades_obj[ciudades.index("Nueva Delhi")].conexiones.append("Bombay")
    ciudades_obj[ciudades.index("Nueva Delhi")].conexiones.append("Madras")
    ciudades_obj[ciudades.index("Nueva Delhi")].conexiones.append("Calcuta")

    # Conexiones de Madras
    ciudades_obj[ciudades.index("Madras")].conexiones.append("Bombay")
    ciudades_obj[ciudades.index("Madras")].conexiones.append("Nueva Delhi")
    ciudades_obj[ciudades.index("Madras")].conexiones.append("Calcuta")
    ciudades_obj[ciudades.index("Madras")].conexiones.append("Bangkok")
    ciudades_obj[ciudades.index("Madras")].conexiones.append("Yakarta")

    # Conexiones de Calcuta
    ciudades_obj[ciudades.index("Calcuta")].conexiones.append("Nueva Delhi")
    ciudades_obj[ciudades.index("Calcuta")].conexiones.append("Madras")
    ciudades_obj[ciudades.index("Calcuta")].conexiones.append("Bangkok")
    ciudades_obj[ciudades.index("Calcuta")].conexiones.append("Hong Kong")

    # Conexiones de Bangkok
    ciudades_obj[ciudades.index("Bangkok")].conexiones.append("Calcuta")
    ciudades_obj[ciudades.index("Bangkok")].conexiones.append("Madras")
    ciudades_obj[ciudades.index("Bangkok")].conexiones.append("Yakarta")
    ciudades_obj[ciudades.index("Bangkok")].conexiones.append("Ho Chi Minh")
    ciudades_obj[ciudades.index("Bangkok")].conexiones.append("Hong Kong")

    # Conexiones de Yakarta
    ciudades_obj[ciudades.index("Yakarta")].conexiones.append("Madras")
    ciudades_obj[ciudades.index("Yakarta")].conexiones.append("Bangkok")
    ciudades_obj[ciudades.index("Yakarta")].conexiones.append("Ho Chi Minh")
    ciudades_obj[ciudades.index("Yakarta")].conexiones.append("Sidney")

    # Conexiones de Sidney
    ciudades_obj[ciudades.index("Sidney")].conexiones.append("Yakarta")
    ciudades_obj[ciudades.index("Sidney")].conexiones.append("Manila")
    ciudades_obj[ciudades.index("Sidney")].conexiones.append("Los Angeles")

    # Conexiones de Manila
    ciudades_obj[ciudades.index("Manila")].conexiones.append("Sidney")
    ciudades_obj[ciudades.index("Manila")].conexiones.append("Ho Chi Minh")
    ciudades_obj[ciudades.index("Manila")].conexiones.append("Taipei")
    ciudades_obj[ciudades.index("Manila")].conexiones.append("Hong Kong")
    ciudades_obj[ciudades.index("Manila")].conexiones.append("San Francisco")

    # Conexiones de Ho Chi Minh
    ciudades_obj[ciudades.index("Ho Chi Minh")].conexiones.append("Yakarta")
    ciudades_obj[ciudades.index("Ho Chi Minh")].conexiones.append("Manila")
    ciudades_obj[ciudades.index("Ho Chi Minh")].conexiones.append("Bangkok")
    ciudades_obj[ciudades.index("Ho Chi Minh")].conexiones.append("Hong Kong")

    # Conexiones de Hong Kong
    ciudades_obj[ciudades.index("Hong Kong")].conexiones.append("Calcuta")
    ciudades_obj[ciudades.index("Hong Kong")].conexiones.append("Bangkok")
    ciudades_obj[ciudades.index("Hong Kong")].conexiones.append("Ho Chi Minh")
    ciudades_obj[ciudades.index("Hong Kong")].conexiones.append("Manila")
    ciudades_obj[ciudades.index("Hong Kong")].conexiones.append("Taipei")
    ciudades_obj[ciudades.index("Hong Kong")].conexiones.append("Shangai")

    # Conexiones de Shangai
    ciudades_obj[ciudades.index("Shangai")].conexiones.append("Pekin")
    ciudades_obj[ciudades.index("Shangai")].conexiones.append("Hong Kong")
    ciudades_obj[ciudades.index("Shangai")].conexiones.append("Taipei")
    ciudades_obj[ciudades.index("Shangai")].conexiones.append("Seul")
    ciudades_obj[ciudades.index("Shangai")].conexiones.append("Tokyo")

    # Conexiones de Taipei
    ciudades_obj[ciudades.index("Taipei")].conexiones.append("Osaka")
    ciudades_obj[ciudades.index("Taipei")].conexiones.append("Manila")
    ciudades_obj[ciudades.index("Taipei")].conexiones.append("Hong Kong")
    ciudades_obj[ciudades.index("Taipei")].conexiones.append("Shangai")

    # Conexiones de Osaka
    ciudades_obj[ciudades.index("Osaka")].conexiones.append("Taipei")
    ciudades_obj[ciudades.index("Osaka")].conexiones.append("Tokyo")

    # Conexiones de Pekin
    ciudades_obj[ciudades.index("Pekin")].conexiones.append("Shangai")
    ciudades_obj[ciudades.index("Pekin")].conexiones.append("Seul")

    # Conexiones de Seul
    ciudades_obj[ciudades.index("Seul")].conexiones.append("Pekin")
    ciudades_obj[ciudades.index("Seul")].conexiones.append("Shangai")
    ciudades_obj[ciudades.index("Seul")].conexiones.append("Tokyo")

    # Conexiones de Tokyo
    ciudades_obj[ciudades.index("Tokyo")].conexiones.append("Seul")
    ciudades_obj[ciudades.index("Tokyo")].conexiones.append("Shangai")
    ciudades_obj[ciudades.index("Tokyo")].conexiones.append("Osaka")

class Creencia:
    def __init__(self, tipo, conceptos):
        self.nombre = tipo
        self.conceptos = conceptos
       
class AgenteTablero(Agent):
# Comportamiento del agente tablero
    class TableroBehav(CyclicBehaviour):
        async def run(self):
            print("Tablero funcionando")
            # wait for a message for 20 seconds
            msg = await self.receive(timeout=20)
            if msg:
                print("El tablero ha recibido un mensaje")
                if msg.body == "Unirme" and msg.get_metadata("performative") == "request":
                    # El tablero verifica que aun acepta jugadores (mediante una creencia)
                    nCreencia = Creencia(msg.get_metadata(
                        "performative"), [msg.body, msg.sender])
                    
                    # Si hay hueco en la partida se puede unir
                    if len(Partida.jugadores) < MAXJUGADORES:
                        # Comprobamos que este agente no se haya unido antes
                        if len(Partida.creencias) != 0:
                            previo_mensaje = False
                            for c in Partida.creencias:
                                if c.nombre == nCreencia.nombre and c.conceptos[0] == nCreencia.conceptos[0] and c.conceptos[1] == nCreencia.conceptos[1]:
                                    previo_mensaje = True

                            # Si el jugador no se ha unido antes al tablero se une
                            if previo_mensaje == False:
                                # Se une el primer jugador al tablero
                                jugador = Partida.Jugador(str(msg.sender))
                                Partida.jugadores.append(jugador)
                                
                                for ciudad in Partida.ciudades_obj:
                                    if ciudad.nombre == "Madrid":
                                        ciudad.pesonajes.append(str(msg.sender))

                                print("El jugador " + str(msg.sender) +
                                        " se ha unido a la partida\nNº de jugadores: " + str(len(Partida.jugadores)))
                                for i in range(0, 3):
                                    index = random.randint(0, len(Partida.mazo)-1)
                                    jugador.cartas.append(Partida.mazo[index])
                                    print("Al jugador " + str(msg.sender) +
                                            " se le reparte la carta " + Partida.mazo[index])
                                    Partida.mazo.pop(index)
                                

                                # Añadir la nueva creencia
                                Partida.creencias.append(nCreencia)

                                # Instantiate the message
                                replymsg = Message(to=str(msg.sender))
                                # Set the "agree" FIPA performative
                                replymsg.set_metadata("performative", "agree")
                                replymsg.body = msg.body  # Set the message content

                                agreeCreencia = Creencia(replymsg.get_metadata(
                                    "performative"), [msg.body, msg.sender])
                                Partida.creencias.append(agreeCreencia)

                                # Informar de la respuesta
                                await self.send(replymsg)
                                print("Respuesta enviada")

                            # El jugador ya se había unido a la partida
                            else:
                                # Añadir la nueva creencia
                                Partida.creencias.append(nCreencia)

                                # Instantiate the message
                                replymsg = Message(to=str(msg.sender))
                                # Set the "agree" FIPA performative
                                replymsg.set_metadata("performative", "refuse")
                                replymsg.body = msg.body  # Set the message content

                                # Añadir y crear la nueva creencia de rechazo
                                refuseCreencia = Creencia(replymsg.get_metadata(
                                    "performative"), [msg.body, msg.sender])
                                Partida.creencias.append(refuseCreencia)

                                # Informar de la respuesta
                                await self.send(replymsg)

                        else:
                            # Es la primera vez que se solicita unirse asi que se une directamente
                            # Añadir un jugador a la partida
                            jugador = Partida.Jugador(str(msg.sender))
                            Partida.jugadores.append(jugador)

                            for ciudad in Partida.ciudades_obj:
                                    if ciudad.nombre == "Madrid":
                                        ciudad.personajes.append(str(msg.sender))
                            
                            print("El jugador " + str(msg.sender) +
                                    " se ha unido a la partida\nNº de jugadores: " + str(len(Partida.jugadores)))
                            for i in range(0, 3):
                                index = random.randint(0, len(Partida.mazo)-1)
                                jugador.cartas.append(Partida.mazo[index])
                                print("Al jugador " + str(msg.sender) +
                                        " se le reparte la carta " + Partida.mazo[index].nombre)
                                Partida.mazo.pop(index)
                            

                            # Añadir la nueva creencia
                            Partida.creencias.append(nCreencia)

                            # Instantiate the message
                            replymsg = Message(to=str(msg.sender))
                            # Set the "agree" FIPA performative
                            replymsg.set_metadata("performative", "agree")
                            replymsg.body = msg.body  # Set the message content

                            agreeCreencia = Creencia(replymsg.get_metadata(
                                "performative"), [msg.body, msg.sender])
                            Partida.creencias.append(agreeCreencia)

                            # Informamos de la respuesta
                            await self.send(replymsg)
                            print("Respuesta enviada")

                    # Caso en el que el jugador iuntente a unirse a un tablero que se encuentre lleno (ya ha alcanzado el máximo de jugadores)
                    else:
                        # Añadirs la nueva creencia
                        Partida.creencias.append(nCreencia)

                        print("El jugador" + str(msg.sender) +
                                "no se ha podido unir a la partida\nNº de jugadores máximos alcanzados")

                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "refuse")
                        replymsg.body = msg.body  # Set the message content

                        # Añadir y crear la nueva creencia de rechazo
                        refuseCreencia = Creencia(replymsg.get_metadata(
                            "performative"), [msg.body, msg.sender])
                        Partida.creencias.append(refuseCreencia)

                        # Informar de la respuesta
                        await self.send(replymsg)

                # Asignar el rol al jugador
                elif msg.body == "Necesito rol" and msg.get_metadata("performative") == "request":
                    # Crear la creencia
                    nCreencia = Creencia(msg.get_metadata(
                        "performative"), [msg.body, msg.sender])
                    previo_mensaje = False

                    # Comprobar que no se le ha asignado un rol anteriormente
                    for c in Partida.creencias:
                        if c.nombre == nCreencia.nombre and c.conceptos[0] == nCreencia.conceptos[0] and c.conceptos[1] == nCreencia.conceptos[1]:
                            previo_mensaje = True

                    if previo_mensaje == False:
                        # Añadir la nueva creencia
                        Partida.creencias.append(nCreencia)
                        # Asignar un rol al jugador
                        x = random.randint(0, len(Partida.roles)-1)
                        for j in Partida.jugadores:
                            if j.nombre == str(msg.sender):
                                j.rol = Partida.roles[x]
                        print("Al jugador " + str(msg.sender) +
                                " se le asigna el rol " + Partida.roles[x])
                        del Partida.roles[x]
                        # Informar de que se le ha aceptado el rol
                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "agree")
                        replymsg.body = msg.body              # Set the message content

                        # Informamos de la respuesta
                        await self.send(replymsg)
                        print("Respuesta enviada")

                    else:
                        # Añadir la nueva creencia
                        Partida.creencias.append(nCreencia)

                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "refuse")
                        replymsg.body = msg.body  # Set the message content

                        # Añadir y crear la nueva creencia de rechazo
                        refuseCreencia = Creencia(replymsg.get_metadata(
                            "performative"), [msg.body, msg.sender])
                        Partida.creencias.append(refuseCreencia)

                        # Informar de la respuesta
                        await self.send(replymsg)

                # Robar cartas
                elif msg.body == "Roba carta" and msg.get_metadata("performative") == "request":
                    # Crear la creencia
                    nCreencia = Creencia(msg.get_metadata(
                        "performative"), [msg.body, msg.sender])

                    # Añadir la nueva creencia
                    Partida.creencias.append(nCreencia)
                    # Robamos Cartas del mazo
                    if len(Partida.mazo) == 0:
                        print("El jugador " + str(msg.sender) +
                                " no ha podido robar ninguna carta")
                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "refuse")
                        replymsg.body = msg.body 
                    elif len(Partida.mazo) == 1:
                        for j in Partida.jugadores:
                            if j.nombre == str(msg.sender):
                                index = random.randint(0, len(Partida.mazo)-1)
                                j.cartas.append(Partida.mazo[index])
                                print("Solo se ha podido robar una carta")
                                print("El jugador " + str(msg.sender) +
                                        " roba la carta " + Partida.mazo[index].nombre)
                                Partida.mazo.pop(index)
                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "agree")
                        replymsg.body = msg.body 
                    else:
                        for i in range(0, 2):
                            for j in Partida.jugadores:
                                if j.nombre == str(msg.sender):
                                    index = random.randint(0, len(Partida.mazo)-1)
                                    j.cartas.append(Partida.mazo[index])
                                    print("El jugador " + str(msg.sender) +
                                            " roba la carta " + Partida.mazo[index].nombre)
                                    Partida.mazo.pop(index)
                            
                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "agree")
                        replymsg.body = msg.body              # Set the message content
                    
                    # Informamos de la respuesta
                    await self.send(replymsg)
                    print("Respuesta enviada")

                # Descarta cartas
                elif msg.body == "Descarta carta" and msg.get_metadata("performative") == "request":
                    # Crear la creencia
                    nCreencia = Creencia(msg.get_metadata(
                        "performative"), [msg.body, msg.sender])

                    # Añadir la nueva creencia
                    Partida.creencias.append(nCreencia)
                    for j in Partida.jugadores:
                        if j.nombre == str(msg.sender):
                            if len(j.cartas) == 0:
                                print("El jugador " + str(msg.sender) +
                                    " no tiene cartas que descartar")
                                # Instantiate the message
                                replymsg = Message(to=str(msg.sender))
                                # Set the "agree" FIPA performative
                                replymsg.set_metadata("performative", "refuse")
                                replymsg.body = msg.body 
                            else:
                                # Comprobamos cual es el grupo de cartas que menos tenemos y nos desacemos de una de ellas aleatoriamente
                                listaR = []
                                listaA = []
                                listaE = []
                                for i in j.cartas:
                                    if i.tipo == "Rojo":
                                        listaR.append(i)
                                    elif i.tipo == "Azul":
                                        listaA.append(i)
                                    elif i.tipo == "Evento":
                                        listaE.append(i)
                                
                                # Si tenemos carta de evento la descartamos
                                if len(listaE) > 0:
                                    index = random.randint(0, len(listaE)-1)
                                    j.cartas.remove(listaE[index])
                                    Partida.mazo_descartes.append(listaE[index])
                                    print("El jugador " + str(msg.sender) +
                                            " descarta la carta " + listaE[index].nombre)
                                
                                # Si no hay carta evento descarta de la que tienes menos
                                else:
                                    # Si hay menos rojas que azules descartamos rojas
                                    if len(listaR) < len(listaA) and len(listaR) != 0:
                                        index = random.randint(0, len(listaR)-1)
                                        j.cartas.remove(listaR[index])
                                        Partida.mazo_descartes.append(listaR[index])
                                        print("El jugador " + str(msg.sender) +
                                                " descarta la carta " + listaR[index].nombre)
                                    
                                    # Si hay menos azules que rojas descartamos azules
                                    elif len(listaA) < len(listaR) and len(listaA) != 0:
                                        index = random.randint(0, len(listaA)-1)
                                        j.cartas.remove(listaA[index])
                                        Partida.mazo_descartes.append(listaA[index])
                                        print("El jugador " + str(msg.sender) +
                                                " descarta la carta " + listaA[index].nombre)
                                    
                                    # Si hay el mismo número de cartas de ambos tipos o de alguna es 0 descartamos una al azar
                                    elif len(listaA) == 0 or len(listaR) == 0 or len(listaA) == len(listaR):
                                        index = random.randint(0, (len(j.cartas)-1))
                                        Partida.mazo_descartes.append(j.cartas[index])
                                        print("El jugador " + str(msg.sender) +
                                                " descarta la carta " + j.cartas[index].nombre)
                                        j.cartas.pop(index)

                            # Instantiate the message
                            replymsg = Message(to=str(msg.sender))
                            # Set the "agree" FIPA performative
                            replymsg.set_metadata("performative", "agree")
                            replymsg.body = msg.body              # Set the message content
                    
                    # Informamos de la respuesta
                    await self.send(replymsg)
                    print("Respuesta enviada")
                
                # Mueve ficha
                elif msg.body == "Mueve ficha" and msg.get_metadata("performative") == "request":
                    # Crear la creencia
                    nCreencia = Creencia(msg.get_metadata(
                        "performative"), [msg.body, msg.sender])

                    # Añadir la nueva creencia
                    Partida.creencias.append(nCreencia)
                    global_.adyacentes.clear()
                    for ciudades in Partida.ciudades_obj:
                        for k in ciudades.personajes:
                            if k == str(msg.sender):
                                for conexiones in ciudades.conexiones:
                                    for c in Partida.ciudades_obj:
                                        if conexiones == c.nombre:
                                            global_.adyacentes.append(c)
                    
                    global_.mazo_cartas.clear()
                    
                    for j in Partida.jugadores:
                        if j.nombre == str(msg.sender):
                            global_.mazo_cartas = j.cartas
                    
                    if global_.adyacentes:
                        print("El jugador " + str(msg.sender) +
                                            " sabe que se puede mover a: ") 
                        for i in global_.adyacentes:
                            ciudad = i.nombre
                            cubos = i.cubos
                            color = i.color
                            print(ciudad + " que tiene " + str(cubos) + " cubos de enfermedad " + str(color))
                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "agree")
                        replymsg.body = msg.body              # Set the message content
                    else: 
                        print("El jugador " + str(msg.sender) +
                                            " no se puede mover")
                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "refuse")
                        replymsg.body = msg.body              # Set the message content
                    
                    # Informamos de la respuesta
                    await self.send(replymsg)
                    print("Respuesta enviada")
                
                elif msg.body == "Mueve ficha a" and msg.get_metadata("performative") == "request":
                    # Crear la creencia
                    nCreencia = Creencia(msg.get_metadata(
                        "performative"), [msg.body, msg.sender])

                    # Añadir la nueva creencia
                    Partida.creencias.append(nCreencia)
                    if global_.destino:
                        for i in Partida.ciudades_obj:
                            for k in i.personajes:
                                if k == str(msg.sender):
                                    i.personajes.remove(str(msg.sender))
                            if i.nombre == global_.destino:
                                i.personajes.append(str(msg.sender))
                        
                        print("El jugador " + str(msg.sender) +
                                            " se mueve a " + global_.destino)

                        replymsg = Message(to=str(msg.sender))  # Instantiate the message
                        replymsg.set_metadata("performative", "agree") # Set the "agree" FIPA performative
                        replymsg.body = msg.body              # Set the message content
                    else: 
                        print("No existe ese destino")
                        # Instantiate the message
                        replymsg = Message(to=str(msg.sender))
                        # Set the "agree" FIPA performative
                        replymsg.set_metadata("performative", "refuse")
                        replymsg.body = msg.body              # Set the message content
                    
                    # Informamos de la respuesta
                    await self.send(replymsg)
                    print("Respuesta enviada")

                # Tratar enfermedad
                elif msg.body == "Trata enfermedad" and msg.get_metadata("performative") == "request":
                    # Crear la creencia
                    nCreencia = Creencia(msg.get_metadata(
                        "performative"), [msg.body, msg.sender])

                    # Añadir la nueva creencia
                    Partida.creencias.append(nCreencia)
                    for i in Partida.ciudades_obj:
                        for k in i.personajes:
                            if k == str(msg.sender):
                                if i.cubos > 0:
                                    i.cubos -= 1
                                    # Instantiate the message
                                    replymsg = Message(to=str(msg.sender))
                                    # Set the "agree" FIPA performative
                                    replymsg.set_metadata("performative", "agree")
                                    replymsg.body = msg.body  
                                    
                                    print("El jugador " + str(msg.sender) +
                                            " ha eliminado un cubo de enfermedad de " + i.nombre + "\nCubos restantes: " + str(i.cubos))
                                else: 
                                    print("No existe cubos de enfermedad que eliminar")

                        
                                    # Instantiate the message
                                    replymsg = Message(to=str(msg.sender))
                                    # Set the "agree" FIPA performative
                                    replymsg.set_metadata("performative", "refuse")
                                    replymsg.body = msg.body  
                    # Informamos de la respuesta
                    await self.send(replymsg)
                    print("Respuesta enviada")
                else:
                    print("El mensaje no coincide con ninguno de los posibles")

            else:
                print("No se ha recibido ningún mensaje tras 20 segundos")

    async def setup(self):
        print("TableroAgent iniciado")
        b = self.TableroBehav()
        self.add_behaviour(b)
