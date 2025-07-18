# DX-SR8 Head/Chassis Protocol

TODO:

- add examples and explainations for head to chassis part.

- document the chassis to head part.

---

## Introduction

The DXSR8's control head is connected to the chassis by a standard ethernet type cable with RJ45 connectors. It's not ethernet but it uses the same cable.

They communicate via two TTL level (5v) serial lines at 38400 8N1. They should not be directly connected to a 3.3v processor.

Most of the protocol was figured out by [AJ9BM](./aj9bm.md) back in 2013. He didn't produce documentation but it's in his python analysis code.

---

## Packets sent at powerup

b'AL~READY\r\n'
b'SWDA0000000081718AA1800100\r\n'
b'SWDV81728AA10100\r\n'

---

## Packets sent head to chassis

### AL~READY

This appears to be the head telling the chassis that it's ready. The only time I've seen it is at powerup.

b'AL~READY\r\n'

### SWDV

Contains rit, ifshift, squelch, and volume.

This is the most common packet because the values of these knobs seem to jitter a little bit. You get this even if you aren't touching the controls.

### SWDR

Contains the direction of rotation of the frequency dial

### SWDA

Related to the frequency dial? We get this packet when we spin the dial rapidly.

### SWDS

Contains the switches on the front panel excluding the power switch.
    
---

## Packets sent chassis to head

Coming soon.

