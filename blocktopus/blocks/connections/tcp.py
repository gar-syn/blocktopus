from blocktopus.blocks.declarations import connection_declaration
from twisted.internet import defer
import octopus.transport.basic

class connection_tcp (connection_declaration):
    def eval (self):
        return defer.succeed(octopus.transport.basic.tcp(
            str(self.fields['HOST']),
            int(self.fields['PORT'])
        ))

    @staticmethod
    def get_interface_definition():
        return {
            "connInputFields": [
                "TCP - ip",
                {"name": "HOST", "type": "string", "default": "192.168.1.254"},
                "port",
                {"name": "PORT", "type": "integer", "default": "100"}
            ],
            "connOutputType": "MachineConnection",
            "connTooltip": "Represents a TCP/IP (Ethernet) connection to a machine."
        }