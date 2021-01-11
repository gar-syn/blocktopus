## Serial Settings

6EF3132A-5231-4B69-B35F-3AACEA5A642B

```
Baud Rate - 9600
Parity - Even
Data Bits - 7
Stop Bits - 1
Flow Control - None
```

## Serial Commands
```
Description - Current RPM
Command - IN_PV_4
Unit - 1/min
Reply - 50.0 4\s\r\s\n
```

```
Description - Setpoint RPM
Command - OUT_SP_4     0 \r \n
Unit - 1/min
```

```
Description - Remote On
Command - START_4
```

```
Description - Remote Off
Command - STOP_4
```

```
Description - Torque
Command - IN_PV_5
Unit - Ncm
Reply - 22.0 5\s\r\s\n
```