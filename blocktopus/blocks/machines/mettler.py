from blocktopus.blocks.declarations import machine_declaration

class machine_mt_icir (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import mt
        return mt.ICIR

    def getMachineParams (self):
        import json
        try:
            return {
                "stream_names": json.loads(self.mutation)['stream_names']
            }
        except (ValueError, KeyError):
            return {}

class machine_mt_sics_balance (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import mt
        return mt.SICSBalance

    @staticmethod
    def get_interface_definition():
        return {
            "machineTitle": "MT Balance (SICS)",
            "machineDefaultName": "balance",
            "machineVars": [
                {"name": "status", "title": "Status", "type": "String", "readonly": True},
                {"name": "weight", "title": "Weight", "type": "Number", "readonly": True}
            ]
        }