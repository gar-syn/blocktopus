from blocktopus.blocks.declarations import machine_declaration

class machine_startech_powerremotecontrol (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import startech
        return startech.PowerRemoteControl