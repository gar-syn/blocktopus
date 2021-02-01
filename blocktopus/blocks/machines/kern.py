from blocktopus.blocks.declarations import machine_declaration

class machine_kern_ew (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import kern
        return kern.EWBalance

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "Kern EW",
            "machineDefaultName": "balance",
            "machineVars": [
                { "name": "weight", "title": "Weight", "type": "Number", "unit": 'g' },
                { "name": "status", "title": "Status", "type": "String", "options": [
                    "stable", "fluctuating", "error"
                ], "readonly": True },
            ]
        }