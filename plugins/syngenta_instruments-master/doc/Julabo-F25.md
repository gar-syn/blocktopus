## Serial Settings

4D9A0CF7-C7A7-4F60-B6CC-E8AE4D3C6F64

```
Baud Rate - 4800
Parity - Even
Data Bits - 7
Stop Bits - 1
Flow Control - None
Command End - \r\n
```

## Serial Commands
```
Description - Turn On/Off
Command - OUT_MODE_05 0 or 1
Reply - 
```
```
Description - Bath temperature
Command - IN_PV_00
Reply - 23.50
Unit - °C
Value - 23.50
```
```
Description - External temperature
Command - IN_PV_02
Reply - 0.00
Unit - °C
Value - 0.00
```
```
Description - Set Setpoint
Command - OUT_SP_00
Reply - 
```
```
Description - Get Setpoint
Command - IN_SP_00
Reply - 23.50
Unit - °C
Value - 23.50
```