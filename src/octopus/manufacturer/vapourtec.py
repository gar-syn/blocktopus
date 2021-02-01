# Twisted Imports
from twisted.internet import defer
from twisted.internet.protocol import Factory

# Package Imports
from octopus.machine import Machine, Component, Stream, Property, ui
from octopus.util import now
from octopus.protocol.basic import QueuedLineReceiver
from octopus.transport.gsioc import Slave as GSIOCSlave
from octopus.protocol.gsioc import NoDevice as GSIOCNoDevice


__all__ = ["R2R4"]


class R2ProtocolFactory (Factory):
    protocol = QueuedLineReceiver


class R2Pump (Component):
    def __init__ (self, title, set_target, set_input):
        self.title = title

        self.target   = Property(title = self.title + " Target Flow Rate", type = int, unit = "uL/min", min = 0, max = 99999, setter = set_target)
        self.input    = Property(title = self.title + " Input", type = str, options = ("solvent", "reagent"), setter = set_input)
        self.rate     = Stream(title = self.title + " Flow Rate", type = int, unit = "uL/min")
        self.pressure = Stream(title = self.title + " Pressure", type = int, unit = "mbar")
        self.airlock  = Stream(title = self.title + " Airlock", type = int)


class R4Heater (Component):
    def __init__ (self, title, set_target):
        self.title = title

        self.target = Property(title = self.title + " Target Temperature", type = int, unit = "C", min = -1000, max = 250, setter = set_target)
        self.mode   = Property(title = self.title + " Mode", type = str)
        self.power  = Stream(title = self.title + " Power", type = int, unit = "W")
        self.temp   = Stream(title = self.title + " Temperature", type = float, unit = "C")


def _set_power (machine):
    def set_power (power):
        if power == "on":
            return machine.protocol.write("PN")
        else:
            return machine.protocol.write("PF")

    return set_power

def _set_pump_target (machine, id):
    def set_target (rate):
        return machine.protocol.write("FR %u %u" % (id, rate))

    return set_target

def _set_pump_input (machine, id):
    base = id * 2
    def set_input (input):
        return machine.protocol.write("KP %u" % (base + (1 if (input == "reagent") else 0)))

    return set_input

def _set_loop (machine, id):
    base = id * 2
    def set_loop (pos):
        return machine.protocol.write("KP %u" % (base + (5 if (pos == "inject") else 4)))

    return set_loop

def _set_output (machine):
    def set_output (pos):
        return machine.protocol.write("KP %u" % (9 if (pos == "collect") else 8))

    return set_output

def _set_pressure_limit (machine):
    def set_pressure_limit (limit):
        return machine.protocol.write("PL %u" % int(limit / 10))

    return set_pressure_limit

def _set_heater_target (machine, id):
    def set_target (temp):
        return machine.protocol.write("R4 ST %u %u" % (id, temp))

    return set_target


class R2R4 (Machine):

    title = "Vapourtec R2+/R4"
    protocolFactory = R2ProtocolFactory()

    def setup (self, **kwargs):

        # setup variables
        self.status = Property(title = "Status", type = str)
        self.power  = Property(title = "System Power", type = str, options = ("on", "off"), setter = _set_power(self))
        self.pressure = Stream(title = "System Pressure", type = int, unit = "mbar")
        self.pressure_limit = Property(title = "System Pressure Limit", type = int, unit = "mbar", min = 1000, max = 50000, setter = _set_pressure_limit(self))
        self.output = Property(title = "Output", type = str, options = ("waste", "collect"), setter = _set_output(self))

        self.pump1 = R2Pump("Pump A", _set_pump_target(self, 0), _set_pump_input(self, 0))
        self.pump2 = R2Pump("Pump B", _set_pump_target(self, 1), _set_pump_input(self, 1))

        self.loop1 = Property(title = "Loop A Position", type = str, options = ("load", "inject"), setter = _set_loop(self, 0))
        self.loop2 = Property(title = "Loop B Position", type = str, options = ("load", "inject"), setter = _set_loop(self, 1))

        self.heater1 = R4Heater("Heater A", _set_heater_target(self, 0))
        self.heater2 = R4Heater("Heater B", _set_heater_target(self, 1))
        self.heater3 = R4Heater("Heater C", _set_heater_target(self, 2))
        self.heater4 = R4Heater("Heater D", _set_heater_target(self, 3))

        self.ui = ui(
            traces = [{
                "title": "Pressure",
                "unit":  self.pressure.unit,
                "traces": [self.pressure, self.pump1.pressure, self.pump2.pressure],
                "colours": ["#0c4", "#F70", "#50a"]
            }, {
                "title": "Temperature",
                "unit":  self.heater1.temp.unit,
                "traces": [self.heater1.temp, self.heater2.temp, self.heater3.temp, self.heater4.temp],
                "colours": ["#0c4", "#F70", "#50a", "#921"]
            }],
            properties = [
                self.pressure,
                self.pump1.pressure,
                self.pump2.pressure,
                self.pump1.rate,
                self.pump2.rate,
                self.pump1.input,
                self.pump2.input,
                self.heater1.temp,
                self.heater2.temp,
                self.heater3.temp,
                self.heater4.temp
            ]
        )

    def gsioc (self, id):
        d = defer.Deferred()

        def interpret (response):
            if response[:13] == 'GSIOC reply: ':
                return response[13:]

            if response == 'GSIOC command failed' or response == 'GSIOC timed out':
                raise GSIOCNoDevice(id)

            if response == 'GSIOC command OK':
                return True

        def immediate_command (line):
            return self.protocol.write(
                    "TG i %d %s" % (id, line)
                ).addCallback(interpret)

        def buffered_command (line):
            return self.protocol.write(
                    "TG b %d %s" % (id, line)
                ).addCallback(interpret)

        def r (result):
            d.callback(GSIOCSlave(
                immediate_command,
                buffered_command,
                name = "%s(GSIOC:%s)" % (
                    self.protocol.connection_name, id
                )
            ))
            return result

        self.ready.addCallback(r)
        return d

    def start (self):
        # setup monitor on a tick to update variables

        self._timeZero = now() # in seconds

        def handleClearHistory (result):
            if result == 'OK':
                self._timeZero = now()

        def clearHistory ():
            return self.protocol.write("HR").addCallback(handleClearHistory)

        heaterMode = {
            "U": "off",
            "C": "cooling",
            "H": "heating",
            "S": "stable unheated",
            "F": "stable heated"
        }

        status = (
            "off", "running",
            "system overpressure",
            "pump 1 overpressure", "pump 2 overpressure",
            "system underpressure",
            "pump 1 underpressure", "pump 2 underpressure"
        )

        def heaterTemp (input):
            if input == "-1000":
                return 0
            else:
                return float(input) / 10

        def interpretPressure (result, sendTime):
            if result == "OK":
                return

            result = [x.split(",") for x in result.split("&")]

            # Compensate for difference between clocks.
            #
            # Expect the last time returned to have some delay:
            #   At least 0.1s (frequency of collection)
            #   + 1/2 round-trip communication time
            #
            # Any other difference is due to slow/fast clock,
            # which can be re-zeroed from time to time.
            #
            # Algorithm:
            #   lastTime = self._timeZero + (float(result[-1][0]) / 10)
            #   roundTripTime = now() - sendTime
            #   expectedDiff = 0.1 + (roundTripTime / 2)
            #   timeDiff = (lastTime - now()) - expectedDiff

            timeDiff = self._timeZero + (float(result[-1][0]) * 0.1) - 0.1 - (now() * 1.5) + (sendTime * 0.5)

            if timeDiff < -0.05:
                self._timeZero -= timeDiff

            for v in result:
                if len(v) < 4:
                    return

                time = self._timeZero + (float(v[0]) / 10)
                self.pressure._push(int(v[1]) * 10, time)
                self.pump1.pressure._push(int(v[2]) * 10, time)
                self.pump2.pressure._push(int(v[3]) * 10, time)

        def interpretHistory (result):
            if result == "OK":
                return


            for type, parts in [x.split("{") for x in result[:-1].split("}")]:
                data = [x.split(",") for x in parts.split("&")]

                if type == "T":
                    for v in data:
                        if len(v) < 9:
                            continue

                        time = self._timeZero + (float(v[0]) / 10)
                        self.heater1.mode._push(heaterMode[v[1]], time)
                        self.heater1.temp._push(heaterTemp(v[2]), time)
                        self.heater2.mode._push(heaterMode[v[3]], time)
                        self.heater2.temp._push(heaterTemp(v[4]), time)
                        self.heater3.mode._push(heaterMode[v[5]], time)
                        self.heater3.temp._push(heaterTemp(v[6]), time)
                        self.heater4.mode._push(heaterMode[v[7]], time)
                        self.heater4.temp._push(heaterTemp(v[8]), time)

                if type == "W":
                    for v in data:
                        if len(v) < 5:
                            continue

                        time = self._timeZero + (float(v[0]) / 10)
                        self.heater1.power._push(int(v[1]), time)
                        self.heater2.power._push(int(v[2]), time)
                        self.heater3.power._push(int(v[3]), time)
                        self.heater4.power._push(int(v[4]), time)

                if type == "F":
                    for v in data:
                        if len(v) < 3:
                            continue

                        time = self._timeZero + (float(v[0]) / 10)
                        self.pump1.rate._push(int(v[1]), time)
                        self.pump2.rate._push(int(v[2]), time)

                if type == "V":
                    for v in data:
                        if len(v) < 2:
                            continue

                        time = self._timeZero + (float(v[0]) / 10)
                        v = int(v[1])

                        self.pump1.input._push("reagent" if v & 1 else "solvent", time)
                        self.pump2.input._push("reagent" if v & 2 else "solvent", time)
                        self.loop1._push("inject" if v & 4 else "load", time)
                        self.loop2._push("inject" if v & 8 else "load", time)
                        self.output._push("collect" if v & 16 else "waste", time)

            # Reset the R2's internal clock before it runs out
            # of numbers for timing (v[0] ~ 2**15 ?)
            if now() > self._timeZero + 2500:
                clearHistory()

        def interpretStatus (result):
            v = result.split(" ")

            if len(v) < 11:
                return

            time = now()

            self.power._push("on" if v[0] == "1" else "off", time)
            self.status._push(status[int(v[0])], time)
            self.pump1.target._push(int(v[1]), time)
            self.pump2.target._push(int(v[2]), time)
            self.pump1.airlock._push(int(v[3]), time)
            self.pump2.airlock._push(int(v[4]), time)
            self.pressure_limit._push(float(v[5]) / 100, time)
            self.heater1.target._push(int(v[7]), time)
            self.heater2.target._push(int(v[8]), time)
            self.heater3.target._push(int(v[9]), time)
            self.heater4.target._push(int(v[10]), time)

        def monitorPressure ():
            self.protocol.write("HP").addCallback(interpretPressure, now())

        def monitorStatus ():
            self.protocol.write("HH").addCallback(interpretHistory)
            self.protocol.write("GA").addCallback(interpretStatus)

        def startMonitors (result):
            self._tick(monitorPressure, 0.1)
            self._tick(monitorStatus, 1)

        clearHistory().addCallback(startMonitors)

    def stop (self):
        self._stopTicks()

    def reset (self):
        return defer.gatherResults([
            self.power.set("off"),
            self.pressure_limit.set(15000),
            self.output.set("waste"),
            self.loop1.set("load"),
            self.loop2.set("load"),
            self.pump1.input.set("solvent"),
            self.pump2.input.set("solvent"),
            self.pump1.target.set(0),
            self.pump2.target.set(0),
            self.heater1.target.set(-1000),
            self.heater2.target.set(-1000),
            self.heater3.target.set(-1000),
            self.heater4.target.set(-1000)
        ])

    def pause (self):
        self._pauseState = self.power.value
        return self.power.set("off")

    def resume (self):
        return self.power.set(self._pauseState)
