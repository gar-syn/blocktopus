from blocktopus.blocks.declarations import machine_declaration

class machine_julabo_f25 (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import julabo
        return julabo.JulaboF25

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "Julabo F25",
            "machineDefaultName": "thermostat",
            "machineVars": [
                { "name": "power", "title": "Power", "type": "String", "options": ['off', 'on'] },
                { "name": "setpoint_1", "title": "Set Point 1", "type": "Number", "unit": 'C' },
                { "name": "bath_temp", "title": "Bath Temp", "type": "Number", "unit": 'C', "readonly": True },
                { "name": "external_temp", "title": "External Temp", "type": "Number", "unit": 'C', "readonly": True }
            ]
        }