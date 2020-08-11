from octopus.blocktopus.blocks.machines import machine_declaration

class machine_vapourtec_R2R4 (machine_declaration):
    def getMachineClass (self):
        from octopus.manufacturer import vapourtec
        return vapourtec.R2R4

    @staticmethod
    def get_interface_definition ():
        R2R4_vars = [
            { "name": "status", "title": "Status", "type": "String", "readonly": True }, 
            { "name": "power", "title": "Power", "type": "String", "options": ['off', 'on'] }, 
            { "name": "loop1", "title": "Loop A", "type": "String", "options": ['load', 'inject'] }, 
            { "name": "loop2", "title": "Loop B", "type": "String", "options": ['load', 'inject'] }, 
            { "name": "pressure_limit", "title": "Pressure Limit", "type": "Number", "unit": { "options": [['mbar', 1], ['bar', 1000]], "default": 1000 } }, 
            { "name": "pressure", "title": "System Pressure", "type": "Number", "readonly": True, "unit": { "options": [['mbar', 1], ['bar', 1000]], "default": 1000 } }, 
            { "name": "output", "title": "Output", "type": "String", "options": ['waste', 'collect'] }
        ]

        for i in range(2):
            R2R4_vars.append(
                { "name": f"pump{i + 1}", "title": f"Pump {chr(65 + i)}", "parts": [
                    { "name": "target", "title": "Target", "type": "Number", "unit": { "options": [['mL/min', 1000], ['uL/min', 1]], "default": 1000 } },
                    { "name": "rate", "title": "Flow Rate", "type": "Number", "readonly": True, "unit": { "options": [['mL/min', 1000], ['uL/min', 1]], "default": 1000 } },
                    { "name": "pressure", "title": "Pressure", "type": "Number", "readonly": True, "unit": { "options": [['mbar', 1], ['bar', 1000]], "default": 1000 } },
                    { "name": "input", "title": "Input", "type": "String", "options": ['solvent', 'reagent'] },
                    { "name": "airlock", "title": "Airlock", "type": "Number", "readonly": True }
                ]}
            )
        
        for i in range(4):
            R2R4_vars.append(
                { "name": f"heater{i + 1}", "title": f"Heater {chr(65 + i)}", "parts": [
                    { "name": "target", "title": "Target", "type": "Number", "unit": 'C' },
                    { "name": "temp", "title": "Temperature", "type": "Number", "readonly": True, "unit": 'C' },
                    { "name": "mode", "title": "Mode", "type": "Number", "readonly": True },
                    { "name": "power", "title": "Power", "type": "Number", "readonly": True, "unit": 'W' }
                ]
            })

        return {
            "machineTitle": "Vapourtec R2+/R4",
            "machineVars": R2R4_vars,
            "machineVarFlags": { "providesGSIOC": True }
        }