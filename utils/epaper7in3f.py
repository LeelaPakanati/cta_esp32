"""
MicroPython Waveshare 7.5" Black/White/Red GDEW075Z09 e-paper display driver
https://github.com/mcauser/micropython-waveshare-epaper

MIT License
Copyright (c) 2017 Waveshare
Copyright (c) 2018 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# also works for black/white/yellow GDEW075C21?

from micropython import const
from time import sleep_ms
import ustruct

# Display resolution
EPD_WIDTH  = const(800)
EPD_HEIGHT = const(480)

# Display commands
PANEL_SETTING                  = const(0x00)
POWER_SETTING                  = const(0x01)
POWER_OFF                      = const(0x02)
POWER_OFF_SEQUENCE_SETTING     = const(0x03)
POWER_ON                       = const(0x04)
POWER_ON_MEASURE               = const(0x05)
BOOSTER_SOFT_START             = const(0x06)
DEEP_SLEEP                     = const(0x07)
DATA_START_TRANSMISSION_1      = const(0x10)
#DATA_STOP                      = const(0x11)
DISPLAY_REFRESH                = const(0x12)
IMAGE_PROCESS                  = const(0x13)
#LUT_FOR_VCOM                   = const(0x20)
#LUT_BLUE                       = const(0x21)
#LUT_WHITE                      = const(0x22)
#LUT_GRAY_1                     = const(0x23)
#LUT_GRAY_2                     = const(0x24)
#LUT_RED_0                      = const(0x25)
#LUT_RED_1                      = const(0x26)
#LUT_RED_2                      = const(0x27)
#LUT_RED_3                      = const(0x28)
#LUT_XON                        = const(0x29)
PLL_CONTROL                    = const(0x30)
#TEMPERATURE_SENSOR_COMMAND     = const(0x40)
TEMPERATURE_CALIBRATION        = const(0x41)
#TEMPERATURE_SENSOR_WRITE       = const(0x42)
#TEMPERATURE_SENSOR_READ        = const(0x43)
VCOM_AND_DATA_INTERVAL_SETTING = const(0x50)
#LOW_POWER_DETECTION            = const(0x51)
TCON_SETTING                   = const(0x60)
TCON_RESOLUTION                = const(0x61)
#SPI_FLASH_CONTROL              = const(0x65)
#REVISION                       = const(0x70)
#GET_STATUS                     = const(0x71)
#AUTO_MEASUREMENT_VCOM          = const(0x80)
#READ_VCOM_VALUE                = const(0x81)
VCM_DC_SETTING                 = const(0x82)
AGID                           = const(0x86)
CCSET                          = const(0xE0)
TSSET                          = const(0xE6)
CDMH                           = const(0xAA)
FLASH_MODE                     = const(0xE5)

BUSY = const(0)  # 0=busy, 1=idle

class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init(self):
        self.reset()
        self._command(CDMH, b'\x49\x55\x20\x08\x09\x18')
        self._command(POWER_SETTING, b'\x3F\x00\x32\x2A\x0E\x2A')
        self._command(PANEL_SETTING, b'\x5F\x69')
        self._command(POWER_OFF_SEQUENCE_SETTING, b'\x00\x54\x00\x44')
        self._command(POWER_ON_MEASURE, b'\x40\x1F\x1F\x2C')
        self._command(BOOSTER_SOFT_START, b'\x6F\x1f\x1f\x22')
        self._command(IMAGE_PROCESS, b'\x00\x04')
        self._command(PLL_CONTROL, b'\x3C')
        self._command(TEMPERATURE_CALIBRATION, b'\x00')
        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x3F')
        self._command(TCON_SETTING, b'\x02\x00')
        self._command(TCON_RESOLUTION, '\x03\x20\x01\xE0')
        self._command(VCM_DC_SETTING, b'\x1E')
        self._command(0x84, b'\x00')
        self._command(AGID, b'\x00')
        self._command(0xE3, b'\x2F')
        self._command(CCSET, b'\x00')
        self._command(TSSET, b'\x00')
        
        self._command(POWER_ON)
        self.wait_until_idle()
        self._command(DISPLAY_REFRESH, b'\x00')
        self.wait_until_idle()
        self._command(POWER_OFF, b'\x00')
        self.wait_until_idle()

    def wait_until_idle(self):
        while self.busy.value() == BUSY:
            sleep_ms(100)

    def reset(self):
        self.rst(0)
        sleep_ms(200)
        self.rst(1)
        sleep_ms(200)

    # draw the current frame memory
    def display_frame(self, frame_buffer, size):
        self._command(DATA_START_TRANSMISSION_1)
        for i in range(0, size):
            temp1 = frame_buffer[i]
            j = 0
            while (j < 4):
                if ((temp1 & 0xC0) == 0xC0):
                    temp2 = 0x03
                elif ((temp1 & 0xC0) == 0x00):
                    temp2 = 0x00
                else:
                    temp2 = 0x04
                temp2 = (temp2 << 4) & 0xFF
                temp1 = (temp1 << 2) & 0xFF
                j += 1
                if ((temp1 & 0xC0) == 0xC0):
                    temp2 |= 0x03
                elif ((temp1 & 0xC0) == 0x00):
                    temp2 |= 0x00
                else:
                    temp2 |= 0x04
                temp1 = (temp1 << 2) & 0xFF
                self._data(bytearray([temp2]))
                j += 1
        self._command(DISPLAY_REFRESH)
        sleep_ms(100)
        self.wait_until_idle()

    def fill_frame(self, byte):
        self._command(DATA_START_TRANSMISSION_1)
        for i in range(0, self.width*self.height//2):
            self._data(byte)
        self._command(DISPLAY_REFRESH)
        sleep_ms(100)
        self.wait_until_idle()



    # to wake call reset() or init()
    def sleep(self):
        self._command(POWER_OFF)
        self.wait_until_idle()
        self._command(DEEP_SLEEP, b'\xA5')
