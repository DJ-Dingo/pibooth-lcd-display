# -*- coding: utf-8 -*-


"""Plugin to handle small LCD display."""

import time
import datetime
import pibooth
from RPLCD.i2c import CharLCD


__version__ = "1.0.2"

def write_date(app):
    """Method called to write the date on the screen
    """
    try:
        app.lcd.cursor_pos = (1, 0)
        app.lcd.write_string('%s' % time.strftime('%d/%m - %H:%M:%S'))
    except OSError:
        pass
    
def write_photo_count(app):
    """Method called to clear LCD and write the date on the screen
    """
    try:
        app.lcd.clear()
        app.lcd.cursor_pos = (0, 0)
        app.lcd.write_string('Today Photos %s' % app.count.taken)
    except OSError:
        pass

@pibooth.hookimpl
def pibooth_startup(app):
    app.lcd = CharLCD('PCF8574', 0x3F)
    # app.lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, auto_linebreak=False, backlight_enabled=False)
    # Re-write the number of taken pictures each time pibooth
    # startup.
    write_photo_count(app)
    # Re-Write the date at pibooth startup
    write_date(app)

@pibooth.hookimpl
def state_wait_enter(app):
    # Re-write the number of taken pictures each time pibooth
    # enter in 'wait' state.
    write_photo_count(app)
    # Re-Write the date each time piboot enters in 'wait' state.
    write_date(app)

@pibooth.hookimpl
def state_wait_do(app):
    # Re-Write the date at 'wait' do
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
def state_preview_do(app):
    # Re-Write the date at preview_do
    write_date(app)

@pibooth.hookimpl
def state_capture_do(app):
    # Re-Write the date at capture_do
    write_date(app)

@pibooth.hookimpl
def state_processing_do(app):
    # Re-Write the date at processing_do
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
    # """ This could be an option as it can be nice to see what time pibooth was shut down
    #     as it stops time and still shows the last time pibooth has been running """
    if hasattr(app, 'lcd'):
        try:
            app.lcd.backlight_enabled=False
            app.lcd.close(clear=True)
        except OSError:
            pass
