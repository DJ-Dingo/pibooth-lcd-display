# -*- coding: utf-8 -*-

"""Plugin to handle small LCD display - Through GPIO 4 bit mode or I2c."""

import time
import datetime
import pibooth

from RPi import GPIO

GPIO.setmode(GPIO.BCM)

__version__ = "2.0.0"
# DJ-Dingo, Kenneth Nicholas Jørgensen : werdeil, Vincent Verdeil

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_gpio_or_i2c', "I2c",
                   "Choose I2c or GPIO setup",
                   "Choose I2c or GPIO setup", ["I2c", "GPIO"])
                   # Select display options I2c
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_chip', "PCF8574",
                   "Choose LCD chip - PCF8574(Default) or MCP23008 or MCP23017",
                   "Choose LCD chip - PCF8574(Default)", ["PCF8574", "MCP23008", "MCP23017"])
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_port_address', "0x3F",
                   'Change Port Address 0x3F(Default)',
                   "Port Expander Address", "0x3F")
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_port', "1",
                   "I2C port number 1 or 2 - (Default = 1)",
                   "I2C port number (Default = 1)", ["1", "2"])
                   # Select display options
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_charmap', "A02",
                   "Change the charmap A00 or A02 or ST0B - (Default = A02)",
                   "Change the charmap", ["A00", "A02", "ST0B"])
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_cols', "16",
                   "Number of columns per row 16 or 20 (16 = Default on a 16x2 LCD)",
                   "Number of columns per row", ["16", "20"])
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_rows', "2",
                   "Number of display rows 1 or 2 or 4 - (2 = Default on a 16x2 LCD)",
                   "Number of rows", ["1", "2", "4"])
                   # Select display options GPIO
                   # PIN setup BCM numbering scheme - 4 bit mode
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_pin_rs', "7", 
                   "GPIO-PIN_RS - Default 7",
                   "GPIO-PIN_RS - Default 7", "7")
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_pin_e', "8",
                   "GPIO-PIN_E - Default 8",
                   "GPIO-PIN_E - Default 8", "8")
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_data_pin4', "25",
                   "GPIO-DATA_PIN_4 - Default 25",
                   "GPIO-DATA_PIN_4 - Default 25", "25")
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_data_pin5', "24",
                   "GPIO-DATA_PIN_5 - Default 24",
                   "GPIO-DATA_PIN_5 - Default 24", "24")
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_data_pin6', "23",
                   "GPIO-DATA_PIN_6 - Default 23",
                   "GPIO-DATA_PIN_6 - Default 23", "23")
    cfg.add_option('LCD DISPLAY SETUP', 'lcd_data_pin7', "18",
                   "GPIO-DATA_PIN_7 - Default 18",
                   "GPIO-DATA_PIN_7 - Default 18", "18")
### Add this if you are using Backligt control
### cfg.add_option('LCD DISPLAY SETUP', 'lcd_pin_backlight', "21", 
###                "PIN_BACKLIGHT - IF NO BACKLIGHT CONTROL Set it to (None), Default 21")

    cfg.add_option('LCD DISPLAY TEXT', 'lcd_line_1_type', "Taken_Photo",
                   "Line 1 type - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date_Time, Empty_Line, Text",
                   "Line 1 type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Empty_Line', 'Text'])
    cfg.add_option('LCD DISPLAY TEXT', 'lcd_line_1_text', "Taken Photo",
                   'Line 1 text (put format code e.g. "%d/%m - %H:%M:%S" for time rendering',
                   "Line 1 text", "Taken Photo")
    cfg.add_option('LCD DISPLAY TEXT', 'lcd_line_2_type', "Date_Time",
                   "Line 2 type - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date_Time, Empty_Line, Text",
                   "Line 2 type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Empty_Line', 'Text'])
    cfg.add_option('LCD DISPLAY TEXT', 'lcd_line_2_text', "%d/%m - %H:%M:%S",
                   'Line 2 text (put format code e.g. "%d/%m - %H:%M:%S" for time rendering',
                   "Line 2 text", "%d/%m - %H:%M:%S")
    cfg.add_option('LCD DISPLAY TEXT', 'lcd_line_3_type', "Empty_Line",
                   "Line 3 type - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date_Time, Empty_Line, Text",
                   "Line 3 type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Empty_Line', 'Text'])
    cfg.add_option('LCD DISPLAY TEXT', 'lcd_line_3_text', "",
                   'Line 3 text (put format code e.g. "%d/%m - %H:%M:%S" for time rendering',
                   "Line 3 text", "")
    cfg.add_option('LCD DISPLAY TEXT', 'lcd_line_4_type', "Empty_Line",
                   "Line 4 type - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date_Time, Empty_Line, Text",
                   "Line 4 type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Empty_Line', 'Text'])
    cfg.add_option('LCD DISPLAY TEXT', 'lcd_line_4_text', "",
                   'Line 4 text (put format code e.g. "%d/%m - %H:%M:%S" for time rendering',
                   "Line 4 text", "")


def write_lcd_lines(app, specific_line_type="all"):
    """Method called to write the lines on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            for row_index in range(app.rows):
                line_text, line_type = app.lines[row_index]
                app.lcd.cursor_pos = (row_index, 0)
                if line_type == 'Taken_Photo' and specific_line_type in ['all', line_type]:
                    app.lcd.write_string(line_text[:app.cols - 4])
                    app.lcd.cursor_pos = (row_index, app.cols - 4)
                    app.lcd.write_string(' %s' % app.count.taken)
                elif line_type == 'Printed' and specific_line_type in ['all', line_type]:
                    app.lcd.write_string(line_text[:app.cols - 4])
                    app.lcd.cursor_pos = (row_index, app.cols - 4)
                    app.lcd.write_string(' %s' % app.count.printed)
                elif line_type == 'Forgotten' and specific_line_type in ['all', line_type]:
                    app.lcd.write_string(line_text[:app.cols - 4])
                    app.lcd.cursor_pos = (row_index, app.cols - 4)
                    app.lcd.write_string(' %s' % app.count.forgotten)
                elif line_type == 'Remaining_Duplicates' and specific_line_type in ['all', line_type]:
                    app.lcd.write_string(line_text[:app.cols - 4])
                    app.lcd.cursor_pos = (row_index, app.cols - 4)
                    app.lcd.write_string(' %s' % app.count.remaining_duplicates)
                elif line_type == 'Date_Time' and specific_line_type in ['all', line_type]:
                    app.lcd.write_string(time.strftime(line_text))
                elif line_type == 'Text' and specific_line_type in ['all', line_type]:
                    app.lcd.write_string(line_text[:app.cols])
        except OSError:
            pass



def connect_i2c(app, cfg):
    """I2c connect to lcd"""
    from RPLCD.i2c import CharLCD

    try:
        app.chip = cfg.get('LCD DISPLAY SETUP', 'lcd_chip')
        app.address = cfg.get('LCD DISPLAY SETUP', 'lcd_port_address').strip('"')
        app.port = cfg.get('LCD DISPLAY SETUP', 'lcd_port')
        app.charmap = cfg.get('LCD DISPLAY SETUP', 'lcd_charmap')
        app.cols = int(cfg.get('LCD DISPLAY SETUP', 'lcd_cols'))
        app.rows = int(cfg.get('LCD DISPLAY SETUP', 'lcd_rows'))
        app.lcd = CharLCD(i2c_expander=app.chip, address=int(app.address, 16),
                          port=int(app.port), charmap=(app.charmap),
                          cols=int(app.cols), rows=int(app.rows),
                          backlight_enabled=True)
    except OSError:
        pass


    # line conf part
    app.lines = [(cfg.get('LCD DISPLAY TEXT', 'lcd_line_1_text').strip('"'), cfg.get('LCD DISPLAY TEXT', 'lcd_line_1_type')),
                 (cfg.get('LCD DISPLAY TEXT', 'lcd_line_2_text').strip('"'), cfg.get('LCD DISPLAY TEXT', 'lcd_line_2_type')),
                 (cfg.get('LCD DISPLAY TEXT', 'lcd_line_3_text').strip('"'), cfg.get('LCD DISPLAY TEXT', 'lcd_line_3_type')),
                 (cfg.get('LCD DISPLAY TEXT', 'lcd_line_4_text').strip('"'), cfg.get('LCD DISPLAY TEXT', 'lcd_line_4_type'))]




def connect_lcd_gpio(app, cfg):
    """connect to LCD Through GPIO 4 bit mode"""
    from RPLCD.gpio import CharLCD
    
    try:

        app.pin_rs = int(cfg.get('LCD DISPLAY SETUP', 'lcd_pin_rs'))
        app.pin_e = int(cfg.get('LCD DISPLAY SETUP', 'lcd_pin_e'))
        app.data_pin4 = int(cfg.get('LCD DISPLAY SETUP', 'lcd_data_pin4'))
        app.data_pin5 = int(cfg.get('LCD DISPLAY SETUP', 'lcd_data_pin5'))
        app.data_pin6 = int(cfg.get('LCD DISPLAY SETUP', 'lcd_data_pin6'))
        app.data_pin7 = int(cfg.get('LCD DISPLAY SETUP', 'lcd_data_pin7'))

### If you are using Backligt Control add this:
###     app.pin_backlight = int(cfg.get('LCD', 'lcd_pin_backlight'))

        app.charmap = cfg.get('LCD DISPLAY SETUP', 'lcd_charmap')
        app.cols = int(cfg.get('LCD DISPLAY SETUP', 'lcd_cols'))
        app.rows = int(cfg.get('LCD DISPLAY SETUP', 'lcd_rows'))
        app.lcd = CharLCD(numbering_mode=GPIO.BCM, charmap=(app.charmap), cols=int(app.cols),
                          rows=int(app.rows), pin_rs=int(app.pin_rs),
                          pin_e=int(app.pin_e), pins_data=[int(app.data_pin4),
                          int(app.data_pin5), int(app.data_pin6),
                          int(app.data_pin7)], backlight_enabled=True)  #, backlight_mode=BacklightMode.active_high

### If you are using Backligt Control add this to CharLCD:
### pin_backlight=int(app.pin_backlight)

    except OSError:
        pass

    # line conf part
    app.lines = [(cfg.get('LCD DISPLAY TEXT', 'lcd_line_1_text').strip('"'), cfg.get('LCD DISPLAY TEXT', 'lcd_line_1_type')),
                 (cfg.get('LCD DISPLAY TEXT', 'lcd_line_2_text').strip('"'), cfg.get('LCD DISPLAY TEXT', 'lcd_line_2_type')),
                 (cfg.get('LCD DISPLAY TEXT', 'lcd_line_3_text').strip('"'), cfg.get('LCD DISPLAY TEXT', 'lcd_line_3_type')),
                 (cfg.get('LCD DISPLAY TEXT', 'lcd_line_4_text').strip('"'), cfg.get('LCD DISPLAY TEXT', 'lcd_line_4_type'))]



@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Connect the LCD to I2c portexpander or GPIO
    # startup.
    app.gpio_or_i2c = cfg.get('LCD DISPLAY SETUP', 'lcd_gpio_or_i2c')
    # Choose I2c or GPIO connection
    c = app.gpio_or_i2c.split()
    if "I2c" in c:
        connect_i2c(app, cfg)
    elif "GPIO" in c:
        connect_lcd_gpio(app, cfg)
    # Write all lines at startup
    app.lcd.clear

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    # Connect the LCD to I2c portexpander or GPIO
    # enter in 'wait' state.
    app.gpio_or_i2c = cfg.get('LCD DISPLAY SETUP', 'lcd_gpio_or_i2c')
    # Choose I2c or GPIO connection
    c = app.gpio_or_i2c.split()
    if "I2c" in c:
        connect_i2c(app, cfg)
    elif "GPIO" in c:
        connect_lcd_gpio(app, cfg)
    # Write all lines at startup
    write_lcd_lines(app)

@pibooth.hookimpl
def state_wait_do(app):
    # Re-Write the date at 'wait' do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_choose_enter(app):
    # Re-Write the date at chose do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_choose_do(app):
    # Re-Write the date at chose do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_chosen_do(app):
    # Re-Write the date at chosen do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_preview_enter(app):
    # Re-Write the date at preview_do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_preview_do(app):
    # Re-Write the date at preview_do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_preview_validate(app):
    # Re-Write the date at preview_validate
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_preview_exit(app):
    # Re-Write the date at preview_exit
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_capture_enter(app):
    # Re-Write the date at capture_enter
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_capture_do(app):
    # Re-Write the date at capture_do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_capture_validate(app):
    # Re-Write the date at capture_validate
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_capture_exit(app):
    # Re-Write the date at capture_exit
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_processing_enter(app):
    # Re-Write the date at processing_enter
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_processing_do(app):
    # Re-Write the date at processing_do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_processing_validate(app):
    # Re-Write the date at processing_validate
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_processing_exit(app):
    # Re-Write the date at processing_exit
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_print_do(app):
    # Re-Write the date at print_do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_finish_do(app):
    # Re-Write the date at finish_do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def state_failsafe_do(app):
    # Re-Write the date at failsafe_do
    write_lcd_lines(app, specific_line_type="Date_Time")

@pibooth.hookimpl
def pibooth_cleanup(app):
    # Turn off backlight when pibooth close, close lcd screen
    if hasattr(app, 'lcd'):
        try:
            c = app.gpio_or_i2c.split()
            if "I2c" in c:
                app.lcd.backlight_enabled=False
                app.lcd.close(clear=True)
            elif "GPIO" in c:
                app.lcd.clear
                GPIO.cleanup([app.pin_rs, app.pin_e, app.data_pin4, app.data_pin5, app.data_pin6, app.data_pin7])
                ### Add "app.pin_backlight" to GPIO.cleanup if you are using Backligt control
        except OSError:
            pass
