from blocktopus.blocks.declarations import connection_declaration
from twisted.internet import defer
import octopus.transport.basic

class connection_serial (connection_declaration):
    def eval (self):
        return defer.succeed(octopus.transport.basic.serial(
            str(self.fields['PORT']),
            baudrate = int(self.fields['BAUD'])
        ))

    @staticmethod
    def get_interface_definition():
        return {
            "connInputFields": [
                "Serial - port",
                {"name": "PORT", "type": "string", "default": "/dev/ttyS0"},
                "baudrate",
                {"name": "BAUD", "type": "integer", "default": "19200"}
            ],
            "connOutputType": "MachineConnection",
            "connTooltip": "Represents a Direct serial (RS-232) connection to a machine."
        }
