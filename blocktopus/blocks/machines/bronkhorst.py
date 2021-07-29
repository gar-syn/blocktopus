from blocktopus.blocks.declarations import machine_declaration

class machine_bronkhorst_elpress (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import bronkhorst
        return bronkhorst.ElPress

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "Bronkhorst EL-PRESS",
            "machineDefaultName": "valve",
            "machineVars": [
                { "name": "power", "title": "Power", "type": "String", "options": ['off', 'on'] },
                { "name": "percentage_setpoint", "title": "Valve Percentage Setpoint", "type": "Number", "unit": "%" },
                { "name": "pressure_setpoint", "title": "Pressure Setpoint", "type": "Number", "unit": "bar" },
                { "name": "percentage_pressure", "title": "Valve Percentage", "type": "Number", "unit": "%", "readonly": True },
                { "name": "pressure", "title": "Pressure", "type": "Number", "unit": "bar", "readonly": True },
            ]
        }