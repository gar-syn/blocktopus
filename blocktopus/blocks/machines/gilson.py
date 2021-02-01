from blocktopus.blocks.declarations import machine_declaration

class machine_gilson_FractionCollector203B (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import gilson
        return gilson.FractionCollector203B