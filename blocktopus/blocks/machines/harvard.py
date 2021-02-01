from blocktopus.blocks.declarations import machine_declaration

class machine_harvard_phd2000 (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import harvard
        return harvard.PHD2000Infuser

    def getMachineParams (self):
        import json
        try:
            return {
                "syringe_diameter": int(json.loads(self.mutation)['syringe_diameter'])
            }
        except (ValueError, KeyError):
            return {}