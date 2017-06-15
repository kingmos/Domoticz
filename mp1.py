#!/usr/bin/python
# -*- coding: UTF-8 -*-

import broadlink
import sys

device_ip="博联设备IP"
device_port=80
device_mac="博联设备mac地址"
device_type="broadlink.mp1"

socket = str(sys.argv[1])
action = str(sys.argv[2])

device = broadlink.mp1(host=(device_ip,device_port), mac=bytearray.fromhex(device_mac))

device.auth()
#device.host

if action == "on":
	if socket == "s1":
		device.set_power(1,True)
	elif socket == "s2":
		device.set_power(2,True)
        elif socket == "s3":
                device.set_power(3,True)
        elif socket == "s4":
                device.set_power(4,True)
elif action == "off":
        if socket == "s1":
                device.set_power(1,False)
        elif socket == "s2":
                device.set_power(2,False)
        elif socket == "s3":
                device.set_power(3,False)
        elif socket == "s4":
                device.set_power(4,False)
elif action == "status":
        print "on" if device.check_power()[socket] else "off"
