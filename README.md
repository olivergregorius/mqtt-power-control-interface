# mqtt-power-control-interface

[![GitHub](https://img.shields.io/github/license/olivergregorius/mqtt-power-control-interface?label=License)](https://github.com/olivergregorius/mqtt-power-control-interface/blob/HEAD/LICENSE)

## Introduction

Micropython project for front panel header power control using the MQTT protocol

## Hardware

This project includes a Kicad project providing schematics and a board layout for placing a Raspberry Pi Pico W on it. The microcontroller acts as a lightweight
MQTT client publishing and controlling the power state of up to 12 devices that are connected via the "Intel 9-pin header" (front panel header):

!TODO include picture of front panel header here!

The microcontroller and the devices are not directly connected, instead, they are galvanically isolated from each other by optocouplers, mitigating the risk of
damage.

The power state is determined by the state of the device's power LED pins. It is active low from the microcontroller's perspective.

The power state is controlled by shorting the device's power button pins for 500 milliseconds. That means if the device initially is powered off, it will be
powered on after the power button pins have been shortened. Powering off the machine is up to the operating system's power management, e.g. on Ubuntu if the
power button is pressed shortly (500 milliseconds are sufficient) a shutdown will be initiated, powering off the device.

Thus, each device can be controlled by two GPIO pins of the microcontroller: one for the power state check, one for the power button control.

## Software

This project is written in Micropython and can be flashed onto various microcontroller boards, e.g. the Raspberry Pi Pico W.

### Required Libraries

- umqtt.simple
- micropython_ota (see [https://github.com/olivergregorius/micropython_ota](https://github.com/olivergregorius/micropython_ota))
- micropython_loki (see [https://github.com/olivergregorius/micropython_loki](https://github.com/olivergregorius/micropython_loki))

### Required Files

The following files are required to be flashed onto the microcontroller:

- `boot.py` - Bootup script containing routines for establishing WiFi connection and installing required libraries
- `mqtt.py` - MQTT client library
- `types.py` - Utility file containing type definitions
- `utils.py` - Utility file containing utility methods
- `main.py` - Main routine
- `config.py` - Config file, see `config.template.py` as reference, the keys are self explanatory

### Message Formats

The message format is JSON.

#### Power State

The power state for each device is published to the topic defined in the config in a dedicated message for each device:

```json
{
    "deviceName": "device1",
    "state": "stopped"
}
```

The `state` attribute can take the values `stopped` and `running`.

#### Power Control

The power state for each device can be controlled by sending a dedicated message for each device to the defined topic in the config:

```json
{
    "deviceName": "device1",
    "action": "powerOn"
}
```

The `action` attribute can take the values `powerOn` and `powerOff`, whereas for now both of the actions trigger a 500 millisecond power button push, regardless
of the current state of the device.

## Disclaimer

This hardware/software is provided "as is", and you use the hardware/software at your own risk. Under no circumstances shall any author be liable for direct,
indirect, special, incidental, or consequential damages resulting from the use, misuse, or inability to use this hardware/software, even if the authors have
been advised of the possibility of such damages.
