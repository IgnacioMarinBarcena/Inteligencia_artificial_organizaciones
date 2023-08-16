import getpass
import time

from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour 
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from enum import Enum
from abc import ABC, abstractmethod

class JugadorAgent(Agent):
    # definimos como enumerados los tipos de creencias, deseos e intenciones de nuestro agente
    class TipoCreencia(Enum):
        # algunos de estos tipos de creencias coincidiran con los predicados
        # Tipos de creencia ya he me he unido, ya he pedido univer etc...
        UNIDO_A_PARTIDA = 1
        ES_TABLERO = 2
        PEDIDO_UNIRSE = 3
        RECHAZADO_A_PARTIDA = 4

    class TipoDeseo(Enum):
        # algunos de estos tipos de deseos coincidiran con los protocolos/servicios
        JUGAR = 1
 
    class TipoIntencion(Enum):
        # algunos de estos tipos de creencias coincidiran con las acciones
        PEDIR_UNIRSE = 1
 
 
    class Creencia(): # clase sin metodos, solo sirve para encapsular datos
        # generica para todos
        def __init__(self, tipo_creencia, valores_creencia):
            self.valores = []
            self.tipo = tipo_creencia
            self.valores.append(valores_creencia)

    class Intencion(ABC): # clase abstracta0
        @abstractmethod
        async def comprobaralcanzada(self,creencias):
            pass
        @abstractmethod
        async def comprobaranulada(self,creencias):
            pass
        @abstractmethod            
        async def ejecuta(self):
            #las otras dos definen que ejecutas
            pass
        @abstractmethod   
        async def calcularprioridad(self,creencias):
            self.prioridad = self.coste + self.urgencia

    # subclase de la clase intención
    class Pedir_Unirse(Intencion):
        def __init__(self, conceptos_intencion, TipoIntencion, deseo_intencion, posteriores):
            self.conceptos = conceptos_intencion #los conceptos de la acción
            self.tipo = TipoIntencion.PEDIR_UNIRSE #La acción/intención a realizar
            self.deseo = deseo_intencion #Indicar a que deseo pertenece la intención ya que los planes son secuencial
            self.coste = 0
            self.urgencia = 0
            self.posteriores = posteriores

        async def comprobaralcanzada(self,creencias):
            for c in creencias:
                if c.tipo == self.UNIDO_A_PARTIDA:
                    return True
                else:
                    return False
        async def comprobaranulada(self,creencias):
            for c in creencias:
                if c.tipo == self.RECHAZADO_A_PARTIDA:
                    return True
                else:
                    return False
                
        async def ejecuta(self):
        # aqui manda el mensaje request al tablero
        # y añade la creencia PEDIDO_UNIRSE
            print("Mensaje de unirse enviado")                    
            for c in self.misCreencias:
                if c.tipo == self.TipoCreencia.ES_TABLERO:
                    tid= c.valores[0]
            msg = Message(to=tid)  # Instantiate the message
            msg.set_metadata(
                "performative", "request"
            )  # Set the "request" FIPA performative
            msg.body = "Unirme" # Set the message content
            await self.send(msg)
            miCreencia = self.Creencia (self.PEDIDO_UNIRSE, self.tablero_Id)
            self.misCreencias.append(miCreencia)

        
    class Deseo(ABC): # clase abstracta
        @abstractmethod
        async def comprobarimposible(self,creencias):
            pass
        @abstractmethod
        async def comprobarsatisfecho(self,creencias):
            pass
        @abstractmethod
        async def comprobarinteres(self,creencias):
            pass
        @abstractmethod
        async def comprobaractivar(self,creencias):
            pass

    class Jugar(Deseo):
        def __init__(self, TipoDeseo, intenciones_deseo, conceptos_deseo):
            self.intenciones = intenciones_deseo
            self.conceptos = conceptos_deseo
            self.activo = False
            self.tipo = TipoDeseo.JUGAR
            
        # como el deseo solo tiene una intencion, coinciden las condiciones (las creencias unido y rechazado) que anulan tanto el deseo como la intencion
        # en un deseo con mas de una intencion, las creencias que los anularan seran distintas
        async def comprobarimposible(self,creencias):
            # Es imposible cuando ha ocurrido algo que te impide hacerlo (se acabo el recurso, etc...)
            for c in creencias:
                if c.tipo == self.RECHAZADO_A_PARTIDA:
                    return True
                else:
                    return False
        
        async def comprobarsatisfecho(self,creencias):
            # En este ejemplo al ser monointención la creencia es unido_a_la_partida, sino la última intención
            for c in creencias:
                if c.tipo == self.UNIDO_A_PARTIDA:
                    return True
                else:
                    return False
        
        async def comprobarinteres(self,creencias):
            # Esto es para comprobrar que sigues teniendo ese deseo en base a la situación de la partida / tablero
            for c in creencias:
                if c.tipo == self.PEDIDO_UNIRSE:
                    return True
                else:
                    return False
        
        async def comprobaractivar(self,creencias):
            pedido = False
            tablero_conocido = False
            for c in creencias:
                if c.tipo == self.PEDIDO_UNIRSE:
                    pedido= True
                if c.tipo == self.ES_TABLERO:
                    tablero_conocido = True
            return not pedido and tablero_conocido

    async def actualizaCreencias(self,msg):
        # En este método, tendras para todos los posibles mensajes que pueda recibir el agente pues las creencias que modifica
        # Tantos deseos como protocolos
        if msg.body == "Unirme" and msg.get_metadata("performative") == "agree":
            miCreencia = self.Creencia (self.TipoCreenica.UNIDO_A_PARTIDA, self.tablero_Id)
            self.misCreencias.append(miCreencia)
        if msg.body == "Unirme" and msg.get_metadata("performative") == "refuse":
            miCreencia = self.Creencia (self.TipoCreenica.RECHAZADO_A_PARTIDA, self.tablero_Id)
            self.misCreencias.append(miCreencia)
            
    async def actualizaDeseos(self):
        for d in self.misDeseos:
            if d.activo:
                if d.comprobarimposible(self.misCreencias) or d.comprobarsatisfecho(self.misCreencias) and not d.comprobarinteres(self.misCreencias):
                    for i in d.intenciones:
                        self.misIntenciones.remove(i)
                    d.activo = False                                  
            else:
                if d.comprobaractivar(self.misCreencias):
                    self.misIntenciones.append (d.intenciones[0]) # ponemos la primera intencion del deseo en las intenciones del agente
                    d.active= True    
                    
    async def actualizaIntenciones(self):
        for i in self.misIntenciones:
            if i.comprobaralcanzada(self.misCreencias): 
                self.misIntenciones.remove(i) # quita la intencion actual de la lista de intenciones del agente
                #poner siguiente intencion del deseo en la lista de intenciones del agente                        
                self.misIntenciones.append(i.posteriores[0])
                i.posteriores.pop(0)
            if i.comprobaranulada(self.misCreencias):
                for p in i.posteriores:
                    self.misIntenciones.remove(p) # quita todas las intenciones posteriores de las intenciones del agente
                self.misIntenciones.remove(i)
                    
    async def calculaPrioridades(self):
        for i in self.misIntenciones:
            i.calculaprioridad(self.misCreencias)

    async def elige_y_ejecutaIntencion(self):
        maximaprioridad=0
        for i in self.misIntenciones:
            if i.prioridad > maximaprioridad:
                maximaprioridad = i.prioridad
                intencion_a_ejecutar = i
        intencion_a_ejecutar.ejecuta()

    # Ciclo de comportamiento de los agentes -> que hacen
    class JugadorBehav(CyclicBehaviour):
        async def run(self):
            print("Ciclo eterno del agente Jugador running")
            # recibes un mensaje o no del exterior (partida) que define tus creencias y de ahí el resto
            msg = self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                self.agent.actualizaCreencias(msg)
                self.agent.actualizaDeseos() # con las creencias cambiadas en el paso anterior
                self.agent.actualizaIntenciones() # con las creencias cambiadas en el paso primero, incluidas las intenciones añadidas en el paso anterior
                self.agent.calculaPrioridades() # de las intenciones
            self.agent.elige_y_ejecutaIntencion() # ejecuta la de mayor prioridad

    # Iniciación del propio agente
    async def setup(self):
        print("JugadorAgent started")
      # buscaria en el df al tablero
      # time.sleep(1) # le damos tiempo al tablero a registrarse en el df
      # dad = spade.DF.DfAgentDescription()
      # sd  = spade.DF.ServiceDescription()
      # sd.setName("Tablero")
      # dad.addService(sd)
      # Tablero_Id = agent.searchService (sd)
        # En idmitablero cuenta del agente tablero creado
        tablero_Id = "idmitablero" # alternativamente le asignamos el id de la cuenta de xmpp correspondiente como si ya lo conociera
        self.misCreencias =[]
        self.misIntenciones = []
        self.misDeseos = []
        miCreencia = self.Creencia(self.TipoCreencia.ES_TABLERO, tablero_Id)
        self.misCreencias.append(miCreencia)
        miDeseo = self.Jugar(self.misIntenciones, None)
        miDeseo.activo = True
        self.misDeseos.append(miDeseo)
        b = self.JugadorBehav()
        self.add_behaviour(b)

# El tablero no sigue BDI es un agente adhoc para mostrar el bdi del jugador en el protocolo unirme!!!
class TableroAgent(Agent):
    class TableroBehav(OneShotBehaviour):
        async def run(self):
            print("Ciclo unico del agente Tablero running")
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            print("primero")
            if msg:
                if msg.body == "Unirme" and msg.get_metadata("performative") == "request":
                # aqui tendria que verificar que aun acepta jugadores (mediante una creencia)
                # si los acepta, manda agree, si ya no los acepta, manda refuse
                    replymsg = Message(to=msg.sender)  # Instantiate the message
                    replymsg.set_metadata(
                        "performative", "agree" )  # Set the "agree" FIPA performative
                    replymsg.body = msg.body              # Set the message content
                    await self.send(msg)
                    print("Message sent!")                
            else:
                print("Did not received any message after 10 seconds")

    async def setup(self):
        print("TableroAgent started")
      # se registraria en el df como tablero
      # dad = spade.DF.DfAgentDescription()
      # sd = spade.DF.ServiceDescription()
      # sd.setName("Tablero")
      # dad.addService(sd)
      # dad.setAID("idmitablero") # es el id de la cuenta xmpp del tablero
      # res = myAgent.registerService (dad)      
        b = self.TableroBehav()
        self.add_behaviour(b)


if __name__ == "__main__":
    agentetablero = TableroAgent("100432074@jabbers.one", "Montaraz_2013")
    future_tablero = agentetablero.start()
    time.sleep(6)
    
    agentejugador = JugadorAgent("100432039@jabbers.one", "Nmbp12714")
    future_jugador = agentejugador.start()

    future_tablero.result()
    future_jugador.result()
    
    while agentetablero.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            agentetablero.stop()
            agentejugador.stop()
            break
    print("Agents finished")

