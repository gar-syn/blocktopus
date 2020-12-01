from octopus.blocktopus.blocks.machines import machine_declaration, connection_declaration

class machine_aquila_gcq (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer.syngenta import aquila
        return aquila.CGQ

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "Aquila CGQ",
            "machineDefaultName": "bioreactor",
            "machineConnectionType": "CGQInputConnection",
            "machineVars": [
                { "name": "backscatter", "title": "Backscatter", "type": "Number", "unit": 'au', "readonly": True },
                { "name": "temperature", "title": "Temperature", "type": "Number", "unit": 'C', "readonly": True },
                { "name": "shakingspeed", "title": "Shaking speed", "type": "Number", "unit": 'rpm', "readonly": True },
                { "name": "growthrate", "title": "Growth rate", "type": "Number", "unit": '1/h', "readonly": True }
            ]
        }


# class connection_cgq_pipe_input (connection_declaration):
#     def eval (self):
#         from twisted.internet import defer
#         from octopus.manufacturer.syngenta import aquila
#         return defer.succeed(aquila.cgq_pipe_input(
#             base = int(self.fields['BASE']),
#             input = int(self.fields['INPUT'])
#         ))
    
#     @staticmethod
#     def get_interface_definition ():
#         return {
#             "connInputFields": [
#                 "CGQ (Named Pipe). Base",
#                 { "name": "BASE", "type": "integer", "default": "1" },
#                 "Input",
#                 { "name": "INPUT", "type": "integer", "default": "1" }
#             ],
#             "connOutputType": "CGQInputConnection",
#             "connTooltip": "A named pipe connection to CGQ via CGQuant software."
#         }


class connection_cgq_tcp_input (connection_declaration):
    def eval (self):
        from twisted.internet import defer
        from octopus.manufacturer.syngenta import aquila
        return defer.succeed(aquila.cgq_tcp_input(
            host = str(self.fields['HOST']),
            port = int(self.fields['PORT']),
            base = int(self.fields['BASE']),
            input = int(self.fields['INPUT'])
        ))
    
    @staticmethod
    def get_interface_definition ():
        return {
            "connInputFields": [
                "CGQ (TCP). Host",
                { "name": "HOST", "type": "string", "default": "host.docker.internal" },
                "Port",
                { "name": "PORT", "type": "integer", "default": "8082" },
                "Base",
                { "name": "BASE", "type": "integer", "default": "1" },
                "Input",
                { "name": "INPUT", "type": "integer", "default": "1" }
            ],
            "connOutputType": "CGQInputConnection",
            "connTooltip": "A tcp connection to CGQ via CGQuant software proxy."
        }