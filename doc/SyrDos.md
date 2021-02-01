## Serial Settings

```
Baud Rate - 9600
Parity - None
Data Bits - 8
Stop Bits - 2
Flow Control - None
```

## Serial Commands
```
Description - Current Flow
Command - 01;IN_PV_00\r\n
Unit - ml/min
Reply - +1;IN_PV_00 000100\r\n
Value - 1 ml/min
```
```
Description - Switch and Status
Command - 01;IN_PAR_04\r\n
Unit - ml/min
Reply - +1;IN_PAR_04 1\r\n
Value - On
```
```
Description - Pressure
Command - 01;IN_PV_05\r\n
Unit - bar
Reply - +1;IN_PV_05 000100\r\n
Value - 1 bar
```
```
Description - Set Flow
Command - 01;OUT_SP_00 000100\r\n
Unit - ml/min
Reply - +1;OUT_SP_00 000100\r\n
Value - 1 ml/min
```
```
Description - Turn On/Off
Command - 01;OUT_MODE_00 0\r\n (1 for on)
Unit - On/Off
Reply - +1;OUT_MODE_00 0\r\n
Value - Off
```