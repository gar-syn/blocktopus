# Twisted Imports
from twisted.internet import defer
from twisted.internet.protocol import Factory

# Package Imports
from octopus.util import now
from octopus.machine import Machine, Stream, Property
from octopus.protocol.basic import QueuedLineReceiver


#
# Serial Settings for IKA Eurostar
# --------------------------------
#
# Baud rate 9600 bps
# Data bits 7         Parity       Even
# Stop bits 1         Flow control None
#
# Protocol type   Raw TCP
#

class IKALineReceiver (QueuedLineReceiver):
    delimiter = b" \r \n"


class IKAEurostar (Machine):

    protocolFactory = Factory.forProtocol(IKALineReceiver)
    name = "IKA Eurostar"

    def setup (self):

        # setup variables
        self.power = Property(title = "Power", type = str, options = ("on", "off"), setter = _set_power(self))
        self.setpoint = Property(title = "Stirrer setpoint", type = float, unit = "rpm", setter = _set_setpoint(self))
        
        self.rpm = Stream(title = "Stirrer Speed", type = float, unit = "rpm")
        self.torque = Stream(title = "Torque", type = float, unit = "Ncm")

    def start (self):
        # def interpret_power (result: str) -> str:
        #     if result == "ON":
        #         return "on"
        #     elif result == "OFF":
        #         return "off"
        
        def interpret_rpm (result: str) -> float:
            value, id = result.split(' ')
            if (id == "4"):
                return float(value)
        
        def interpret_torque (result: str) -> float:
            value, id = result.split(' ')
            if (id == "5"):
                return float(value)
    
        def interpret_setpoint (result: str) -> float:
            value, id = result.split(' ')
            if (id == "4"):
                return float(value)
        
        to_monitor = []

        def addMonitor (command, fn, variable: Stream):
            def interpret (result):
                variable._push(fn(result), now())
            
            to_monitor.append(( command, interpret ))

        # addMonitor("KM?", interpret_power, self.power)
        addMonitor("IN_PV_4", interpret_rpm, self.rpm)
        addMonitor("IN_PV_5", interpret_torque, self.torque)
        addMonitor("IN_SP_4", interpret_setpoint, self.setpoint)

        def monitor ():
            for cmd, fn in to_monitor:
                self.protocol.write(cmd).addCallback(fn)

        self._monitor = self._tick(monitor, 1)

    def stop (self):
        if self._monitor:
            self._monitor.stop()

    def reset (self):
        return defer.succeed('OK')


def _set_power (machine: IKAEurostar):
    @defer.inlineCallbacks
    def set_power (power: str):
        if power == "on":
            yield machine.protocol.write("START_4", expectReply = False)
        else:
            yield machine.protocol.write("STOP_4", expectReply = False)
        
        machine.power._push(power)

    return set_power


def _set_setpoint (machine: IKAEurostar):
    def set_setpoint (setpoint: float):
        return machine.protocol.write(f"OUT_SP_4 {setpoint:.1f}", expectReply = False)

    return set_setpoint


__all__ = ["IKAEurostar"]
