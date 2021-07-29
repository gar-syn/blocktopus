from blocktopus.blocks.declarations import machine_declaration

class machine_sartorious_balance (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import sartorious
        return sartorious.Sartorious

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "Sartorious Balance",
            "machineDefaultName": "balance",
            "machineVars": [
                { "name": "weight", "title": "Weight", "type": "Number", "unit": 'g' },
            ]
        }