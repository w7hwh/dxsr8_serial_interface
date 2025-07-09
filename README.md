# DX-SR8 Serial Interface

Since I have a DX-SR8 and a few Raspberry Pi Picos sitting around I decided to try building an interface based on a Raspberry Pi Pico 2w. If nothing else the project will force me to become more familiar with MicroPython.

Back in 2013 AJ9BM did an analysis of the communication between the DX-SR8's chassis and its front panel. He found out a great deal about the protocol and built working prototypes but for some reason he abandoned the project. 

Before he did he released the python analysis code in /aj9bm_code [on Github](https://github.com/jbm9/dxsr8_serial) and a couple of videos on YouTube. [Showing the analysis code running](https://www.youtube.com/watch?v=cRo2k7FbKFA),  [a prototype board controlling the rig](https://www.youtube.com/watch?v=0eBNIf6Rozc), and [another of a more finished prototype board controlling the rig](https://www.youtube.com/watch?v=aqtLbdCvwj8). Unfortunately at that point he abandoned the project and never released the board design or the final code.

# Planned stages are:

- [ ] Firmware to continue analyzing the protocol. Essentially use the pico as a double channel usb-serial adapter with some analysis/decoding capability.

- [ ] Design a board

- [ ] Add capability to send CAT commands to control the rig.

- [ ] Add capability to send/receive audio?

- [ ] Add a webserver to provide a different way to control it.


# Contents:

1. firmware/ -- My code to run in MicroPython on a Raspberry Pi Pico 2w.
2. board/ -- Board design files
3. aj9bm_code/ -- The original python analysis code AJ9BM wrote back in 2013.

