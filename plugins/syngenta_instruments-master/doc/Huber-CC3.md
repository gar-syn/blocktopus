## Serial Settings

A42EA926-931E-4735-8AC1-66E96A100DDF

```
Baud Rate - 9600
Parity - None
Data Bits - 8
Stop Bits - 1
Flow Control - None
Command End - \r\n
```

## Serial Commands
```
Description - Turn On
Command - KM_ON@
Reply - ON
```
```
Description - Turn Off
Command - KM_OFF@
Reply - OFF
```
```
Description - Status
Command - KM?
Reply - OFF/ON
```
```
Description - Bath temperature
Command - TI?
Reply - TI +02198\r\n
Unit - C
Value - 21.98
```
```
Description - External temperature
Command - TE?
Reply - TE -12761\r\n
Unit - C
Value - -127.61
```
```
Description - Set Setpoint
Command - SP@ %+06d
Reply - 
```
```
Description - Get Setpoint
Command - SP?
Reply - SP +02000\r\n
Unit - C
Value - 20.00
```