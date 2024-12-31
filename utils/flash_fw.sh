#!/usr/bin/sh

esptool.py --chip esp32 --port $1 erase_flash
esptool.py --chip esp32 --port $1 --baud 460800 write_flash -z 0x1000 "./utils/ESP32_GENERIC-20241129-v1.24.1.bin"
