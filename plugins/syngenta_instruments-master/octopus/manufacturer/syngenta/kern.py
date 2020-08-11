# Twisted Imports
from twisted.internet import defer
from twisted.internet.protocol import Factory

# Package Imports
from octopus.machine import Machine, Stream, Property
from octopus.protocol.basic import QueuedLineReceiver

__all__ = ["EWBalance"]


class EWBalance (Machine):

    protocolFactory = Factory.forProtocol(QueuedLineReceiver)
    name = "Kern EW Balance"

    def setup (self):

        # setup variables
        self.weight = Stream(title = "Weight", type = float, unit = "g")
        self.status = Property(title = "Status", type = "str")

    def start (self):
        def interpret_weight (result: str):
            result_state = result[-1]
            # result_type = result[-2]
            result_unit = result[-4:2]

            if result_state == "E":
                self.status._push("error")
                return
            elif result_state == "S":
                self.status._push("stable")
            elif result_state == "U":
                self.status._push("fluctuating")

            # result_type != "G" --> out of range.
            
            if result_unit != " G":
                raise Exception("Balance units should be set to grams.")

            result_value = float(result[:-5])

            self.weight._push(result_value)

        def monitor_weight ():
            self.protocol.write("O8").addCallback(interpret_weight)

        self._tick(monitor_weight, 1)

    def stop (self):
        self._stopTicks()

    def reset (self):
        return defer.succeed('OK')

    def tare (self):
        return self.protocol.write("T ", expectReply = False, wait = 5)
