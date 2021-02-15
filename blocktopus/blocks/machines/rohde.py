from blocktopus.blocks.declarations import machine_declaration

class machine_rohde_hmp4040 (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import rohde
        return rohde.HMP4040

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "Rohde Schwarz HMP4040",
            "machineDefaultName": "power supply",
            "machineVars": [
                { "name": "channel", "title": "Select Channel", "type": "String", "options": ['1', '2', '3', '4'] },
                { "name": "activate", "title": "Activate Channel", "type": "String", "options": ['off', 'on'] },
                { "name": "voltage", "title": "Voltage", "type": "Number", "unit": "V" },
                { "name": "current", "title": "Amps", "type": "Number", "unit": "A" },
                { "name": "get_volt1", "title": "Ch1 V", "type": "Number", "unit": "V", "readonly": True },
                { "name": "get_amp1", "title": "Ch1 A", "type": "Number", "unit": "A",  "readonly": True }
            ]
        }