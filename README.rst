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


Add any 16x2 or 20x4 LCD-screen with a **Hitachi HD44780 controller** using a port expander connected Through I2c.  :raw-html:`<br />`
It can show numbers of **Photos Taken**, **Printed Photos**, **Forgotten Photos**, **Remaining Duplicates**.  :raw-html:`<br />` 
It also have 4 x **Free-Text** where you can write your own text, and show **Date/Time**  :raw-html:`<br />` 

Supported port expanders are the (**PCF8574** - Default), the **MCP23008** and the **MCP23017**. :raw-html:`<br />` 
* I2c port address (**Default 0x27** on I2c PCF8574T ), (**Default 0x3F** on I2c PCF8574AT) :raw-html:`<br />`

  -- Show text like "Taken Photoś 197" (Max 12 letters before photo count) with a 16x2 LCD :raw-html:`<br />`
  -- Show text like "Today Photos 197" (Max 16 letters before photo count) with a 20x4 LCD :raw-html:`<br />`
  -- Show a "Free-text" (Max 16 Letters) with a 16x2 LCD :raw-html:`<br />`
  -- Show a "Free-text" (Max 20 Letters) with a 20x4 LCD :raw-html:`<br />`  

  **-- It can show a Date/Time Clock**

**All changes can be made in the pibooth.cfg**

--------------------------------------------------------------------------------

.. contents::

Requirements
------------

Hardware
^^^^^^^^

* 1 Raspberry Pi 3 Model B (or higher) :raw-html:`<br />`
* 1 LCD-screen **Hitachi HD44780 controller** with I2c (PCF8574, or MCP23008 or MCP23017) :raw-html:`<br />`
* 1 I2c safe Bi-directional Logic Level Converter :raw-html:`<br />`

Install
-------
::

  How to Setup comming soon


Configuration
-------------


Turn I2C on - Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The I2C peripheral is not turned on by default.  :raw-html:`<br />` 
There are two methods to adjust the settings. To enable it, do the following.

**Raspberry Pi Configuration via Desktop GUI**  :raw-html:`<br />` 
You can use the Desktop GUI by heading to the Pi Start Menu > Preferences > Raspberry Pi Configuration.

A window will pop up with different tabs to adjust settings. What we are interested is the Interfaces tab. :raw-html:`<br />`
Click on the tab and select Enable for I2C. Click on the OK button to save.    :raw-html:`<br />`
We recommend restarting your Pi to ensure that the changes to take effect.  :raw-html:`<br />`
Click on the Pi Start Menu > Preferences > Shutdown. Since we just need to restart, click on the Restart button.

**raspi-config Tool via Terminal**

I2C is not turned on by default. Again, we can use raspi-config to enable it.

* Run sudo raspi-config.
* Use the down arrow to select 5 Interfacing Options
* Arrow down to P5 I2C.
* Select yes when it asks you to enable I2C
* Also select yes if it asks about automatically loading the kernel module.
* Use the right arrow to select the <Finish> button.
* Select yes when it asks to reboot.

The system will reboot. when it comes back up, log in and enter the following command

``>ls /dev/*i2c*``   :raw-html:`<br />` 
The Pi should respond with

``/dev/i2c-1``        :raw-html:`<br />` 
Which represents the user-mode I2C interface.


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
You need to know the address of your I2c. You can find it on the command line using the **"sudo i2cdetect -y 1"** command.  :raw-html:`<br />` 
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


How to setup the LCD in the config.cfg file
-------------------------------------------

Options are available by editing the configuration file which is easily done using the command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

   $ pibooth --config
   

How to setup LCD_I2C in config.cfg :raw-html:`<br />`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[LCD_I2C] :raw-html:`<br />`
# Choose LCD chip - PCF8574(Default) or MCP23008 or MCP23017 :raw-html:`<br />`
lcd_chip = **PCF8574** :raw-html:`<br />`
# Change Port Address 0x3F(Default) :raw-html:`<br />`
lcd_port_address = **0x3F** :raw-html:`<br />`
# Change the I2C port number 1 or 2 - (Default = 1) :raw-html:`<br />`
lcd_port = **1** :raw-html:`<br />`
# Change the I2C charmap A00 or A02 or ST0B - (Default = A02) :raw-html:`<br />`
lcd_charmap = **A02** :raw-html:`<br />`
# Number of columns per row 16 or 20 (16 = Default on a 16x2 LCD) :raw-html:`<br />`
lcd_cols = **16** :raw-html:`<br />`
# Number of display rows 1 or 2 or 4 - (2 = Default on a 16x2 LCD) :raw-html:`<br />`
lcd_rows = **2** :raw-html:`<br />`

Write text showing before the counter :raw-html:`<br />`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Text before taken counter is displayed - Max-12 characters on a 16x2 display - Max 16 characters on a 20x4 display :raw-html:`<br />`
lcd_taken_photo_text = **Taken Photo** :raw-html:`<br />`
# Text before printed counter is displayed - Max-12 characters on a 16x2 display - Max 16 characters on a 20x4 display :raw-html:`<br />`
lcd_printed_text = **Printed** :raw-html:`<br />`
# Text before forgotten counter is displayed - Max-12 characters on a 16x2 display - Max 16 characters on a 20x4 display :raw-html:`<br />`
lcd_forgotten_text = **Forgotten** :raw-html:`<br />`
# Text before remaining_duplicates counter is displayed - Max-12 characters on a 16x2 display - Max 16 characters on a 20x4 display :raw-html:`<br />`
lcd_remaining_duplicates_text = **Duplicates** :raw-html:`<br />`

How to change the Date-Time format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See the Date-time format codes here
https://github.com/DJ-Dingo/pibooth-lcd-I2c/blob/master/Date-Time_Format_Codes.rst  :raw-html:`<br />`
# You can change the way Date-Time is displayed - Max-16 character on a 16x2 display - Max 20 character on a 20x4 display  :raw-html:`<br />`
# Default = **%d/%m - %H:%M:%S** :raw-html:`<br />`
lcd_show_date_time = **%d/%m - %H:%M:%S** :raw-html:`<br />`

Write your own free text :raw-html:`<br />`
^^^^^^^^^^^^^^^^^^^^^^^^
# Free Text 1 - Max-16 characters on a 16x2 display - Max 20 characters on a 20x4 display :raw-html:`<br />`
lcd_free_text1 = **Free Text 1** :raw-html:`<br />`
# Free Text 2 - Max-16 characters on a 16x2 display - Max 20 characters on a 20x4 display :raw-html:`<br />`
lcd_free_text2 = **Free Text 2** :raw-html:`<br />`
# Free Text 3 - Max-16 characters on a 16x2 display - Max 20 characters on a 20x4 display :raw-html:`<br />`
lcd_free_text3 = **Free Text 3** :raw-html:`<br />`
# Free Text 4 - Max-16 characters on a 16x2 display - Max 20 characters on a 20x4 display :raw-html:`<br />`
lcd_free_text4 = **Free Text 4** :raw-html:`<br />`

Select what to display on line 1,2,3,4  :raw-html:`<br />`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# '**Taken_Photo**', '**Printed**', '**Forgotten**', '**Remaining_Duplicates**', '**Date_Time**'  :raw-html:`<br />`
# '**Free_Text_1**', '**Free_Text_2**', '**Free_Text_3**', '**Free_Text_4**' :raw-html:`<br />`
# Choose what to display on line 1 :raw-html:`<br />`
lcd_line_1 = **Taken_Photo** :raw-html:`<br />`
# Choose what to display on line 2 :raw-html:`<br />`
lcd_line_2 = **Date_Time** :raw-html:`<br />`
# Choose what to display on line 3 ((( ONLY FOR 20x4 or 16x4 displays, otherwise leave empty ))) :raw-html:`<br />`
lcd_line_3 =  :raw-html:`<br />`
# Choose what to display on line 4 ((( ONLY FOR 20x4 or 16x4 displays, otherwise leave empty ))) :raw-html:`<br />`
lcd_line_4 =  :raw-html:`<br />`


States description
------------------

.. image:: https://github.com/DJ-Dingo/pibooth-lcd-I2c/blob/master/templates/state-sequence-lcd-i2c.png
   :align: center
   :alt:  State sequence


Circuit diagram
---------------
Here is the diagram for hardware connections.

.. image:: https://github.com/DJ-Dingo/pibooth-lcd-I2c/blob/master/templates/Pibooth%20LCD-I2c%20Sketch%208_bb.png
   :align: center
   :alt:  PIR-sensor Electronic sketch

Wiring
------

I2C-safe Bi-directional Logic Level Converter 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using a port expander on your LCD, you will have to use 5v.  :raw-html:`<br />`
Since the Raspberry Pi GPIO only handle 3.3v, it will therefore be a good idea to use a **I2C-safe Bi-directional Logic Level Converter** so you don't fryed your pi.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/level_converter.png
   :align: center
   :alt: 4-channel I2C-safe Bi-directional Logic Level converter


How to connect a **Level Converter** to your **Port Expander** and the Raspberry Pi (**BOARD numbering scheme**) :raw-html:`<br />`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Connect the I2c Port Expander to **HV** (High Level) on the Level Converter.  :raw-html:`<br />`

- GND: Pin GND (GND)
- VCC: Pin HV  (HV)(5v) - Also connect **5v** from the raspberry Pi Pin 2, to **HV** on the Level Converter
- SDA: Pin HV2 (HV2)
- SCL: Pin HV1 (HV1)

Connect the Raspberry Pi to **LV** (Low Level) on the Level Converter. :raw-html:`<br />`

- GND:  Pin 6 (GND)
- 3.3v: Pin 1 (LV)
- SDA:  Pin 3 (LV2)
- SCL:  Pin 5 (LV1)


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
