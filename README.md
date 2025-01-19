Raspberry-based RCU
===

# Parts
* [TAA020A RCU](docs/RCU%20Rising%20Sun%20TAA02A/readme.md)

Each part will be stacked boards.

# Controlling several parts above 26 I/O
Trick: addressing multiplexed I/O notable with the [I2C protocol](https://en.m.wikipedia.org/wiki/I2C) or [SPI](https://en.m.wikipedia.org/wiki/Serial_Peripheral_Interface)

* You need to define which GPIO port will be IN or OUT across the many staked boards.
* To send a signal to a given card, GPIO could be combined, say in binary, and each board will calculate (eg. with logic gates) to retrieve signals addressed to it



