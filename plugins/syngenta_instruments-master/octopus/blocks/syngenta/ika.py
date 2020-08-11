from octopus.blocktopus.blocks.machines import machine_declaration

class machine_ika_eurostar (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer.syngenta import ika
        return ika.IKAEurostar

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "IKA Eurostar",
            "machineDefaultName": "stirrer",
            "machineVars": [
                { "name": "power", "title": "Power", "type": "String", "options": ['off', 'on'] },
                { "name": "setpoint", "title": "Set Point", "type": "Number", "unit": 'rpm' },
                { "name": "rpm", "title": "RPM", "type": "Number", "unit": 'rpm', "readonly": True },
                { "name": "torque", "title": "Torque", "type": "Number", "unit": 'Ncm', "readonly": True }
            ]
        }