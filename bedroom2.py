#!/usr/bin/python

import broadlink
import sys
import time

device_ip="10.0.0.138"
device_port=80
device_mac="aabbccddeeff"
device_type="broadlink.rmpro"

device = broadlink.rm(host=(device_ip,device_port), mac=bytearray.fromhex(device_mac))

device.auth()

device.host


codeData="e9263400260c0d230d23250b260c0d23250c0d24250c0e23250d0d24240c250c250c0d24250c0d24240c0c240d240c24250c0d240d00017000000000"
device.send_data(codeData.decode('hex'))

