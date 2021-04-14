from blocktopus.blocks.declarations import machine_declaration

class machine_ika_eurostar (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import ika
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

class machine_ika_rct5 (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import ika
        return ika.RCT5

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "IKA RCT 5",
            "machineDefaultName": "stirrer_hotplate",
            "machineVars": [
                { "name": "heater_power", "title": "Heater Power", "type": "String", "options": ['off', 'on'] },
                { "name": "stirrer_power", "title": "Stirrer Power", "type": "String", "options": ['off', 'on'] },
                { "name": "stirrer_setpoint", "title": "Stirrer Set Point", "type": "Number", "unit": 'rpm' },
                { "name": "heater_setpoint", "title": "Heater Set Point", "type": "Number", "unit": 'C' },
                { "name": "external_temperature", "title": "External Temp", "type": "Number", "unit": 'C', "readonly": True },
                { "name": "hotplate_temperature", "title": "Temp", "type": "Number", "unit": 'C', "readonly": True },
                { "name": "stirrer_speed", "title": "RPM", "type": "Number", "unit": 'rpm', "readonly": True },
                { "name": "viscosity", "title": "Viscosity", "type": "Number", "unit": '%', "readonly": True }
            ]
        }