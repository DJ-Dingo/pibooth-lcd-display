# -*- coding: utf-8 -*-

"""Plugin to handle small LCD display."""

import time
import datetime
import pibooth
from RPLCD.i2c import CharLCD

__version__ = "1.0.4"

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('LCD_I2C', 'lcd_chip', "PCF8574", 
                   "Choose LCD chip - PCF8574(Default) or MCP23008 or MCP23017")
    cfg.add_option('LCD_I2C', 'lcd_port_address', "0x3F", 
                   "Port address 0x3F(Default)")
    cfg.add_option('LCD_I2C', 'lcd_port', "1", 
                   "The I2C port number 1(Default) or 2")
    cfg.add_option('LCD_I2C', 'lcd_cols', "16", 
                   "Number of columns per row 16(Default-LCD 16x2) or 20")
    cfg.add_option('LCD_I2C', 'lcd_rows', "2", 
                   "Number of display rows 1 or 2(Default-LCD 16x2) or 4")
    cfg.add_option('LCD_I2C', 'lcd_taken_photo_text', "Taken Photo", 
                   "Text before taken counter displayed Max-12 on 16x2 - Max 16 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_printed_text', "Printed", 
                   "Text before printed counter displayed Max-12 on 16x2 - Max 16 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_forgotten_text', "Forgotten", 
                   "Text before forgotten counter displayed Max-12 on 16x2 - Max 16 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_remaining_duplicates_text', "Duplicates", 
                   "Text before remaining_duplicates counter displayed Max-12 on 16x2 - Max 16 on 20x4")

    cfg.add_option('LCD_I2C', 'lcd_taken_photo_line', "0", 
                   "What line to display taken photo ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")
    cfg.add_option('LCD_I2C', 'lcd_date_time_line', "1", 
                   "What line to display date/time ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")
    cfg.add_option('LCD_I2C', 'lcd_printed_line', " ", 
                   "What line to display printed photo ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")
    cfg.add_option('LCD_I2C', 'lcd_forgotten_line', " ", 
                   "What line to display forgotten photo ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")
    cfg.add_option('LCD_I2C', 'lcd_remaining_duplicates_line', " ", 
                   "What line to display remaining_duplicates ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")

# 0=Taken_Photo, 2=Printed, 3=Forgotten, 4=Remaining_Duplicates, 1=Date/Time")

def write_date(app, cfg):
    """Method called to write the Date on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            app.date_time_line = cfg.get('LCD_I2C', 'lcd_date_time_line').strip('"')
            app.lcd.cursor_pos = (int('%s' % app.date_time_line), 0)
            app.lcd.write_string('%s' % time.strftime('%d/%m - %H:%M:%S'))
        except OSError:
            pass
    
def write_photo_count(app, cfg):
    """Method called to clear LCD and write the Taken Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            app.lcd.clear()
            app.taken_photo_line = cfg.get('LCD_I2C', 'lcd_taken_photo_line').strip('"')
            app.lcd.cursor_pos = (int('%s' % app.taken_photo_line), 0)
            app.taken_photo_text = cfg.get('LCD_I2C', 'lcd_taken_photo_text').strip('"')
            app.lcd.write_string('%s' % app.taken_photo_text)
            app.lcd.cursor_pos = (int('%s' % app.taken_photo_line), 12)
            app.lcd.write_string(" "'%s' % app.count.taken)
        except OSError:
            pass

def write_printed_count(app, cfg):
    """Method called to clear LCD and write the Printed Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            app.lcd.clear()
            app.lcd.cursor_pos = (0, 0)
            app.printed_text = cfg.get('LCD_I2C', 'lcd_printed_text').strip('"')
            app.lcd.write_string('%s' % app.printed_text)
            app.lcd.cursor_pos = (0, 12)
            app.lcd.write_string(" "'%s' % app.count.printed)
            #  + " " '%s' % app.count.taken
        except OSError:
            pass

def write_forgotten_count(app, cfg):
    """Method called to clear LCD and write the Forgotten Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            app.lcd.clear()
            app.lcd.cursor_pos = (0, 0)
            app.forgotten_text = cfg.get('LCD_I2C', 'lcd_forgotten_text').strip('"')
            app.lcd.write_string('%s' % app.forgotten_text)
            app.lcd.cursor_pos = (0, 12)
            app.lcd.write_string(" "'%s' % app.count.forgotten)
        except OSError:
            pass

def write_remaining_duplicates_count(app, cfg):
    """Method called to clear LCD and write the Remaining Duplicates Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            app.lcd.clear()
            app.lcd.cursor_pos = (0, 0)
            app.remaining_duplicates_text = cfg.get('LCD_I2C', 'lcd_remaining_duplicates_text').strip('"')
            app.lcd.write_string('%s' % app.remaining_duplicates_text)
            app.lcd.cursor_pos = (0, 12)
            app.lcd.write_string(" "'%s' % app.count.remaining_duplicates)
        except OSError:
            pass


def i2c(app, cfg):
    """I2c connect to lcd"""
    try:
        app.chip = cfg.get('LCD_I2C', 'lcd_chip').strip('"')
        app.address = cfg.get('LCD_I2C', 'lcd_port_address').strip('"')
        app.port = cfg.get('LCD_I2C', 'lcd_port').strip('"')
        app.cols = cfg.get('LCD_I2C', 'lcd_cols').strip('"')
        app.rows = cfg.get('LCD_I2C', 'lcd_rows').strip('"')
        app.lcd = CharLCD(i2c_expander='%s' % app.chip, address=int('%s' % app.address, 16),
                          port=int('%s' % app.port), cols=int('%s' % app.cols),
                          rows=int('%s' % app.rows), backlight_enabled=True)
    except OSError:
        pass
        
@pibooth.hookimpl
def pibooth_startup(app, cfg):
    i2c(app, cfg)
    # app.lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, auto_linebreak=False, backlight_enabled=False)
    # Re-write the number of taken pictures each time pibooth
    # startup.
    write_photo_count(app, cfg)
    # Re-write the number of printed pictures each time pibooth
    # startup.
    #write_printed_count(app, cfg)
    # Re-Write the date at pibooth startup
    write_date(app, cfg)

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    i2c(app, cfg)
    # Re-write the number of taken pictures each time pibooth
    # enter in 'wait' state.
    write_photo_count(app, cfg)
    # Re-write the number of printed pictures each time pibooth
    # enter in 'wait' state.
    #write_printed_count(app, cfg)
    # Re-Write the date each time piboot enters in 'wait' state.
    write_date(app, cfg)

@pibooth.hookimpl
def state_wait_do(app, cfg):
    # Re-Write the date at 'wait' do
    write_date(app, cfg)

@pibooth.hookimpl
def state_choose_do(app, cfg):
    # Re-Write the date at chose do
    write_date(app, cfg)

@pibooth.hookimpl
def state_chosen_do(app, cfg):
    # Re-Write the date at chosen do
    write_date(app, cfg)

@pibooth.hookimpl
def state_preview_do(app, cfg):
    # Re-Write the date at preview_do
    write_date(app, cfg)

@pibooth.hookimpl
def state_capture_do(app, cfg):
    # Re-Write the date at capture_do
    write_date(app, cfg)

@pibooth.hookimpl
def state_processing_do(app, cfg):
    # Re-Write the date at processing_do
    write_date(app, cfg)

@pibooth.hookimpl
def state_print_do(app, cfg):
    # Re-Write the date at print_do
    write_date(app, cfg)

@pibooth.hookimpl
def state_finish_do(app, cfg):
    # Re-Write the date at finish_do
    write_date(app, cfg)

@pibooth.hookimpl
def state_failsafe_do(app, cfg):
    # Re-Write the date at failsafe_do
    write_date(app, cfg)

@pibooth.hookimpl
def pibooth_cleanup(app):
    # Turn off backlight when pibooth close, close lcd screen
    # """ This could be an option as it can be nice to see what time pibooth was shut down
    #     as it stops time and still shows the last time pibooth has been running """
    if hasattr(app, 'lcd'):
        try:
            app.lcd.backlight_enabled=False
            app.lcd.close(clear=True)
        except OSError:
            pass
