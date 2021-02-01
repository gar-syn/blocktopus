# Twisted Imports
from twisted.internet import defer
from twisted.internet.protocol import Factory

# Package Imports
from octopus.util import now
from octopus.machine import Machine, Stream, Property
from octopus.protocol.basic import QueuedLineReceiver


#
# Serial Settings for JulaboF25
# --------------------------------
#
# Baud rate 4800 bps
# Data bits 7         Parity       Even
# Stop bits 1         Flow control None
#
# Protocol type   Raw TCP
#

class JulaboF25 (Machine):

    protocolFactory = Factory.forProtocol(QueuedLineReceiver)
    name = "Julabo F25"

    def setup (self):

        # setup variables
        self.power = Property(title = "Power", type = str, options = ("on", "off"), setter = _set_power(self))
        self.setpoint_1 = Property(title = "Setpoint 1", type = float, unit = "C", setter = _set_setpoint(self))
        
        self.bath_temp = Stream(title = "Bath Temperature", type = float, unit = "C")
        self.external_temp = Stream(title = "External Temperature", type = float, unit = "C")

    def start (self):
        def interpret_power (result: str) -> str:
            if result == "1":
                return "on"
            elif result == "0":
                return "off"
        
        to_monitor = []

        def addMonitor (command, fn, variable: Stream):
            def interpret (result):
                variable._push(fn(result), now())
            
            to_monitor.append(( command, interpret ))

        addMonitor("IN_MODE_05", interpret_power, self.power)
        addMonitor("IN_PV_00", float, self.bath_temp)
        addMonitor("IN_PV_02", float, self.external_temp)
        addMonitor("IN_SP_00", float, self.setpoint_1)

        def monitor ():
            for cmd, fn in to_monitor:
                self.protocol.write(cmd).addCallback(fn)

        self._monitor = self._tick(monitor, 1)

    def stop (self):
        if self._monitor:
            self._monitor.stop()

    def reset (self):
        return defer.succeed('OK')


def _set_power (machine: JulaboF25):
    def set_power (power: str):
        return machine.protocol.write(
            f"OUT_MODE_05 {1 if power == 'on' else 0}", 
            expectReply = False, 
            wait = 0.25
        )

    return set_power


def _set_setpoint (machine: JulaboF25):
    def set_setpoint (setpoint: float):
        return machine.protocol.write(f"OUT_SP_00 {setpoint:.1f}", expectReply = False)

    return set_setpoint


__all__ = ["JulaboF25"]
