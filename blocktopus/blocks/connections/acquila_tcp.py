# from blocktopus.blocks.declarations import connection_declaration

# class connection_cgq_tcp_input (connection_declaration):
#     def eval (self):
#         from twisted.internet import defer
#         from octopus.manufacturer import aquila
#         return defer.succeed(aquila.cgq_tcp_input(
#             host = str(self.fields['HOST']),
#             port = int(self.fields['PORT']),
#             base = int(self.fields['BASE']),
#             input = int(self.fields['INPUT'])
#         ))
    
#     @staticmethod
#     def get_interface_definition ():
#         return {
#             "connInputFields": [
#                 "CGQ (TCP). Host",
#                 { "name": "HOST", "type": "string", "default": "host.docker.internal" },
#                 "Port",
#                 { "name": "PORT", "type": "integer", "default": "8082" },
#                 "Base",
#                 { "name": "BASE", "type": "integer", "default": "1" },
#                 "Input",
#                 { "name": "INPUT", "type": "integer", "default": "1" }
#             ],
#             "connOutputType": "CGQInputConnection",
#             "connTooltip": "A tcp connection to CGQ via CGQuant software proxy."
#         }