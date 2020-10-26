# -*- coding: utf-8 -*-

"""Plugin to handle small LCD display."""

import time
import datetime
import pibooth
import textwrap
from RPLCD.i2c import CharLCD


__version__ = "1.0.6"

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('LCD_I2C', 'lcd_chip', "PCF8574", 
                   "Choose LCD chip - PCF8574(Default) or MCP23008 or MCP23017")
    cfg.add_option('LCD_I2C', 'lcd_port_address', "0x3F", 
                   "Port address 0x3F(Default)")
    cfg.add_option('LCD_I2C', 'lcd_port', "1", 
                   "The I2C port number 1(Default) or 2")
    cfg.add_option('LCD_I2C', 'lcd_charmap', "A02", 
                   "The I2C charmap A00 or A02(Default) or ST0B")
    cfg.add_option('LCD_I2C', 'lcd_cols', "16", 
                   "Number of columns per row 16(Default-LCD 16x2) or 20")
    cfg.add_option('LCD_I2C', 'lcd_rows', "2", 
                   "Number of display rows 1 or 2(Default-LCD 16x2) or 4")
                   # Text
    cfg.add_option('LCD_I2C', 'lcd_taken_photo_text', "Taken Photo", 
                   "Text before taken counter displayed Max-12 on 16x2 - Max 16 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_printed_text', "Printed", 
                   "Text before printed counter displayed Max-12 on 16x2 - Max 16 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_forgotten_text', "Forgotten", 
                   "Text before forgotten counter displayed Max-12 on 16x2 - Max 16 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_remaining_duplicates_text', "Duplicates", 
                   "Text before remaining_duplicates counter displayed Max-12 on 16x2 - Max 16 on 20x4")
                   # Free Text
    cfg.add_option('LCD_I2C', 'lcd_free_text1', "Free Text 1", 
                   "Free Text 1 - Max-16 on 16x2 - Max 20 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_free_text2', "Free Text 2", 
                   "Free Text 2 - Max-16 on 16x2 - Max 20 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_free_text3', "Free Text 3", 
                   "Free Text 3 - Max-16 on 16x2 - Max 20 on 20x4")
    cfg.add_option('LCD_I2C', 'lcd_free_text4', "Free Text 4", 
                   "Free Text 4 - Max-16 on 16x2 - Max 20 on 20x4")
                   # Line select
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
    cfg.add_option('LCD_I2C', 'lcd_free_text1_line', " ", 
                   "What line to display Free Text 1 ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")
    cfg.add_option('LCD_I2C', 'lcd_free_text2_line', " ", 
                   "What line to display Free Text 2 ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")
    cfg.add_option('LCD_I2C', 'lcd_free_text3_line', " ", 
                   "What line to display Free Text 3 ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")
    cfg.add_option('LCD_I2C', 'lcd_free_text4_line', " ", 
                   "What line to display Free Text 4 ((( FIRST LINE STARTS WITH 0, then 1,2,3 )))")


# 0=Taken_Photo, 2=Printed, 3=Forgotten, 4=Remaining_Duplicates, 1=Date/Time")

def write_date(app, cfg):
    """Method called to write the Date on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                e = app.date_time_line = cfg.get('LCD_I2C', 'lcd_date_time_line').strip('"')
                for e in (('%s' % app.date_time_line)):
                    if (e.isnumeric()) == True:
                        app.date_time_line = cfg.get('LCD_I2C', 'lcd_date_time_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.date_time_line), 0)
                        app.lcd.write_string('%s' % time.strftime('%d/%m - %H:%M:%S'))
        except OSError:
            pass
    
def write_photo_count(app, cfg):
    """Method called to write the Taken Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                a = app.taken_photo_line = cfg.get('LCD_I2C', 'lcd_taken_photo_line').strip('"')
                for a in (('%s' % app.taken_photo_line)):
                    if (a.isnumeric()) == True:
                        app.taken_photo_line = cfg.get('LCD_I2C', 'lcd_taken_photo_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.taken_photo_line), 0)
                        app.taken_photo_text = cfg.get('LCD_I2C', 'lcd_taken_photo_text').strip('"')
                        app.lcd.write_string(textwrap.shorten(('%s' % app.taken_photo_text), width=12, placeholder=""))
                        app.lcd.cursor_pos = (int('%s' % app.taken_photo_line), 12)
                        app.lcd.write_string(" "'%s' % app.count.taken)
        except OSError:
            pass

def write_printed_count(app, cfg):
    """Method called to write the Printed Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                b = app.printed_photo_line = cfg.get('LCD_I2C', 'lcd_printed_line').strip('"')
                for b in (('%s' % app.printed_photo_line)):
                    if (b.isnumeric()) == True:
                        app.printed_line = cfg.get('LCD_I2C', 'lcd_printed_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.printed_line), 0)
                        app.printed_text = cfg.get('LCD_I2C', 'lcd_printed_text').strip('"')
                        app.lcd.write_string(textwrap.shorten(('%s' % app.printed_text), width=12, placeholder=""))
                        app.lcd.cursor_pos = (int('%s' % app.printed_line), 12)
                        app.lcd.write_string(" "'%s' % app.count.printed)
        except OSError:
            pass

def write_forgotten_count(app, cfg):
    """Method called to write the Forgotten Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                c = app.forgotten_line = cfg.get('LCD_I2C', 'lcd_forgotten_line').strip('"')
                for c in (('%s' % app.forgotten_line)):
                    if (c.isnumeric()) == True:
                        app.forgotten_line = cfg.get('LCD_I2C', 'lcd_forgotten_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.forgotten_line), 0)
                        app.forgotten_text = cfg.get('LCD_I2C', 'lcd_forgotten_text').strip('"')
                        app.lcd.write_string(textwrap.shorten(('%s' % app.forgotten_text), width=12, placeholder=""))
                        app.lcd.cursor_pos = (int('%s' % app.forgotten_line), 12)
                        app.lcd.write_string(" "'%s' % app.count.forgotten)
        except OSError:
            pass

def write_remaining_duplicates_count(app, cfg):
    """Method called to write the Remaining Duplicates Photo on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                d = app.remaining_duplicates_line = cfg.get('LCD_I2C', 'lcd_remaining_duplicates_line').strip('"')
                for d in (('%s' % app.remaining_duplicates_line)):
                    if (d.isnumeric()) == True:
                        
                        app.remaining_line = cfg.get('LCD_I2C', 'lcd_remaining_duplicates_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.remaining_line), 0)
                        app.remaining_duplicates_text = cfg.get('LCD_I2C', 'lcd_remaining_duplicates_text').strip('"')
                        
                        app.lcd.write_string(textwrap.shorten(('%s' % app.remaining_duplicates_text), width=12, placeholder=""))
                        app.lcd.cursor_pos = (int('%s' % app.remaining_line), 12)
                        app.lcd.write_string(" "'%s' % app.count.remaining_duplicates)
        except OSError:
            pass

def write_free_text1(app, cfg):
    """Method called to write the Free-Text 1 on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                d = app.free_text1_line = cfg.get('LCD_I2C', 'lcd_free_text1_line').strip('"')
                for d in (('%s' % app.free_text1_line)):
                    if (d.isnumeric()) == True:
                        
                        app.free_text1_line = cfg.get('LCD_I2C', 'lcd_free_text1_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.free_text1_line), 0)
                        app.free_text1 = cfg.get('LCD_I2C', 'lcd_free_text1').strip('"')
                        app.lcd.write_string('%s' % app.free_text1)
        except OSError:
            pass

def write_free_text2(app, cfg):
    """Method called to write the Free-Text 2 on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                d = app.free_text2_line = cfg.get('LCD_I2C', 'lcd_free_text2_line').strip('"')
                for d in (('%s' % app.free_text2_line)):
                    if (d.isnumeric()) == True:
                        
                        app.free_text2_line = cfg.get('LCD_I2C', 'lcd_free_text2_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.free_text2_line), 0)
                        app.free_text2 = cfg.get('LCD_I2C', 'lcd_free_text2').strip('"')
                        app.lcd.write_string('%s' % app.free_text2)
        except OSError:
            pass

def write_free_text3(app, cfg):
    """Method called to write the Free-Text 3 on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                d = app.free_text3_line = cfg.get('LCD_I2C', 'lcd_free_text3_line').strip('"')
                for d in (('%s' % app.free_text3_line)):
                    if (d.isnumeric()) == True:
                        
                        app.free_text3_line = cfg.get('LCD_I2C', 'lcd_free_text3_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.free_text3_line), 0)
                        app.free_text3 = cfg.get('LCD_I2C', 'lcd_free_text3').strip('"')
                        app.lcd.write_string('%s' % app.free_text3)
        except OSError:
            pass
        
def write_free_text4(app, cfg):
    """Method called to write the Free-Text 4 on the screen
    """
    if hasattr(app, 'lcd'):
        try:
            if not "":
                d = app.free_text4_line = cfg.get('LCD_I2C', 'lcd_free_text4_line').strip('"')
                for d in (('%s' % app.free_text4_line)):
                    if (d.isnumeric()) == True:
                        
                        app.free_text4_line = cfg.get('LCD_I2C', 'lcd_free_text4_line').strip('"')
                        app.lcd.cursor_pos = (int('%s' % app.free_text4_line), 0)
                        app.free_text4 = cfg.get('LCD_I2C', 'lcd_free_text4').strip('"')
                        app.lcd.write_string('%s' % app.free_text4)
        except OSError:
            pass

def write_i2c(app, cfg):
    """I2c connect to lcd"""
    try:
        app.chip = cfg.get('LCD_I2C', 'lcd_chip').strip('"')
        app.address = cfg.get('LCD_I2C', 'lcd_port_address').strip('"')
        app.port = cfg.get('LCD_I2C', 'lcd_port').strip('"')
        app.charmap = cfg.get('LCD_I2C', 'lcd_charmap').strip('"')
        app.cols = cfg.get('LCD_I2C', 'lcd_cols').strip('"')
        app.rows = cfg.get('LCD_I2C', 'lcd_rows').strip('"')
        app.lcd = CharLCD(i2c_expander='%s' % app.chip, address=int('%s' % app.address, 16),
                          port=int('%s' % app.port), charmap=('%s' % app.charmap),
                          cols=int('%s' % app.cols), rows=int('%s' % app.rows),
                          backlight_enabled=True)
    except OSError:
        pass

@pibooth.hookimpl
def pibooth_startup(app, cfg):
    write_i2c(app, cfg)
    # app.lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, auto_linebreak=False, backlight_enabled=False)
    
    # Re-write the number of taken photo each time pibooth
    # startup.
    write_photo_count(app, cfg)

    # Re-write the number of printed pictures each time pibooth
    # startup.
    write_printed_count(app, cfg)
        
    # Re-Write the number of forgotten pictures at pibooth
    # startup
    write_forgotten_count(app, cfg)

    # Re-Write the number of remaining_duplicates at pibooth
    # startup
    write_remaining_duplicates_count(app, cfg)

    # Re-Write the date/time at pibooth
    # startup
    write_date(app, cfg)
    
    # Write Free-Text 1
    # startup.
    write_free_text1(app, cfg)
    
    # Write Free-Text 2
    # startup.
    write_free_text2(app, cfg)
    
    # Write Free-Text 3
    # startup.
    write_free_text3(app, cfg)
    
    # Write Free-Text 4
    # startup.
    write_free_text4(app, cfg)

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    write_i2c(app, cfg)
    # Re-write the number of taken pictures each time pibooth
    # enter in 'wait' state.
    write_photo_count(app, cfg)

    # Re-write the number of printed pictures each time pibooth
    # enter in 'wait' state.
    write_printed_count(app, cfg)
        
    # Re-Write the number of forgotten pictures at pibooth
    # enter in 'wait' state.
    write_forgotten_count(app, cfg)

    # Re-Write the number of remaining_duplicates at pibooth
    # enter in 'wait' state.
    write_remaining_duplicates_count(app, cfg)

    # Re-Write the date at pibooth
    # enter in 'wait' state.
    write_date(app, cfg)
    
    # Write Free-Text 1
    # enter in 'wait' state.
    write_free_text1(app, cfg)
    
    # Write Free-Text 2
    # enter in 'wait' state.
    write_free_text2(app, cfg)
    
    # Write Free-Text 3
    # enter in 'wait' state.
    write_free_text3(app, cfg)
    
    # Write Free-Text 4
    # enter in 'wait' state.
    write_free_text4(app, cfg)

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
    if hasattr(app, 'lcd'):
        try:
            app.lcd.backlight_enabled=False
            app.lcd.close(clear=True)
        except OSError:
            pass
