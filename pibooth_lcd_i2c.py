# -*- coding: utf-8 -*-

"""Plugin to handle small LCD display."""

import time
import datetime
import pibooth
from RPLCD.i2c import CharLCD

__version__ = "1.1.0"
# DJ-Dingo, Kenneth Nicholas Jørgensen

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('LCD_I2C', 'lcd_chip', "PCF8574", 
                   "Choose LCD chip - PCF8574(Default) or MCP23008 or MCP23017")
    cfg.add_option('LCD_I2C', 'lcd_port_address', "0x3F", 
                   "Change Port Address 0x3F(Default)")
    cfg.add_option('LCD_I2C', 'lcd_port', "1", 
                   "Change the I2C port number 1 or 2 - (Default = 1)")
    cfg.add_option('LCD_I2C', 'lcd_charmap', "A02", 
                   "Change the I2C charmap A00 or A02 or ST0B - (Default = A02)")
    cfg.add_option('LCD_I2C', 'lcd_cols', "16", 
                   "Number of columns per row 16 or 20 (16 = Default on a 16x2 LCD)")
    cfg.add_option('LCD_I2C', 'lcd_rows', "2", 
                   "Number of display rows 1 or 2 or 4 - (2 = Default on a 16x2 LCD)")
                   # Text
    cfg.add_option('LCD_I2C', 'lcd_taken_photo_text', "Taken Photo", 
                   "Text before taken counter is displayed - Max-12 characters on a 16x2 display - Max 16 characters on a 20x4 display")
    cfg.add_option('LCD_I2C', 'lcd_show_date_time', "%d/%m - %H:%M:%S", 
                   "You can change the way Date-Time is displayed - Max-16 character on a 16x2 display - Max 20 character on a 20x4 display \n# Default %d/%m - %H:%M:%S")
    cfg.add_option('LCD_I2C', 'lcd_printed_text', "Printed", 
                   "Text before printed counter is displayed - Max-12 characters on a 16x2 display - Max 16 characters on a 20x4 display")
    cfg.add_option('LCD_I2C', 'lcd_forgotten_text', "Forgotten", 
                   "Text before forgotten counter is displayed - Max-12 characters on a 16x2 display - Max 16 characters on a 20x4 display")
    cfg.add_option('LCD_I2C', 'lcd_remaining_duplicates_text', "Duplicates", 
                   "Text before remaining_duplicates counter is displayed - Max-12 characters on a 16x2 display - Max 16 characters on a 20x4 display")
                   # Free Text
    cfg.add_option('LCD_I2C', 'lcd_free_text1', "Free Text 1", 
                   "Free Text 1 - Max-16 characters on a 16x2 display - Max 20 characters on a 20x4 display")
    cfg.add_option('LCD_I2C', 'lcd_free_text2', "Free Text 2", 
                   "Free Text 2 - Max-16 characters on a 16x2 display - Max 20 characters on a 20x4 display")
    cfg.add_option('LCD_I2C', 'lcd_free_text3', "Free Text 3", 
                   "Free Text 3 - Max-16 characters on a 16x2 display - Max 20 characters on a 20x4 display")
    cfg.add_option('LCD_I2C', 'lcd_free_text4', "Free Text 4", 
                   "Free Text 4 - Max-16 characters on a 16x2 display - Max 20 characters on a 20x4 display")
                   # Line select options
    cfg.add_option('LCD_I2C', 'lcd_line_1', "Taken_Photo", 
                   "Choose what to display on line 1\n# 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Free_Text_1', 'Free_Text_2', 'Free_Text_3', 'Free_Text_4'")
    cfg.add_option('LCD_I2C', 'lcd_line_2', "Date_Time", 
                   "Choose what to display on line 2\n# 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Free_Text_1', 'Free_Text_2', 'Free_Text_3', 'Free_Text_4'")
    cfg.add_option('LCD_I2C', 'lcd_line_3', " ", 
                   "Choose what to display on line 3 ((( ONLY FOR 20x4 or 16x4 displays, otherwise leave empty )))\n# 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Free_Text_1', 'Free_Text_2', 'Free_Text_3', 'Free_Text_4'")
    cfg.add_option('LCD_I2C', 'lcd_line_4', " ", 
                   "Choose what to display on line 4 ((( ONLY FOR 20x4 or 16x4 displays, otherwise leave empty )))\n# 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Free_Text_1', 'Free_Text_2', 'Free_Text_3', 'Free_Text_4'")

#'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'Free_text_1', 'Free_text_2', 'Free_text_3', 'Free_text_4')

def write_date(app):
    """Method called to write the Date on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            for line_index, line in enumerate(app.lines):
                if "date_time" in line.split():
                    app.lcd.cursor_pos = (line_index, 0)
                    app.lcd.write_string(time.strftime(app.show_date_time))
        except OSError:
            pass


def write_photo_count(app):
    """Method called to write the Taken Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            for line_index, line in enumerate(app.lines):
                if "taken_photo" in line.split():
                    app.lcd.cursor_pos = (line_index, 0)
                    app.lcd.write_string(app.taken_photo_text)[:app.cols]
                    app.lcd.cursor_pos = (line_index, app.cols)
                    app.lcd.write_string('%s' % app.count.taken)
        except OSError:
            pass


def write_printed_count(app):
    """Method called to write the Printed Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            for line_index, line in enumerate(app.lines):
                if "printed" in line.split():
                    app.lcd.cursor_pos = (line_index, 0)
                    app.lcd.write_string(app.printed_text[:app.cols])
                    app.lcd.cursor_pos = (line_index, app.cols)
                    app.lcd.write_string('%s' % app.count.printed)
        except OSError:
            pass


def write_forgotten_count(app):
    """Method called to write the Forgotten Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            for line_index, line in enumerate(app.lines):
                if "forgotten" in line.split():
                    app.lcd.cursor_pos = (line_index, 0)
                    app.lcd.write_string(app.forgotten_text[:app.cols])
                    app.lcd.cursor_pos = (line_index, app.cols)
                    app.lcd.write_string('%s' % app.count.forgotten)
        except OSError:
            pass


def write_remaining_duplicates_count(app):
    """Method called to write the Remaining Duplicates Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            for line_index, line in enumerate(app.lines):
                if "remaining_duplicates" in line.split():
                    app.lcd.cursor_pos = (line_index, 0)
                    app.lcd.write_string(app.remaining_duplicates_text)[:app.cols]
                    app.lcd.cursor_pos = (line_index, app.cols)
                    app.lcd.write_string('%s' % app.count.remaining_duplicates)
        except OSError:
            pass


def write_free_texts(app):
    """Method called to write the Free-Text 4 on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            for free_text in app.free_texts:
                for line_index, line in enumerate(app.lines):
                    if free_text in line.split():
                        app.lcd.cursor_pos = (line_index, 0)
                        app.lcd.write_string(free_text[:app.cols])
        except OSError:
            pass


def connect_i2c(app, cfg):
    """I2c connect to lcd"""
    try:
        app.chip = cfg.get('LCD_I2C', 'lcd_chip')
        app.address = cfg.get('LCD_I2C', 'lcd_port_address')
        app.port = cfg.get('LCD_I2C', 'lcd_port')
        app.charmap = cfg.get('LCD_I2C', 'lcd_charmap')
        app.cols = int(cfg.get('LCD_I2C', 'lcd_cols'))
        app.rows = cfg.get('LCD_I2C', 'lcd_rows')
        app.lcd = CharLCD(i2c_expander=app.chip, address=int(app.address, 16),
                          port=int(app.port), charmap=(app.charmap),
                          cols=int(app.cols), rows=int(app.rows),
                          backlight_enabled=True)
    except OSError:
        pass

    # line conf part
    app.lines = [cfg.get('LCD_I2C', 'lcd_line_1').lower(),
                 cfg.get('LCD_I2C', 'lcd_line_2').lower(),
                 cfg.get('LCD_I2C', 'lcd_line_3').lower(),
                 cfg.get('LCD_I2C', 'lcd_line_4').lower()]

    # free text conf part
    app.free_texts = [cfg.get('LCD_I2C', 'lcd_free_text1'),
                      cfg.get('LCD_I2C', 'lcd_free_text2'),
                      cfg.get('LCD_I2C', 'lcd_free_text3'),
                      cfg.get('LCD_I2C', 'lcd_free_text4')]

    # datetime conf part
    app.show_date_time = cfg.get('LCD_I2C', 'lcd_show_date_time')
    app.taken_photo_text = cfg.get('LCD_I2C', 'lcd_taken_photo_text')

# app.lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, auto_linebreak=False, backlight_enabled=False)

@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Connect the LCD to I2c portexpander
    # startup.
    connect_i2c(app, cfg)
    
    # Re-write the number of taken photo each time pibooth
    # startup.
    write_photo_count(app)

    # Re-write the number of printed pictures each time pibooth
    # startup.
    write_printed_count(app)
        
    # Re-Write the number of forgotten pictures at pibooth
    # startup
    write_forgotten_count(app)

    # Re-Write the number of remaining_duplicates at pibooth
    # startup
    write_remaining_duplicates_count(app)

    # Re-Write the date/time at pibooth
    # startup
    write_date(app)
    
    # Write Free-Texts 
    # startup.
    write_free_texts(app)

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    # Connect the LCD to I2c portexpander
    # enter in 'wait' state.
    connect_i2c(app, cfg)

    # Re-write the number of taken pictures each time pibooth
    # enter in 'wait' state.
    write_photo_count(app)

    # Re-write the number of printed pictures each time pibooth
    # enter in 'wait' state.
    write_printed_count(app)
        
    # Re-Write the number of forgotten pictures at pibooth
    # enter in 'wait' state.
    write_forgotten_count(app)

    # Re-Write the number of remaining_duplicates at pibooth
    # enter in 'wait' state.
    write_remaining_duplicates_count(app)

    # Re-Write the date at pibooth
    # enter in 'wait' state.
    write_date(app)
    
    # Write Free-Texts
    # enter in 'wait' state.
    write_free_texts(app)

@pibooth.hookimpl
def state_wait_do(app):
    # Re-Write the date at 'wait' do
    write_date(app)

@pibooth.hookimpl
def state_choose_enter(app):
    # Re-Write the date at chose do
    write_date(app)

@pibooth.hookimpl
def state_choose_do(app):
    # Re-Write the date at chose do
    write_date(app)

@pibooth.hookimpl
def state_chosen_do(app):
    # Re-Write the date at chosen do
    write_date(app)

@pibooth.hookimpl
def state_preview_enter(app):
    # Re-Write the date at preview_do
    write_date(app)

@pibooth.hookimpl
def state_preview_do(app):
    # Re-Write the date at preview_do
    write_date(app)

@pibooth.hookimpl
def state_preview_validate(app):
    # Re-Write the date at preview_validate
    write_date(app)

@pibooth.hookimpl
def state_preview_exit(app):
    # Re-Write the date at preview_exit
    write_date(app)

@pibooth.hookimpl
def state_capture_enter(app):
    # Re-Write the date at capture_enter
    write_date(app)

@pibooth.hookimpl
def state_capture_do(app):
    # Re-Write the date at capture_do
    write_date(app)

@pibooth.hookimpl
def state_capture_validate(app):
    # Re-Write the date at capture_validate
    write_date(app)

@pibooth.hookimpl
def state_capture_exit(app):
    # Re-Write the date at capture_exit
    write_date(app)

@pibooth.hookimpl
def state_processing_enter(app):
    # Re-Write the date at processing_enter
    write_date(app)

@pibooth.hookimpl
def state_processing_do(app):
    # Re-Write the date at processing_do
    write_date(app)

@pibooth.hookimpl
def state_processing_validate(app):
    # Re-Write the date at processing_validate
    write_date(app)

@pibooth.hookimpl
def state_processing_exit(app):
    # Re-Write the date at processing_exit
    write_date(app)

@pibooth.hookimpl
def state_print_do(app):
    # Re-Write the date at print_do
    write_date(app)

@pibooth.hookimpl
def state_finish_do(app):
    # Re-Write the date at finish_do
    write_date(app)

@pibooth.hookimpl
def state_failsafe_do(app):
    # Re-Write the date at failsafe_do
    write_date(app)

@pibooth.hookimpl
def pibooth_cleanup(app):
    # Turn off backlight when pibooth close, close lcd screen
    if hasattr(app, 'lcd'):
        try:
            app.lcd.backlight_enabled=False
            app.lcd.close(clear=True)
        except OSError:
            pass
