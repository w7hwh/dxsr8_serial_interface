# DXSR8 Serial Interface Firmware for Stm32

The micropython version doesn't seem able to keep up with decoding the data from the radio.  It seems to fill any size buffer I set and then overflow it. This makes sense because the original python code was written to do analysis on a desktop/laptop system, not run realtime on a small cpu.

This is (or will be) a version written in C to run on a STM32 chip under freeRTOS. Both picked not for strong technical reasons but because I have experience with them.


