# DX-SR8 Serial Interface

## Introduction

Since I have a DX-SR8 and a few Raspberry Pi Picos sitting around I decided to try building an interface based on a Raspberry Pi Pico 2. If nothing else the project will force me to become more familiar with MicroPython.

Back in 2013 AJ9BM did an analysis of the communication between the DX-SR8's chassis and its front panel. He found out a great deal about the protocol and built working prototypes but he eventually abandoned the project. More about his work is in [aj9bm.md](./aj9bm.md).
 
The micropython didn't work so well for me so I've switched to programming in C to run under freeRTOS. This was picked because of the same reason many things are decided, I have experience with both C and freeRTOS. :^) Initially I'm using a "Blue Pill" board with a cpu labeled STM32F103CBT6 . The ST-INFO utility says it has 256k flash and 64k of ram instead of the lower amounts that chip is supposed to have. 

---

## Planned stages are:

- [x] Micropython firmware to continue analyzing the protocol using a breadboarded RPi Pico 2. Essentially use the Pico as a double channel usb-serial adapter with some analysis/decoding capability. This includes converting the original python2 to python3.

- [ ] Firmware to actually control the radio. Currently planned to be in C running under freeRTOS.

- [ ] Design a board.

- [ ] Add capability to send CAT commands to control the rig.

- [ ] Add capability to send/receive audio?

---

## Contents:

- aj9bm_code/ -- The original python analysis code AJ9BM wrote back in 2013.
- board/ -- Board design files
- documentation/ -- Documenting the protocol between radio and head.
- firmware_c/ -- My code to run in C on a STM32 cpu. (currently a STM32F103 based 'Blue Pill' board.)
- firmware_python/ -- My code to run in MicroPython on a Raspberry Pi Pico 2. This has been abandoned in favor of the C version.
- images/ -- Images

