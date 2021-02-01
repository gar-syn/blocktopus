from blocktopus.blocks.declarations import machine_declaration

class machine_wpi_aladdin (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import wpi
        return wpi.Aladdin

    def getMachineParams (self):
        import json
        try:
            return {
                "syringe_diameter": int(json.loads(self.mutation)['syringe_diameter'])
            }
        except (ValueError, KeyError):
            return {}