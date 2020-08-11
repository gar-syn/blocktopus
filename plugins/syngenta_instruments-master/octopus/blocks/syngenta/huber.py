from octopus.blocktopus.blocks.machines import machine_declaration

class machine_huber_cc3 (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer.syngenta import huber
        return huber.HuberCC3

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "Huber CC3",
            "machineDefaultName": "thermostat",
            "machineVars": [
                { "name": "power", "title": "Power", "type": "String", "options": ['off', 'on'] },
                { "name": "setpoint", "title": "Set Point", "type": "Number", "unit": 'C' },
                { "name": "bath_temp", "title": "Bath Temp", "type": "Number", "unit": 'C', "readonly": True },
                { "name": "external_temp", "title": "External Temp", "type": "Number", "unit": 'C', "readonly": True }
            ]
        }