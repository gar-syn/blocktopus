# Twisted Imports
from twisted.internet import defer
from twisted.internet.protocol import Factory

# Package Imports
from octopus.util import now
from octopus.machine import Machine, Stream, Property
from octopus.protocol.basic import QueuedLineReceiver


#
# Serial Settings for SyrDos / LabDos
# -----------------------------------
#
# Baud rate 9600 bps
# Data bits 8         Parity       None
# Stop bits 2         Flow control None
#
# Protocol type   Raw TCP
#

class SyrDos(Machine):

    protocolFactory = Factory.forProtocol(QueuedLineReceiver)
    name = "HiTec-Zang SyrDos"

    def setup (self):

        # setup variables
        self.power = Property(title = "Power", type = str, options = ("on", "off"), setter = _set_power_s(self))
        self.target = Property(title = "Target flowrate", type = float, unit = "mL/min", setter = _set_setpoint_s(self))
        
        self.flowrate = Stream(title = "Flow rate", type = float, unit = "mL/min")
        self.pressure = Stream(title = "Pressure", type = float, unit = "bar")

    def start (self):
        def interpret_power (result: str) -> str:
            result_power = result.split(';')[1].split(' ')[1]
            if result_power == 1:
                return "on"
            elif result_power == 0:
                return "off"
        
        def interpret_flowrate (result: str) -> float:
            return int(result.split(';')[1].split(' ')[1]) / 100
        
        def interpret_pressure (result: str) -> float:
            return int(result.split(';')[1].split(' ')[1]) / 100
        
        to_monitor = []

        def addMonitor (command, fn, variable: Stream):
            def interpret (result):
                variable._push(fn(result), now())
            
            to_monitor.append(( command, interpret ))

        addMonitor("01;IN_PAR_04", interpret_power, self.power)
        addMonitor("01;IN_PV_00", interpret_flowrate, self.flowrate)
        addMonitor("01;IN_PV_05", interpret_pressure, self.pressure)

        def monitor ():
            for cmd, fn in to_monitor:
                self.protocol.write(cmd).addCallback(fn)

        self._monitor = self._tick(monitor, 1)

    def stop (self):
        if self._monitor:
            self._monitor.stop()

    def reset (self):
        return defer.succeed('OK')


def _set_power_s (machine: SyrDos):
    @defer.inlineCallbacks
    def set_power (power: str):
        power_int = 1 if power == 'on' else 0
        result = yield machine.protocol.write(
            f"01;OUT_MODE_00 {power_int}"
        )

        result_power = int(result.split(';')[1].split(' ')[1])
        if result_power != power_int:
            raise Exception(f"Could not switch {power} SyrDos power")

        machine.power._push(power)
        return 'OK'

    return set_power


def _set_setpoint_s (machine: SyrDos):
    @defer.inlineCallbacks
    def set_setpoint (setpoint: float):
        result = yield machine.protocol.write(f"01;OUT_SP_00 +{int(setpoint * 100):06d}")
        result_setpoint = int(result.split(';')[1].split(' ')[1]) / 100
        machine.target._push(result_setpoint)

        if result_setpoint != int(setpoint * 100) / 100:
            raise Exception(f"Could not set SyrDos target flowrate to {setpoint}")

        return "OK"

    return set_setpoint


class LabDos(Machine):

    protocolFactory = Factory.forProtocol(QueuedLineReceiver)
    name = "HiTec-Zang LabDos"

    def setup (self):

        # setup variables
        self.power = Property(title = "Power", type = str, options = ("on", "off"), setter = _set_power_l(self))
        self.target = Property(title = "Target speed", type = float, unit = "1/min", setter = _set_setpoint_l(self))
        
        self.speed = Stream(title = "Speed", type = float, unit = "1/min")

    def start (self):
        # def interpret_power (result: str) -> str:
        #     result_power = result.split(';')[1].split(' ')[1]
        #     if result_power == 1:
        #         return "on"
        #     elif result_power == 0:
        #         return "off"
        
        def interpret_speed (result: str) -> float:
            return int(result.split(' ')[1]) / 100
        
        to_monitor = []

        def addMonitor (command, fn, variable: Stream):
            def interpret (result):
                variable._push(fn(result), now())
            
            to_monitor.append(( command, interpret ))

        # addMonitor("01;IN_PAR_04", interpret_power, self.power)
        addMonitor("IN_PV_00", interpret_speed, self.speed)

        def monitor ():
            for cmd, fn in to_monitor:
                self.protocol.write(cmd).addCallback(fn)

        self._monitor = self._tick(monitor, 1)

    def stop (self):
        if self._monitor:
            self._monitor.stop()

    def reset (self):
        return defer.succeed('OK')


def _set_power_l (machine: LabDos):
    @defer.inlineCallbacks
    def set_power (power: str):
        power_int = 1 if power == 'on' else 0
        result = yield machine.protocol.write(
            f"OUT_MODE_00 {power_int}"
        )

        result_power = int(result.split(' ')[1])
        if result_power != power_int:
            raise Exception(f"Could not switch {power} LabDos power")

        machine.power._push(power)
        return 'OK'

    return set_power


def _set_setpoint_l (machine: LabDos):
    @defer.inlineCallbacks
    def set_setpoint (setpoint: float):
        result = yield machine.protocol.write(f"OUT_SP_00 {int(setpoint * 100):05d}")
        result_setpoint = int(result.split(';')[1].split(' ')[1]) / 100
        machine.target._push(result_setpoint)

        if result_setpoint != int(setpoint * 100) / 100:
            raise Exception(f"Could not set LabDos target speed to {setpoint}")

        return "OK"

    return set_setpoint

__all__ = ["SyrDos", "LabDos"]
