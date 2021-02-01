from blocktopus.blocks.declarations import machine_declaration

class machine_knauer_K120 (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import knauer
        return knauer.K120


class machine_knauer_S100 (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import knauer
        return knauer.S100
