# Blocktopus

A fork of the Octopus project [LINK](https://github.com/richardingham/octopus)

Blocktopus is an open source, MIT licensed, lab automation platform built on the blockly and twisted platform.

## Getting Started

### Prerequisites

I recommend running the platform using [Docker](https://www.docker.com/get-started) or [Podman](https://podman.io/getting-started/). The image has been built for amd64 and arm64. Running the image on a Linux host is recommended as you can access hardware natively (I believe this is not supported on a Windows or macOS host).

We run the platform on a Raspberry Pi 4B 4GB with Ubuntu Server 20.04 LTS 64-bit.

### Installing

1. Pull the image
   
   ```bash
   docker pull ghcr.io/gar-syn/blocktopus:latest
   ```

2. Run the container
   
   ```bash
   docker run --privileged -it -p 8001:8001 -p 9001:9001 -v /app/data:/app/data --name blocktopus ghcr.io/gar-syn/blocktopus
   ```
   
   **Note**: The above command contains`--privileged` which will grant the container access to system hardware (cameras, USB devices, serial devices, etc.). If you do not wish to do this please remove this option. Otherwise you can define which hardware can be accessed ([LINK](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)).

3. Access the platform
   
   ```bash
   http://127.0.0.1:8001
   ```

## Integrate Devices

| Type                | Manufacturer     | Model                | Status                  | Connection | Notes                                                                  |
| ------------------- | ---------------- | -------------------- |:-----------------------:| ---------- | ---------------------------------------------------------------------- |
| Pump                | Harvard Appartus | PHD 2000             | :ballot_box_with_check: | RS232      |                                                                        |
|                     | HitecZang        | LabDos               | :ballot_box_with_check: | RS232      |                                                                        |
|                     | HitecZang        | SyrDos               | :ballot_box_with_check: | RS232      |                                                                        |
|                     | Knauer           | K120                 | :ballot_box_with_check: | RS232      |                                                                        |
|                     | Knauer           | S100                 | :ballot_box_with_check: | RS232      |                                                                        |
|                     | WPI              | Aladdin              | :ballot_box_with_check: | RS232      |                                                                        |
| Reactor             | Vapourtec        | R2+/R4               | :ballot_box_with_check: | RS232      | Can't use the built in vapourtec control at the same time.             |
| Balance             | Kern             | EW                   | :ballot_box_with_check: | RS232      |                                                                        |
|                     | Mettler Toledo   | SICS                 | :ballot_box_with_check: | RS232      |                                                                        |
| Instrumentation     | Mettler Toledo   | FlowIR               | :ballot_box_with_check: | CSV        | Script must be ran on the computer running the Mettler iC IR software. |
|                     |                  | ReactIR              | :ballot_box_with_check: | CSV        | Script must be ran on the computer running the Mettler iC IR software. |
|                     | Omega            | HH306A               | :ballot_box_with_check: | RS232      |                                                                        |
| Cryostat/Thermostat | Huber            | CC3                  | :ballot_box_with_check: | RS232      |                                                                        |
|                     | Julabo           | F25                  | :ballot_box_with_check: | RS232      |                                                                        |
| Stirrer             | IKA              | Eurostar             | :ballot_box_with_check: | RS232      |                                                                        |
| Other               | VICI             | Multi Position Valve | :ballot_box_with_check: | RS232      |                                                                        |
|                     | Phidgets         | pH Sensor            | :question: Untested     | USB        |                                                                        |
|                     | StarTech         | Power Remote Control | :question: Untested     | RS232      |                                                                        |

## Built With

* [Blockly](https://github.com/google/blockly) - The Sketch interface

* [Twisted](https://github.com/twisted/twisted) - Event drive Python framework

## Authours

* Richard Ingham - [LINK](https://github.com/richardingham/)

* Gary Short - [LINK](https://github.com/gar-syn/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/gar-syn/blocktopus/blob/master/LICENSE) file for details
