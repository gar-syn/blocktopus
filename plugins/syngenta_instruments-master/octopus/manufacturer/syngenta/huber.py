# Twisted Imports
from twisted.internet import defer
from twisted.internet.protocol import Factory

# Package Imports
from octopus.util import now
from octopus.machine import Machine, Component, Stream, Property
from octopus.protocol.basic import QueuedLineReceiver


#
# Serial Settings for Huber CC3
# ----------------------------------------
#
# Baud rate 9600 bps
# Data bits 8         Parity       None
# Stop bits 1         Flow control None
#
# Protocol type   Raw TCP
#

class HuberCC3 (Machine):

    protocolFactory = Factory.forProtocol(QueuedLineReceiver)
    name = "Huber CC3"

    def setup (self):

        # setup variables
        self.power = Property(title = "Power", type = str, options = ("on", "off"), setter = _set_power(self))
        self.setpoint = Property(title = "Setpoint", type = int, unit = "C", setter = _set_setpoint(self))
        
        self.bath_temp = Stream(title = "Bath Temperature", type = float, unit = "C")
        self.external_temp = Stream(title = "External Temperature", type = float, unit = "C")

    def start (self):
        def interpret_power (result: str) -> str:
            if result == "ON":
                return "on"
            elif result == "OFF":
                return "off"
        
        def interpret_bath_temp (result: str) -> float:
            if (result[0:2] == "TI"):
                return int(result[3:]) / 100
        
        def interpret_external_temp (result: str) -> float:
            if (result[0:2] == "TE"):
                return int(result[3:]) / 100
    
        def interpret_setpoint (result: str) -> float:
            if (result[0:2] == "SP"):
                return int(result[3:]) / 100
        
        to_monitor = []

        def addMonitor (command, fn, variable):
            def interpret (result):
                variable._push(fn(result), now())
            
            to_monitor.append(( command, interpret ))

        addMonitor("KM?", interpret_power, self.power)
        addMonitor("TI?", interpret_bath_temp, self.bath_temp)
        addMonitor("TE?", interpret_external_temp, self.external_temp)
        addMonitor("SP?", interpret_setpoint, self.setpoint)

        def monitor ():
            for cmd, fn in to_monitor:
                self.protocol.write(cmd).addCallback(fn)

        self._monitor = self._tick(monitor, 1)

    def stop (self):
        if self._monitor:
            self._monitor.stop()

    def reset (self):
        return defer.succeed('OK')


def _set_power (machine: HuberCC3):
    @defer.inlineCallbacks
    def set_power (power: str):

        if power == "on":
            result = yield machine.protocol.write("KM_ON@")
        else:
            result = yield machine.protocol.write("KM_OFF@")

        if result != power.upper():
            raise Exception(f"Could not switch {power} Huber power")

        return "OK"

    return set_power


def _set_setpoint (machine: HuberCC3):
    def set_setpoint (setpoint: float):
        return machine.protocol.write(f"SP@ {setpoint * 100:+06d}", expectReply = False)

    return set_setpoint


__all__ = ["HuberCC3"]
