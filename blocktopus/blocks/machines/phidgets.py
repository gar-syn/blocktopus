from blocktopus.blocks.declarations import machine_declaration

class machine_phidgets_phsensor (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import phidgets
        return phidgets.PHSensor

    def getMachineParams (self):
        import json
        try:
            return {
                "min_change": float(json.loads(self.mutation)['min_change'])
            }
        except (ValueError, KeyError):
            return {}