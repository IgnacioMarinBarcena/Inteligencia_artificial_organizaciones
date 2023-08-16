import global_
import random

from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from enum import Enum
from abc import ABC
from spade.behaviour import OneShotBehaviour
from spade.template import Template

class JugadorAgent_Antonio(Agent):
    # definimos como enumerados los tipos de creencias, deseos e intenciones de nuestro agente
    class TipoCreencia(Enum):
        # Tipos de creencias del jugador
        # Unirse a partida
        UNIDO_A_PARTIDA = 1
        ES_TABLERO = 2
        PEDIDO_UNIRSE = 3
        RECHAZADO_A_PARTIDA = 4

        # Pedir rol
        ROL_ASIGNADO = 5
        ROL_PEDIDO = 6
        ROL_RECHAZADO = 7
        
        PARTIDA_LISTA = 8
        
        # Moverse
        CIUDADES_DEVUELTAS = 9
        CIUDADES_PEDIDAS = 10
        CIUDADES_RECHAZADAS = 11

        # Robar carta
        CARTA_ROBADA = 12
        ROBOCARTA_PEDIDO = 13
        ROBOCARTA_RECHAZADO = 14

        # Descartar carta
        CARTA_DESCARTADA = 15
        DESCARTECARTA_PEDIDO = 16
        DESCARTECARTA_RECHAZADO = 17
                
        # Moverse a
        FICHA_MOVIDA = 18
        MOVIMIENTO_PEDIDO = 19
        MOVIMIENTO_RECHAZADO = 20

        # Tratar enfermedad
        ENFERMEDAD_TRATADA = 21
        TRATOENF_PEDIDO = 22
        TRATOENF_RECHAZADO = 23

    class TipoDeseo(Enum):
        JUGAR = 1
        ROL = 2
        ROBAR_CARTA = 3
        DESCARTAR_CARTA = 4
        MOVER_FICHA = 5
        TRATAR_ENFERMEDAD = 6

    class TipoIntencion(Enum):
        PEDIR_UNIRSE = 1
        PEDIR_MOVER_FICHA = 2
        PEDIR_ROL = 3
        PEDIR_ROBAR_CARTA = 4
        PEDIR_DESCARTAR_CARTA = 5
        PEDIR_MOVER_FICHA_A = 6
        PEDIR_TRATAR_ENFERMEDAD = 7

    # Clase que representa las creencias del jugador
    class Creencia():
        def __init__(self, tipo_creencia, valores_creencia):
            self.tipo = tipo_creencia  # Valor de la clase TipoCreencia
            self.valores = []
            self.valores.append(valores_creencia)

    # Clase que representa las intenciones del jugador, se contienen dentro de los deseos
    class Intencion(ABC):
        def __init__(self, tipo_intencion, prioridad):
            self.tipo_intencion = tipo_intencion  # Valor de la clase TipoIntencion
            self.prioridad = prioridad

        def comprobaralcanzada(self, creencias):
            pass

        def comprobaranulada(self, creencias):
            pass

        def ejecuta(self):
            pass

        def calcularprioridad(self, creencias):
            self.prioridad = self.coste + self.urgencia

    # Intención de unirse a la partida
    class Unir_jugador_partida(Intencion):
        def __init__(self, conceptos_intencion, deseo_intencion, posteriores):
            # Conceptos necesarios para ejecutar la intencion
            self.conceptos = conceptos_intencion
            self.tipo = JugadorAgent_Antonio.TipoIntencion.PEDIR_UNIRSE
            self.deseo = deseo_intencion
            self.coste = 0
            self.urgencia = 0
            self.posteriores = []  # Lista con intenciones que puede que necesiten ejecutarse despues
            self.posteriores.append(posteriores)

        # Compobar si se ha cumplido la intencion
        def comprobaralcanzada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.UNIDO_A_PARTIDA:
                    return True
            return False

        # Compobar si la intencion ya no se puede realizar
        def comprobaranulada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.RECHAZADO_A_PARTIDA:
                    return True
            return False

        # Ejecutar la intención
        async def ejecuta(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tid = c.valores[0]
                    msg = Message(to=tid)  # Instantiate the message
                    # Set the "request" FIPA performative
                    msg.set_metadata("performative", "request")
                    msg.body = "Unirme"  # Set the message content
                    miCreencia = JugadorAgent_Antonio.Creencia(
                        JugadorAgent_Antonio.TipoCreencia.PEDIDO_UNIRSE, tid)
                    return msg, miCreencia  # Devuelve el mensaje y la creencia para que puedan ser tratados

    # Intención de pedirle un rol al tablero
    class Solicitar_rol(Intencion):
        def __init__(self, conceptos_intencion, deseo_intencion, posteriores):
            # Conceptos necesarios para ejecutar la intencion
            self.conceptos = conceptos_intencion
            self.tipo = JugadorAgent_Antonio.TipoIntencion.PEDIR_ROL
            self.deseo = deseo_intencion
            self.coste = 0
            self.urgencia = 0
            self.posteriores = []  # Lista con intenciones que puede que necesiten ejecutarse despues
            self.posteriores.append(posteriores)

        # Compobar si se ha cumplido la intencion
        def comprobaralcanzada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROL_ASIGNADO:
                    return True
            return False

        # Compobar si la intencion ya no se puede realizar
        def comprobaranulada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROL_RECHAZADO:
                    return True
            return False

        # Ejecutar la intención
        async def ejecuta(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tid = c.valores[0]
                    msg = Message(to=tid)  # Instantiate the message
                    # Set the "request" FIPA performative
                    msg.set_metadata("performative", "request")
                    msg.body = "Necesito rol"  # Set the message content
                    miCreencia = JugadorAgent_Antonio.Creencia(
                        JugadorAgent_Antonio.TipoCreencia.ROL_PEDIDO, tid)
                    return msg, miCreencia  # Devuelve el mensaje y la creencia para que puedan ser tratados

    # Intención de mover una ficha
    class Mover_ficha(Intencion):
        def __init__(self, conceptos_intencion, deseo_intencion, posteriores):
            # Conceptos necesarios para ejecutar la intencion
            self.conceptos = conceptos_intencion
            self.tipo = JugadorAgent_Antonio.TipoIntencion.PEDIR_MOVER_FICHA
            self.deseo = deseo_intencion
            self.coste = 0
            self.urgencia = 0
            self.posteriores = []  # Lista con intenciones que puede que necesiten ejecutarse despues
            self.posteriores.append(posteriores)

        # Compobar si se ha cumplido la intencion
        def comprobaralcanzada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CIUDADES_DEVUELTAS:
                    return True
            return False

        # Compobar si la intencion ya no se puede realizar
        def comprobaranulada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CIUDADES_RECHAZADAS:
                    return True
            return False

        # Ejecutar la intención
        async def ejecuta(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tid = c.valores[0]
                    msg = Message(to=tid)  # Instantiate the message
                    # Set the "request" FIPA performative
                    msg.set_metadata("performative", "request")
                    msg.body = "Mueve ficha"  # Set the message content
                    miCreencia = JugadorAgent_Antonio.Creencia(
                        JugadorAgent_Antonio.TipoCreencia.CIUDADES_PEDIDAS, tid)
                    return msg, miCreencia  # Devuelve el mensaje y la creencia para que puedan ser tratados
    
    # Intención de mover una ficha a
    class Mover_ficha_a(Intencion):
        def __init__(self, conceptos_intencion, deseo_intencion, posteriores):
            # Conceptos necesarios para ejecutar la intencion
            self.conceptos = conceptos_intencion
            self.tipo = JugadorAgent_Antonio.TipoIntencion.PEDIR_MOVER_FICHA_A
            self.deseo = deseo_intencion
            self.coste = 0
            self.urgencia = 0
            self.posteriores = []  # Lista con intenciones que puede que necesiten ejecutarse despues
            self.posteriores.append(posteriores)

        # Compobar si se ha cumplido la intencion
        def comprobaralcanzada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.FICHA_MOVIDA:
                    return True
            return False

        # Compobar si la intencion ya no se puede realizar
        def comprobaranulada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.MOVIMIENTO_RECHAZADO:
                    return True
            return False

        # Ejecutar la intención
        async def ejecuta(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tid = c.valores[0]
                    msg = Message(to=tid)  # Instantiate the message
                    # Set the "request" FIPA performative
                    msg.set_metadata("performative", "request")
                    msg.body = "Mueve ficha a"  # Set the message content
                    # Calculamos la ciudad destino a la que nos movemos
                    ciudadesM = []
                    for c in global_.adyacentes:
                        if len(c.personajes) > 0:
                            ciudadesM.append(c)
                            
                    if len(ciudadesM) > 0:
                        index = random.randint(0, len(ciudadesM)-1)
                        global_.destino = ciudadesM[index].nombre
                    else:
                        index = random.randint(0, len(global_.adyacentes)-1)
                        global_.destino = global_.adyacentes[index].nombre

                    miCreencia = JugadorAgent_Antonio.Creencia(
                        JugadorAgent_Antonio.TipoCreencia.MOVIMIENTO_PEDIDO, tid)
                    return msg, miCreencia  # Devuelve el mensaje y la creencia para que puedan ser tratados

    # Intención de robar carta
    class Robar_carta(Intencion):
        def __init__(self, conceptos_intencion, deseo_intencion, posteriores):
            # Conceptos necesarios para ejecutar la intencion
            self.conceptos = conceptos_intencion
            self.tipo = JugadorAgent_Antonio.TipoIntencion.PEDIR_ROBAR_CARTA
            self.deseo = deseo_intencion
            self.coste = 0
            self.urgencia = 0
            self.posteriores = []  # Lista con intenciones que puede que necesiten ejecutarse despues
            self.posteriores.append(posteriores)

        # Compobar si se ha cumplido la intencion
        def comprobaralcanzada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CARTA_ROBADA:
                    return True
            return False

        # Compobar si la intencion ya no se puede realizar
        def comprobaranulada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROBOCARTA_RECHAZADO:
                    return True
            return False

        # Ejecutar la intención
        async def ejecuta(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tid = c.valores[0]
                    msg = Message(to=tid)  # Instantiate the message
                    # Set the "request" FIPA performative
                    msg.set_metadata("performative", "request")
                    msg.body = "Roba carta"  # Set the message content
                    miCreencia = JugadorAgent_Antonio.Creencia(
                        JugadorAgent_Antonio.TipoCreencia.ROBOCARTA_PEDIDO, tid)
                    return msg, miCreencia  # Devuelve el mensaje y la creencia para que puedan ser tratados

    # Intención de descartar carta
    class Descartar_carta(Intencion):
        def __init__(self, conceptos_intencion, deseo_intencion, posteriores):
            # Conceptos necesarios para ejecutar la intencion
            self.conceptos = conceptos_intencion
            self.tipo = JugadorAgent_Antonio.TipoIntencion.PEDIR_DESCARTAR_CARTA
            self.deseo = deseo_intencion
            self.coste = 0
            self.urgencia = 0
            self.posteriores = []  # Lista con intenciones que puede que necesiten ejecutarse despues
            self.posteriores.append(posteriores)

        # Compobar si se ha cumplido la intencion
        def comprobaralcanzada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CARTA_DESCARTADA:
                    return True
            return False

        # Compobar si la intencion ya no se puede realizar
        def comprobaranulada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.DESCARTECARTA_RECHAZADO:
                    return True
            return False

        # Ejecutar la intención
        async def ejecuta(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tid = c.valores[0]
                    msg = Message(to=tid)  # Instantiate the message
                    # Set the "request" FIPA performative
                    msg.set_metadata("performative", "request")
                    msg.body = "Descarta carta"  # Set the message content
                    miCreencia = JugadorAgent_Antonio.Creencia(
                        JugadorAgent_Antonio.TipoCreencia.DESCARTECARTA_PEDIDO, tid)
                    return msg, miCreencia  # Devuelve el mensaje y la creencia para que puedan ser tratados
    
    # Intención de tratar enfermedad
    class Tratar_enfermedad(Intencion):
        def __init__(self, conceptos_intencion, deseo_intencion, posteriores):
            # Conceptos necesarios para ejecutar la intencion
            self.conceptos = conceptos_intencion
            self.tipo = JugadorAgent_Antonio.TipoIntencion.PEDIR_TRATAR_ENFERMEDAD
            self.deseo = deseo_intencion
            self.coste = 0
            self.urgencia = 0
            self.posteriores = []  # Lista con intenciones que puede que necesiten ejecutarse despues
            self.posteriores.append(posteriores)

        # Compobar si se ha cumplido la intencion
        def comprobaralcanzada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ENFERMEDAD_TRATADA:
                    return True
            return False

        # Compobar si la intencion ya no se puede realizar
        def comprobaranulada(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.TRATOENF_RECHAZADO:
                    return True
            return False

        # Ejecutar la intención
        async def ejecuta(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tid = c.valores[0]
                    msg = Message(to=tid)  # Instantiate the message
                    # Set the "request" FIPA performative
                    msg.set_metadata("performative", "request")
                    msg.body = "Trata enfermedad"  # Set the message content
                    miCreencia = JugadorAgent_Antonio.Creencia(
                        JugadorAgent_Antonio.TipoCreencia.TRATOENF_PEDIDO, tid)
                    return msg, miCreencia  # Devuelve el mensaje y la creencia para que puedan ser tratados

    # Clase abstracta con las funciones a aplicar sobre los deseos
    class Deseo(ABC):

        # Comprobar que el deseo no es imposible realizarlo
        def comprobarimposible(self, creencias):
            pass

        # Comprobar si se ha cumplido el deseo
        def comprobarsatisfecho(self, creencias):
            pass

        # Comprbar que el deseo sigue estando activo
        def comprobarinteres(self, creencias):
            pass

        # Comprobar si el deseo necesita ser activado
        def comprobaractivar(self, creencias):
            pass

    # Deseo de unirse a la partida
    class Jugar(Deseo):
        def __init__(self, intenciones_deseo, conceptos_deseo):
            self.intenciones = [] # Intenciones necesarias para que se cumpla el deseo
            self.intenciones.append(intenciones_deseo)
            self.conceptos = conceptos_deseo
            self.activo = False  # Booleano que representa si el deseo esta activo o no
            self.tipo = JugadorAgent_Antonio.TipoDeseo.JUGAR

        # Comprobar que el deseo no es imposible realizarlo
        def comprobarimposible(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.RECHAZADO_A_PARTIDA:
                    return True
            return False

        # Comprobar si se ha cumplido el deseo
        def comprobarsatisfecho(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.UNIDO_A_PARTIDA:
                    return True
            return False

        # Comprbar que el deseo sigue estando activo
        def comprobarinteres(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.PEDIDO_UNIRSE:
                    return True
            return False

        # Comprobar si el deseo necesita ser activado
        def comprobaractivar(self, creencias):
            pedido = False
            tablero_conocido = False
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.PEDIDO_UNIRSE:
                    pedido = True
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tablero_conocido = True
            return not pedido and tablero_conocido
    
    # Deseo de obtener rol
    class Rol(Deseo):
        def __init__(self, intenciones_deseo, conceptos_deseo):
            self.intenciones = [] # Intenciones necesarias para que se cumpla el deseo
            self.intenciones.append(intenciones_deseo)
            self.conceptos = conceptos_deseo
            self.activo = False  # Booleano que representa si el deseo esta activo o no
            self.tipo = JugadorAgent_Antonio.TipoDeseo.ROL

        # Comprobar que el deseo no es imposible realizarlo
        def comprobarimposible(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROL_RECHAZADO:
                    return True
            return False

        # Comprobar si se ha cumplido el deseo
        def comprobarsatisfecho(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROL_ASIGNADO:
                    return True
            return False

        # Comprbar que el deseo sigue estando activo
        def comprobarinteres(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROL_PEDIDO:
                    return True
            return False

        # Comprobar si el deseo necesita ser activado
        def comprobaractivar(self, creencias):
            pedido = False
            tablero_conocido = False
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.UNIDO_A_PARTIDA:
                    pedido = True
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROL_PEDIDO:
                    pedido = False
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tablero_conocido = True
            return pedido and tablero_conocido
    
    # Deseo de robar carta
    class Robar(Deseo):
        def __init__(self, intenciones_deseo, conceptos_deseo):
            self.intenciones = [] # Intenciones necesarias para que se cumpla el deseo
            self.intenciones.append(intenciones_deseo)
            self.conceptos = conceptos_deseo
            self.activo = False  # Booleano que representa si el deseo esta activo o no
            self.tipo = JugadorAgent_Antonio.TipoDeseo.ROBAR_CARTA

        # Comprobar que el deseo no es imposible realizarlo
        def comprobarimposible(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROBOCARTA_RECHAZADO:
                    return True
            return False

        # Comprobar si se ha cumplido el deseo
        def comprobarsatisfecho(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CARTA_ROBADA:
                    return True
            return False

        # Comprbar que el deseo sigue estando activo
        def comprobarinteres(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROBOCARTA_PEDIDO:
                    return True
            return False

        # Comprobar si el deseo necesita ser activado
        def comprobaractivar(self, creencias):
            pedido = False
            tablero_conocido = False
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROL_ASIGNADO:
                    pedido = True
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ROBOCARTA_PEDIDO:
                    pedido = False
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tablero_conocido = True
            return pedido and tablero_conocido
    
    # Deseo de descartar carta
    class Descartar(Deseo):
        def __init__(self, intenciones_deseo, conceptos_deseo):
            self.intenciones = [] # Intenciones necesarias para que se cumpla el deseo
            self.intenciones.append(intenciones_deseo)
            self.conceptos = conceptos_deseo
            self.activo = False  # Booleano que representa si el deseo esta activo o no
            self.tipo = JugadorAgent_Antonio.TipoDeseo.DESCARTAR_CARTA

        # Comprobar que el deseo no es imposible realizarlo
        def comprobarimposible(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.DESCARTECARTA_RECHAZADO:
                    return True
            return False

        # Comprobar si se ha cumplido el deseo
        def comprobarsatisfecho(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CARTA_DESCARTADA:
                    return True
            return False

        # Comprbar que el deseo sigue estando activo
        def comprobarinteres(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.DESCARTECARTA_PEDIDO:
                    return True
            return False

        # Comprobar si el deseo necesita ser activado
        def comprobaractivar(self, creencias):
            pedido = False
            tablero_conocido = False
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CARTA_ROBADA:
                    pedido = True
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.DESCARTECARTA_PEDIDO:
                    pedido = False
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tablero_conocido = True
            return pedido and tablero_conocido
    
    # Deseo de mover ficha
    class Moverficha(Deseo):
        def __init__(self, intenciones_deseo, conceptos_deseo):
            self.intenciones = intenciones_deseo # Intenciones necesarias para que se cumpla el deseo
            self.conceptos = conceptos_deseo
            self.activo = False  # Booleano que representa si el deseo esta activo o no
            self.tipo = JugadorAgent_Antonio.TipoDeseo.MOVER_FICHA

        # Comprobar que el deseo no es imposible realizarlo
        def comprobarimposible(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CIUDADES_RECHAZADAS or c.tipo == JugadorAgent_Antonio.TipoCreencia.MOVIMIENTO_RECHAZADO:
                    return True
            return False

        # Comprobar si se ha cumplido el deseo
        def comprobarsatisfecho(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.FICHA_MOVIDA:
                    return True
            return False

        # Comprbar que el deseo sigue estando activo
        def comprobarinteres(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CIUDADES_PEDIDAS or c.tipo == JugadorAgent_Antonio.TipoCreencia.MOVIMIENTO_PEDIDO:
                    return True
            return False

        # Comprobar si el deseo necesita ser activado
        def comprobaractivar(self, creencias):
            pedido = False
            tablero_conocido = False
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.CARTA_DESCARTADA:
                    pedido = True
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.MOVIMIENTO_PEDIDO:
                    pedido = False
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tablero_conocido = True
            return pedido and tablero_conocido
    
    # Deseo tratar enfermedad
    class Tratarenfermedad(Deseo):
        def __init__(self, intenciones_deseo, conceptos_deseo):
            self.intenciones = [] # Intenciones necesarias para que se cumpla el deseo
            self.intenciones.append(intenciones_deseo)
            self.conceptos = conceptos_deseo
            self.activo = False  # Booleano que representa si el deseo esta activo o no
            self.tipo = JugadorAgent_Antonio.TipoDeseo.TRATAR_ENFERMEDAD

        # Comprobar que el deseo no es imposible realizarlo
        def comprobarimposible(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.TRATOENF_RECHAZADO:
                    return True
            return False

        # Comprobar si se ha cumplido el deseo
        def comprobarsatisfecho(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ENFERMEDAD_TRATADA:
                    return True
            return False

        # Comprbar que el deseo sigue estando activo
        def comprobarinteres(self, creencias):
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.TRATOENF_PEDIDO:
                    return True
            return False

        # Comprobar si el deseo necesita ser activado
        def comprobaractivar(self, creencias):
            pedido = False
            tablero_conocido = False
            for c in creencias:
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.FICHA_MOVIDA:
                    pedido = True
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.TRATOENF_PEDIDO:
                    pedido = False
                if c.tipo == JugadorAgent_Antonio.TipoCreencia.ES_TABLERO:
                    tablero_conocido = True
            return pedido and tablero_conocido

    # Actualizar las creencias del agente jugador
    def actualizaCreencias(self, msg):
        if msg.body == "Unirme" and msg.get_metadata("performative") == "agree":
            miCreencia = JugadorAgent_Antonio.Creencia(
                JugadorAgent_Antonio.TipoCreencia.UNIDO_A_PARTIDA, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Unirme" and msg.get_metadata("performative") == "refuse":
            miCreencia = self.Creencia(
                JugadorAgent_Antonio.TipoCreencia.RECHAZADO_A_PARTIDA, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Necesito rol" and msg.get_metadata("performative") == "agree":
            miCreencia = JugadorAgent_Antonio.Creencia(
                JugadorAgent_Antonio.TipoCreencia.ROL_ASIGNADO, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Necesito rol" and msg.get_metadata("performative") == "refuse":
            miCreencia = self.Creencia(
                JugadorAgent_Antonio.TipoCreencia.ROL_RECHAZADO, str(msg.sender))
            self.misCreencias.append(miCreencia)
        
        if msg.body == "Mueve ficha" and msg.get_metadata("performative") == "agree":
            miCreencia = JugadorAgent_Antonio.Creencia(
                JugadorAgent_Antonio.TipoCreencia.CIUDADES_DEVUELTAS, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Mueve ficha" and msg.get_metadata("performative") == "refuse":
            miCreencia = self.Creencia(
                JugadorAgent_Antonio.TipoCreencia.CIUDADES_RECHAZADAS, str(msg.sender))
            self.misCreencias.append(miCreencia)
        
        if msg.body == "Roba carta" and msg.get_metadata("performative") == "agree":
            miCreencia = JugadorAgent_Antonio.Creencia(
                JugadorAgent_Antonio.TipoCreencia.CARTA_ROBADA, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Roba carta" and msg.get_metadata("performative") == "refuse":
            miCreencia = self.Creencia(
                JugadorAgent_Antonio.TipoCreencia.ROBOCARTA_RECHAZADO, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Descarta carta" and msg.get_metadata("performative") == "agree":
            miCreencia = JugadorAgent_Antonio.Creencia(
                JugadorAgent_Antonio.TipoCreencia.CARTA_DESCARTADA, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Descarta carta" and msg.get_metadata("performative") == "refuse":
            miCreencia = self.Creencia(
                JugadorAgent_Antonio.TipoCreencia.DESCARTECARTA_RECHAZADO, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Mueve ficha a" and msg.get_metadata("performative") == "agree":
            miCreencia = JugadorAgent_Antonio.Creencia(
                JugadorAgent_Antonio.TipoCreencia.FICHA_MOVIDA, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Mueve ficha a" and msg.get_metadata("performative") == "refuse":
            miCreencia = self.Creencia(
                JugadorAgent_Antonio.TipoCreencia.MOVIMIENTO_RECHAZADO, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Trata enfermedad" and msg.get_metadata("performative") == "agree":
            miCreencia = JugadorAgent_Antonio.Creencia(
                JugadorAgent_Antonio.TipoCreencia.ENFERMEDAD_TRATADA, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == "Trata enfermedad" and msg.get_metadata("performative") == "refuse":
            miCreencia = self.Creencia(
                JugadorAgent_Antonio.TipoCreencia.TRATOENF_RECHAZADO, str(msg.sender))
            self.misCreencias.append(miCreencia)

        if msg.body == None:
            pass
            
    # Actualizar los deseos del agente jugador
    def actualizaDeseos(self):
        for d in self.misDeseos:
            if d.activo:
                if d.comprobarimposible(self.misCreencias) or d.comprobarsatisfecho(self.misCreencias) and d.comprobarinteres(self.misCreencias):
                    for i in d.intenciones:
                        if i in self.misIntenciones:
                            self.misIntenciones.remove(i)
                    d.activo = False
                else:
                    if d.comprobaractivar(self.misCreencias):
                        if d.intenciones[0] not in self.misIntenciones:
                        # Colocar la siguiente intencion del deseo en las intenciones del agente
                            self.misIntenciones.append(d.intenciones[0])
            # Fijarse en d itenciones no en self
            else:
                if d.comprobaractivar(self.misCreencias):
                    # Colocar la primera intencion del deseo en las intenciones del agente
                    self.misIntenciones.append(d.intenciones[0])
                    d.activo = True

    # Actualizar las intenciones del agente jugador
    def actualizaIntenciones(self):
        # Variable auxiliar que representa si el jugador sigue teniendo intenciones
        hay_intenciones = True
        intenciones = self.misIntenciones.copy()
        for i in self.misIntenciones:
            if i.comprobaralcanzada(self.misCreencias):
                # quitar la intencion actual de la lista de intenciones del agente si se ha cumplido
                intenciones.remove(i)
                if len(i.posteriores) != 0:
                    if i.posteriores[0] != None:
                        # poner siguiente intencion del deseo en la lista de intenciones del agente
                        intenciones.append(i.posteriores[0])
                        i.posteriores.pop(0)
                        
            elif i.comprobaranulada(self.misCreencias):
                for p in i.posteriores:
                    if p != None:
                        # quitar todas las intenciones posteriores de las intenciones del agente si no se ha cumplido
                        intenciones.remove(p)
                intenciones.remove(i)
                
        self.misIntenciones = intenciones.copy()
            
        if len(self.misIntenciones) == 0:
            # Variable auxiliar que ayuda a detener el programa si el jugador se queda sin intenciones
            global_.parar = True
            hay_intenciones = False

        return hay_intenciones

    def calculaPrioridades(self):
        for i in self.misIntenciones:
            i.calcularprioridad(self.misCreencias)

    async def elige_y_ejecutaIntencion(self):
        maximaprioridad = 0
        intencion_a_ejecutar = self.misIntenciones[0]
        """for i in self.misIntenciones:
            if i.prioridad >= maximaprioridad:
                maximaprioridad = i.prioridad
                intencion_a_ejecutar = i"""
        msg, miCreencia = await intencion_a_ejecutar.ejecuta(self.misCreencias)
        self.misCreencias.append(miCreencia)

        return msg

    class JugadorBehav(CyclicBehaviour):

        async def run(self):
            print("Jugador funcionando")
            # wait for a message for 10 seconds
            msg = await self.receive(timeout=10)
            if msg:
                print("El Jugador ha recibido un mensaje ")
                self.agent.actualizaCreencias(msg)
            self.agent.actualizaDeseos()
            hay_intenciones = self.agent.actualizaIntenciones()
            if hay_intenciones == False:
                print("El agente no tiene intenciones que realizar")
            else:
                self.agent.calculaPrioridades()
                msg = await self.agent.elige_y_ejecutaIntencion()
                await self.send(msg)
                print("Mensaje enviado")
                
    # Iniciación del propio agente
    async def setup(self):
        print("JugadorAgent_Antonio iniciado")
        self.tablero_Id = "tablerog5@jabbers.one"
        self.misCreencias = []
        self.misIntenciones = []
        self.misDeseos = []
        
        miCreencia = self.Creencia(JugadorAgent_Antonio.TipoCreencia.ES_TABLERO, self.tablero_Id)
        self.misCreencias.append(miCreencia)
        
        miIntencion7 = self.Tratar_enfermedad(None, None, None)
        miIntencion6 = self.Mover_ficha_a(None, None, None)
        miIntencion5 = self.Mover_ficha(None, None, miIntencion6)
        miIntencion4 = self.Descartar_carta(None, None, None)
        miIntencion3 = self.Robar_carta(None, None, None)
        miIntencion2 = self.Solicitar_rol(None, None, None)
        miIntencion1 = self.Unir_jugador_partida(None, None, None)
         
        miDeseo1 = self.Jugar(miIntencion1, None)
        miDeseo1.activo = True
        self.misDeseos.append(miDeseo1)
        
        miDeseo2 = self.Rol(miIntencion2, None)
        self.misDeseos.append(miDeseo2)

        miDeseo3 = self.Robar(miIntencion3, None)
        self.misDeseos.append(miDeseo3)

        miDeseo4 = self.Descartar(miIntencion4, None)
        self.misDeseos.append(miDeseo4)

        intencionesMoverse = [miIntencion5, miIntencion6]
        miIntencion5.posteriores.append(miIntencion6)
        miDeseo5 = self.Moverficha(intencionesMoverse, None)
        self.misDeseos.append(miDeseo5)

        miDeseo6 = self.Tratarenfermedad(miIntencion7, None)
        self.misDeseos.append(miDeseo6)
        
        b = self.JugadorBehav()
        self.add_behaviour(b)
