from blocktopus.blocks.declarations import connection_declaration
from twisted.internet import defer

class connection_phidget (connection_declaration):
    def eval (self):
        from octopus.transport.phidgets import Phidget
        return defer.succeed(Phidget(
            int(self.fields['ID']),
        ))

    @staticmethod
    def get_interface_definition():
        return {
            "connInputFields": [
                "Phidget - ID",
                {"name": "ID", "type": "integer", "default": "0"},
            ],
            "connOutputType": "PhidgetConnection",
            "connTooltip": "Represents a Phidget device. Specify the serial ID of the phidget board."
        }
