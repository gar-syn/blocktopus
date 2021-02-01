from blocktopus.blocks.declarations import machine_declaration

class machine_omega_hh306a (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import omega
        return omega.HH306A