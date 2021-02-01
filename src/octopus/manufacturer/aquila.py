# Zope Imports
from zope.interface import implementer

# Twisted Imports
from twisted.internet import reactor, defer, abstract
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.protocols.basic import LineOnlyReceiver
from twisted.python.util import FancyEqMixin

# System Imports
from time import time as now
from typing import Literal
from collections import namedtuple

# Package Imports
from octopus.machine import Machine, Property, Stream

__all__ = ["CGQ"]

CGQUANT_DATA_PIPE = '\\\\.\\pipe\\CGQuantDataPipe'

#
# Transports have a connect() function, taking a protocolFactory
# object as the single argument. This should return an IProtocol
# object or equivalent (or a deferred).
#

@implementer(IAddress)
class NamedPipeAddress (FancyEqMixin, object):
    """
    Object representing a Windows Named Pipe endpoint.
    @ivar name: The name of the pipe.
    @type name: C{str}
    """

    compareAttributes = ('name', )

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'NamedPipeAddress({self.name!s})'

    def __hash__(self):
        if self.name is None:
            return hash((self.__class__, None))
        else:
            return hash(self.name)


@implementer(IAddress)
class CGQInputAddress (FancyEqMixin, object):
    """
    Object representing a CGQ Base Input endpoint.
    @ivar base: The CGQ base.
    @type base: C{int}
    @ivar input: The input number on the base.
    @type input: C{int}
    """

    compareAttributes = ('base', 'input')

    def __init__(self, base: int, input: int):
        self.base = base
        self.input = input

    def __repr__(self):
        return f'CGQInputAddress({self.base}, {self.input})'

    def __hash__(self):
        if self.base is None and self.input is None:
            return hash((self.__class__, None))
        else:
            return hash((self.base, self.input))
    

# class SelectableFile (abstract.FileDescriptor):
#     def __init__ (self, fp, protocol: Protocol):
#         self.fp = fp
#         fdesc.setNonBlocking(fp)
#         self.protocol = protocol
#         self.protocol.makeConnection(transport = self)
#         self.fileno = self.fp.fileno

#     def doRead (self):
#         buf = self.fp.read(256)
#         if buf:
#             self.protocol.dataReceived(buf)
#         else:
#             self.protocol.connectionLost()

#     def write (self, data):
#         pass # what can we do with the data?

#     def loseConnection (self):
#         self.fp.close()


CGQuantDataPacket = namedtuple('CGQuantDataPacket', ['time', 'base', 'input', 'experimenttime', 'backscatter', 'temperature', 'shakingspeed', 'growthrate'])


# class CGQuantSingleInputReceiver (Protocol):
#     def __init__ (self, addr: CGQInputAddress):
#         self.connection_name = "disconnected"
#         self.addr = addr
#         self.on_data = None

#     def packetReceived (packet: CGQuantDataPacket):
#         if not (packet.base == self.addr.base and packet.input == self.addr.input):
#             return

#         if self.on_data is not None:
#             self.on_data(packet)

class CGQuantLineReceiver (LineOnlyReceiver):
    delimiter = b'\n'

    def __init__ (self):
        self.listener = None
    
    def setListener (self, listener):
        self.listener = listener
    
    def setBaseInput (self, base_no: int, input_no: int):
        self.base = base_no
        self.input = input_no

    def lineReceived (self, line: bytes):
        # line: '2020-10-08 20:12:17\tBase=0\tInputNo=0\tExperimentTime[s]=23\tBackscatter[au]=374.232\tTemperature[Â°C]=30.08\tShakingSpeed[rpm]=248.18\tGrowthRate[1/h]=-0.02615\n'
        parts = [p.split('=')[-1] for p in line.decode('utf-8').strip().split('\t')]

        if len(parts) != 8:
            print (f"Incomplete packet received from CGQuant: {line.decode('utf-8')!r}")
            return

        packet = CGQuantDataPacket(
            time = parts[0],
            base = int(parts[1]),
            input = int(parts[2]),
            experimenttime = float(parts[3]),
            backscatter = float(parts[4]),
            temperature = float(parts[5]),
            shakingspeed = float(parts[6]),
            growthrate = float(parts[7])
        )

        if not (packet.base == self.base and packet.input == self.input):
            return

        print ('CGQ packet', packet)

        if self.listener is not None:
            self.listener(packet)

# class CGQuantDataPipeLineReceiver (LineOnlyReceiver):
#     delimiter = b'\n'

#     def __init__ (self):
#         self.listeners = []

#     def lineReceived (self, line: bytes):
#         # line: '2020-10-08 20:12:17\tBase=0\tInputNo=0\tExperimentTime[s]=23\tBackscatter[au]=374.232\tTemperature[Â°C]=30.08\tShakingSpeed[rpm]=248.18\tGrowthRate[1/h]=-0.02615\n'
#         parts = [p.split('=')[-1] for p in line.decode('ascii').strip().split('\t')]

#         if len(parts) != 8:
#             print (f"Incomplete packet received from CGQuant: {line.decode('ascii')!r}")
#             return

#         packet = CGQuantDataPacket(
#             time = parts[0],
#             base = int(parts[1]),
#             input = int(parts[2]),
#             experimenttime = float(parts[3]),
#             backscatter = float(parts[4]),
#             temperature = float(parts[5]),
#             shakingspeed = float(parts[6]),
#             growthrate = float(parts[7])
#         )

#         print ('CGQ packet', packet)

#         for protocol in self.listeners:
#             try:
#                 protocol.packetReceived(packet)
#             except AttributeError:
#                 print('Listener does not have a packetReceived method.')
    
#     def addListener (self, protocol: CGQuantSingleInputReceiver):
#         print('Adding a listener to the CGQuantDataPipeLineReceiver.')
#         if protocol not in self.listeners:
#             self.listeners.append(protocol)


# class CGQuantInputFactory (Factory):
#     protocol = CGQuantSingleInputReceiver
    
#     def __init__ (self):
#         self._reader_protocol = None
#         # self._reader_protocol_listeners = []

#     # def startFactory (self):
#     def _start (self):
#         print('CGQuantInputFactory _start')
#         self._reader_protocol = CGQuantDataPipeLineReceiver()
#         self._reader = SelectableFile(fp = open(CGQUANT_DATA_PIPE, 'r'), protocol = self._reader_protocol)
#         reactor.addReader(self._reader)

#         # for p in self._reader_protocol_listeners:
#         #     self._reader_protocol.addListener(p)

#     # def stopFactory (self):
#     def __del__ (self):
#         print ('CGQuantInputFactory __del__')
#         reactor.removeReader(self._reader)
#         self._reader = None

#     def buildProtocol (self, addr):
#         if self._reader_protocol is None:
#             self._start()
            
#         p = self.protocol(addr)
#         p.factory = self

#         # if self._reader_protocol is not None:
#         self._reader_protocol.addListener(p)
#         # else:
#             # self._reader_protocol_listeners.append(p)

#         return p

class _SetBaseInputFactory (Factory):
    def __init__ (self, factory: Factory, base: int, input: int):
        self.base = base
        self.input = input
        self.factory = factory

    def buildProtocol (self, addr):
        # addr = CGQInputAddress(self.base, self.input)
        p = self.factory.buildProtocol(addr)
        p.setBaseInput(self.base, self.input)

        return p


class cgq_pipe_input (object):
    # _factory = CGQuantInputFactory
    _data_pipe = None

    def __init__ (self, base: int, input: int):
        self.base = base
        self.input = input
        self.name = f"cgq_pipe_input({base:d}, {input:d})"

    def connect (self, factory):
        addr = CGQInputAddress(self.base, self.input)
        protocol = _SetBaseInputFactory(factory, self.base, self.input).buildProtocol(addr)

        # self._serial = self._factory(protocol, self.port, reactor, self.baudrate, **self._args)

        return protocol


class cgq_tcp_input (object):
    def __init__ (self, host: str, port: int, base: int, input: int):
        self.host = host
        self.port = port
        self.base = base
        self.input = input
        self.name = f"cgq_tcp_input({host!s}, {port:d}, {base:d}, {input:d})"

        self.point = TCP4ClientEndpoint(reactor, host, port)

    def connect (self, factory):
        return self.point.connect(_SetBaseInputFactory(factory, self.base, self.input))

    # def connect(self, protocolFactory):
    #     """
    #     Implement L{IStreamClientEndpoint.connect} to connect via TCP.
    #     """
    #     try:
    #         wf = _WrappingFactory(protocolFactory)
    #         self._reactor.connectTCP(
    #             self._host, self._port, wf,
    #             timeout=self._timeout, bindAddress=self._bindAddress)
    #         return wf._onConnection
    #     except:
    #         return defer.fail()

    # def connect (self, factory):
    #   protocol = factory.buildProtocol(addr)

    #   # self._serial = self._factory(protocol, self.port, reactor, self.baudrate, **self._args)

    #   return protocol


class CGQ (Machine):
    """
    Control class for a Aquila CGQ, via the CGQuant software.
    The software connects via a Named Pipe at \\.\pipe\CGQuantDataPipe
    """

    protocolFactory = Factory.forProtocol(CGQuantLineReceiver)
    name = "CGQuant"

    def setup (self):

        # setup variables
        self.backscatter = Stream(title = "Backscatter", type = float, unit = "au")
        self.temperature = Stream(title = "Temperature", type = float, unit = "C")
        self.shakingspeed = Stream(title = "Shaking speed", type = float, unit = "rpm")
        self.growthrate = Stream(title = "Growth rate", type = float, unit = "1/h")

    def start (self):
        def receive_packet (packet: CGQuantDataPacket):
            self.backscatter._push(packet.backscatter)
            self.temperature._push(packet.temperature)
            self.shakingspeed._push(packet.shakingspeed)
            self.growthrate._push(packet.growthrate)

        self.protocol.setListener(receive_packet)

    def stop (self):
        self.protocol.setListener(None)