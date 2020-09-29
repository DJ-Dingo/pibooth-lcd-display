
====================
pibooth-lcd-i2c
====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-lcd-i2c`` is a plugin for the `pibooth`_ application.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/lcd.png
   :align: center
   :alt: Electronic sketch


It adds an 16x2 (HD44780) lcd screen to show numbers of photos taken, and Date/Time - connected Through I2c.
This version is for now setup to use port expander - PCF8574 Supported port expanders are the (PCF8574 -Default), the MCP23008 and the MCP23017.
Port Expander and Address app.lcd = CharLCD('PCF8574', 0x3F)

I2c port address (Default 0x27) Here it is set up with Address = 0x3F

Text "Today Photos" before "number of photos taken" Max 12 with a 16x2 LCD app.lcd.write_string('Today Photos %s' % app.count.taken)


Install
-------

::


Configuration
-------------


States description
------------------

 

Circuit diagram
---------------


.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth

.. |PythonVersions| image:: https://img.shields.io/badge/python-2.7+ / 3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 2.7+/3.6+