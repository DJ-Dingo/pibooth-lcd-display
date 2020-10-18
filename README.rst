.. role:: raw-html(raw)
    :format: html
====================
pibooth-lcd-i2c
====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-lcd-i2c`` is a plugin for the `pibooth`_ application.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/lcd.png
   :align: center
   :alt: LCD screen


Add an LCD-screen with **Hitachi HD44780 controller** connected Through I2c, to show numbers of photos taken and Date/Time.  :raw-html:`<br />` 
Supported port expanders are the (**PCF8574** - Default), the **MCP23008** and the **MCP23017**. :raw-html:`<br />` 

* I2c port address (**Default 0x27** on I2c PCF8574T ), (**Default 0x3F** on I2c PCF8574AT) :raw-html:`<br />`
  -- Port Expander and Address ``app.lcd = CharLCD('PCF8574', 0x3F)``  :raw-html:`<br />`

  -- Text "Today Photos" Max 12 with a 16x2 LCD :raw-html:`<br />`
     ``app.lcd.write_string('Today Photos %s' % app.count.taken)``  :raw-html:`<br />`

  **-- Date/Clock**

.. contents::

Install
-------

::


Configuration
-------------



How to find the name of your port expander on the I2c
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You need to provide the name of the I²C port expander that your board uses.  :raw-html:`<br />` 
It should be written on the microchip that’s soldered on to your I2c board. :raw-html:`<br />`  
Supported port expanders are the **PCF8574**, the **MCP23008** and the **MCP23017**.

The board on this photo has a **PCF8574** port expander chip on it. :raw-html:`<br />`

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/I2c-port-expander-name__.png
   :align: center
   :alt: I2C on the back of LCD

How to find your I2c addresss
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You need to know the address of your I2c. You can find it on the command line using the **sudo i2cdetect -y 1** command.  :raw-html:`<br />` 
In this case the address of the display is **0x3F**.  :raw-html:`<br />`

.. image:: https://github.com/DJ-Dingo/pibooth-lcd-I2c/blob/master/templates/iic-address.png
   :align: center
   :alt: I2C Address

How to change address on the I2c
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can change the address by making a bridge. :raw-html:`<br />`
Soldering 1 or more wire on the back of the I2c (short circuit) **A0**, **A1**, **A2** :raw-html:`<br />`

.. image:: https://github.com/DJ-Dingo/pibooth-lcd-I2c/blob/master/templates/I2c-adress.png
   :align: center
   :alt:  Change Address on I2c

States description
------------------

 

Circuit diagram
---------------
Here is the diagram for hardware connections.

.. image:: https://github.com/DJ-Dingo/pibooth-lcd-I2c/blob/master/templates/Pibooth%20LCD-I2c%20Sketch%208_bb.png
   :align: center
   :alt:  PIR-sensor Electronic sketch

Wiring
------
When using a port expander on your LCD, you will have to use 5v. Since the Raspberry Pi GPIO only handle 3.3v, it will Therefore be a good idea to use a **I2C-safe Bi-directional Logic Level Converter** so you don't fryed your pi.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/level_shifter.jpg
   :align: center
   :alt: 4-channel I2C-safe Bi-directional Logic Level Shifter


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

.. |PypiPackage| image:: https://badge.fury.io/py/pibooth.svg
   :target: 
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pibooth?color=purple
   :target: 
   :alt: PyPi downloads
