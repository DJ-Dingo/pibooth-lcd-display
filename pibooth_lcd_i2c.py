# -*- coding: utf-8 -*-

"""Plugin to handle small LCD display."""

import time
import datetime
import pibooth
from RPLCD.i2c import CharLCD

__version__ = "1.0.0"
# DJ-Dingo, Kenneth Nicholas Jørgensen : werdeil, Vincent Verdeil

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('LCD_I2C', 'lcd_chip', "PCF8574",
                   "Choose LCD chip - PCF8574(Default) or MCP23008 or MCP23017")
    cfg.add_option('LCD_I2C', 'lcd_port_address', "0x3F",
                   'Change Port Address 0x3F(Default)',
                   "Port Expander Address", "0x3F")
    cfg.add_option('LCD_I2C', 'lcd_port', "1",
                   "Change the I2C port number 1 or 2 - (Default = 1)")
    cfg.add_option('LCD_I2C', 'lcd_charmap', "A02",
                   "Change the I2C charmap A00 or A02 or ST0B - (Default = A02)")
    cfg.add_option('LCD_I2C', 'lcd_cols', "16",
                   "Number of columns per row 16 or 20 (16 = Default on a 16x2 LCD)",
                   "Number of columns per row", ["16", "20"])
    cfg.add_option('LCD_I2C', 'lcd_rows', "2",
                   "Number of display rows 1 or 2 or 4 - (2 = Default on a 16x2 LCD)",
                   "Number of rows", ["1", "2", "4"])

    cfg.add_option('LCD_I2C', 'lcd_line_1_type', "Taken_Photo",
                   "Line 1 type",
                   "Line 1 type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Text'])
    cfg.add_option('LCD_I2C', 'lcd_line_1_text', "Taken Photo",
                   'Line 1 text (put format code e.g. "%d/%m - %H:%M:%S" for time rendering',
                   "Line 1 text", "Taken Photo")
    cfg.add_option('LCD_I2C', 'lcd_line_2_type', "Date_Time",
                   "Line 2 type",
                   "Line 2 type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Text'])
    cfg.add_option('LCD_I2C', 'lcd_line_2_text', "%d/%m - %H:%M:%S",
                   'Line 2 text (put format code e.g. "%d/%m - %H:%M:%S" for time rendering',
                   "Line 2 text", "%d/%m - %H:%M:%S")
    cfg.add_option('LCD_I2C', 'lcd_line_3_type', "None",
                   "Line 3 type",
                   "Line 3 type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Text'])
    cfg.add_option('LCD_I2C', 'lcd_line_3_text', "",
                   'Line 3 text (put format code e.g. "%d/%m - %H:%M:%S" for time rendering',
                   "Line 3 text", "")
    cfg.add_option('LCD_I2C', 'lcd_line_4_type', "None",
                   "Line 4 type - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date_Time, Text",
                   "Line 4 type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Text'])
    cfg.add_option('LCD_I2C', 'lcd_line_4_text', "",
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
    try:
        app.chip = cfg.get('LCD_I2C', 'lcd_chip')
        app.address = cfg.get('LCD_I2C', 'lcd_port_address').strip('"')
        app.port = cfg.get('LCD_I2C', 'lcd_port')
        app.charmap = cfg.get('LCD_I2C', 'lcd_charmap')
        app.cols = int(cfg.get('LCD_I2C', 'lcd_cols'))
        app.rows = int(cfg.get('LCD_I2C', 'lcd_rows'))
        app.lcd = CharLCD(i2c_expander=app.chip, address=int(app.address, 16),
                          port=int(app.port), charmap=(app.charmap),
                          cols=int(app.cols), rows=int(app.rows),
                          backlight_enabled=True)
    except OSError:
        pass

    # line conf part
    app.lines = [(cfg.get('LCD_I2C', 'lcd_line_1_text').strip('"'), cfg.get('LCD_I2C', 'lcd_line_1_type')),
                 (cfg.get('LCD_I2C', 'lcd_line_2_text').strip('"'), cfg.get('LCD_I2C', 'lcd_line_2_type')),
                 (cfg.get('LCD_I2C', 'lcd_line_3_text').strip('"'), cfg.get('LCD_I2C', 'lcd_line_3_type')),
                 (cfg.get('LCD_I2C', 'lcd_line_4_text').strip('"'), cfg.get('LCD_I2C', 'lcd_line_4_type'))]


@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Connect the LCD to I2c portexpander
    # startup.
    connect_i2c(app, cfg)

    # Write all lines at startup
    write_lcd_lines(app)

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    # Connect the LCD to I2c portexpander
    # enter in 'wait' state.
    connect_i2c(app, cfg)

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
            app.lcd.backlight_enabled=False
            app.lcd.close(clear=True)
        except OSError:
            pass
