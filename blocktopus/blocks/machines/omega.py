from blocktopus.blocks.declarations import machine_declaration

class machine_omega_hh306a (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import omega
        return omega.HH306A

class machine_omega_rdxl4sd (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import omega
        return omega.RDXL4SD

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "Omega RDXL4SD",
            "machineDefaultName": "thermocouple",
            "machineVars": [
                { "name": "temp1", "title": "Temperature 1", "type": "Number", "unit": "C", "readonly": True },
                { "name": "temp2", "title": "Temperature 2", "type": "Number", "unit": "C", "readonly": True },
                { "name": "temp3", "title": "Temperature 3", "type": "Number", "unit": "C", "readonly": True },
                { "name": "temp4", "title": "Temperature 4", "type": "Number", "unit": "C", "readonly": True }
            ]
        }