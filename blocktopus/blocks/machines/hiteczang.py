from blocktopus.blocks.declarations import machine_declaration

class machine_hiteczang_syrdos (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import hiteczang
        return hiteczang.SyrDos

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "HiTec-Zang SyrDos",
            "machineDefaultName": "pump",
            "machineVars": [
                { "name": "power", "title": "Power", "type": "String", "options": ['off', 'on'] },
                { "name": "target", "title": "Target flowrate", "type": "Number", "unit": { "options": [['mL/min', 1000], ['uL/min', 1]], "default": 1000 } },
                { "name": "flowrate", "title": "Flowrate", "type": "Number", "unit": { "options": [['mL/min', 1000], ['uL/min', 1]], "default": 1000 }, "readonly": True },
                { "name": "pressure", "title": "Pressure", "type": "Number", "unit": { "options": [['mbar', 1], ['bar', 1000]], "default": 1 },  "readonly": True }
            ]
        }

class machine_hiteczang_labdos (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import hiteczang
        return hiteczang.LabDos

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "HiTec-Zang LabDos",
            "machineDefaultName": "pump",
            "machineVars": [
                { "name": "power", "title": "Power", "type": "String", "options": ['off', 'on'] },
                { "name": "target", "title": "Target Speed", "type": "Number", "unit": "rpm" },
                { "name": "speed", "title": "Speed", "type": "Number", "unit": "rpm", "readonly": True },
            ]
        }

class machine_hiteczang_multivalve (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import hiteczang
        return hiteczang.MultiValve

    @staticmethod
    def get_interface_definition ():
        return {
            "machineTitle": "HiTec-Zang MultiValve",
            "machineDefaultName": "valve",
            "machineVars": [
                { "name": "position", "title": "Position", "type": "String", "options": ['A>', 'A<', 'B>', 'B<', 'C>', 'C<', 'D>', 'D<', 'E>', 'E<', 'F>', 'F<', 'G>', 'G<', 'H>', 'H<', 'I>', 'I<', 'J>', 'J<', 'K>', 'K<', 'L>', 'L<'] },
            ]
        }