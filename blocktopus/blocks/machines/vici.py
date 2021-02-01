from blocktopus.blocks.declarations import machine_declaration

class machine_vici_multivalve (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import vici
        return vici.MultiValve