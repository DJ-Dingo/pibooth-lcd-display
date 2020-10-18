
====================
pibooth-lcd-i2c
====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-lcd-i2c`` is a plugin for the `pibooth`_ application.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/lcd.png
   :align: center
   :alt: LCD screen


Adds an 16x2 lcd screen (Hitachi HD44780 controller), to show numbers of photos taken and Date/Time - connected Through I2c.

This version is setup to use port expander - **PCF8574**. 

Supported port expanders are the (**PCF8574** - Default), the **MCP23008** and the **MCP23017**.

Port Expander and Address ``app.lcd = CharLCD('PCF8574', 0x3F)``   
I2c port address (**Default 0x27**) But it is set up with my I2c Address = **0x3F**   

Text "Today Photos" before "number of photos taken" Max 12 with a 16x2 LCD 
``app.lcd.write_string('Today Photos %s' % app.count.taken)``


Install
-------

::


Configuration
-------------

You need to know the address of your LCD. You can find it on the command line using the **sudo i2cdetect 1** command (or **sudo i2cdetect 0** on the original Raspberry Pi). In my case the address of the display was **0x3F**. You also need to provide the name of the I²C port expander that your board uses. It should be written on the microchip that’s soldered on to your board. 
Supported port expanders are the **PCF8574**, the **MCP23008** and the **MCP23017**.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/i2c.png
   :align: center
   :alt: I2C on the back of LCD

The board on this photo has a **PCF8574** port expander chip on it. There are also boards with other chips, e.g. the Adafruit I²C/SPI LCD Backpack which uses an **MCP23008** port expander. And the **MCP23017**


States description
------------------

 

Circuit diagram
---------------
Here is the diagram for hardware connections.
.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/
   :align: center
   :alt:  PIR-sensor Electronic sketch

Wiring
------
When using a port expander on your LCD, you will have to use 5v. Since the Raspberry Pi GPIO only handle 3.3v, it will Therefore be a good idea to use a **I2C-safe Bi-directional Logic Level Converter** so you don't fryed your pi.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/4-channel-I2C-safe-Bi-directional-Logic-Level-Converter.png
   :align: center
   :alt: 4-channel I2C-safe Bi-directional Logic Level Converter


Connection to connect your Level Converter and port expander on the Raspberry Pi (**BOARD numbering scheme**):

- GND: Pin 6 (GND)
- VCC: Pin 4 (5V)
- SDA: Pin 3 (SDA)
- SCL: Pin 5 (SCL)




.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth

.. |PythonVersions| image:: https://img.shields.io/badge/python-2.7+ / 3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 2.7+/3.6+
