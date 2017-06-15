#           Broadlink MP1 Python Plugin for Domoticz
# 
#           Py Author: blindlight,DT27
#
#           Script Author:Zack, Thanks Zack for script！ 
# 
#           Dev. Platform : Win10 x64 & Py 3.5.0 x86   ??
#
#           Author:     Kingmos     2017
# 
#           0.0.1:  code compatible py  XXX


# Below is what will be displayed in Domoticz GUI under HW
#
"""
<plugin key="BroadLinkMP" name="BroadLinkMP" author="Kingmos" version="0.0.1" wikilink="https://www.domoticz.cn/forum/viewtopic.php?f=33&t=22"  externallink="https://www.domoticz.cn/forum/viewtopic.php?f=33&t=22">
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Mode1" label="Mac" width="100px" required="true" default="000000000000"/>
        <param field="Mode2" label="Device name" width="300px" required="true" default="BroadlinkMP"/>
        <param field="Mode3" label="检测间隔(秒)" width="40px" required="true" default="30"/>

    </params>
</plugin>
"""
#
# Main Import
import Domoticz
import sys
import os 

if sys.platform.startswith('linux'):
    # linux specific code here
    sys.path.append(os.path.dirname(os.__file__) + '/dist-packages')
elif sys.platform.startswith('darwin'):
    # mac
    sys.path.append(os.path.dirname(os.__file__) + '/site-packages')
elif sys.platform.startswith('win32'):
    #  win specific
    sys.path.append(os.path.dirname(os.__file__) + '\site-packages')

import broadlink

isConnected = False

# Domoticz call back functions

# Executed once at HW creation/ update. Can create up to 255 devices.
def onStart():
	#Domoticz.Debugging(1)

	if ( 1 not in Devices):  
		Domoticz.Device(Name="S1",  Unit=1, TypeName="Switch", Used=1).Create()

	if ( 2 not in Devices):  
		Domoticz.Device(Name="S2",  Unit=2, TypeName="Switch", Used=1).Create()

	if ( 3 not in Devices):  
		Domoticz.Device(Name="S3",  Unit=3, TypeName="Switch", Used=1).Create()

	if ( 4 not in Devices):  
		Domoticz.Device(Name="S4",  Unit=4, TypeName="Switch", Used=1).Create()		

	Domoticz.Heartbeat(int(Parameters["Mode3"]))

	return True

def onMessage(Data, Status, Extra):    
    Domoticz.Log('onMessage: '+str(Data)+" ,"+str(Status)+" ,"+str(Extra))    
    return True

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):

    Domoticz.Log("Notification: " + str(Name))

    return

# executed each time we click on device thru domoticz GUI
def onCommand(Unit, Command, Level, Hue):

        if （Unit ==  1）:
            if Command == 'On':
            	if broadlinkConnect():
                	device.set_power(1,True)
            elif Command == 'Off':
            	if broadlinkConnect():
            		device.set_power(1,False)
            else:
                Domoticz.Error('Unknown command')
            checkState()

        elif （Unit ==  2）:
            if Command == 'On':
            	if broadlinkConnect():
                	device.set_power(2,True)
            elif Command == 'Off':
            	if broadlinkConnect():
            		device.set_power(2,False)
            else:
                Domoticz.Error('Unknown command')
            checkState()

        elif（Unit ==  3）:
            if Command == 'On':
            	if broadlinkConnect():
                	device.set_power(3,True)
            elif Command == 'Off':
            	if broadlinkConnect():
            		device.set_power(3,False)
            else:
                Domoticz.Error('Unknown command')
            checkState()

        elif （Unit ==  4）:
            if Command == 'On':
            	if broadlinkConnect():
                	device.set_power(4,True)
            elif Command == 'Off':
            	if broadlinkConnect():
            		device.set_power(4,False)
            else:
                Domoticz.Error('Unknown command')
            checkState()
        else:
                Domoticz.Error('Unknown command')
    
        return True

# execution depend of Domoticz.Heartbeat(x) x in seconds
def onHeartbeat():

	checkState()

	return True


def onDisconnect():
    Domoticz.Log("onDisconnect called")
    return

# executed once when HW updated/removed
def onStop():
    Domoticz.Log("onStop called")
    return True



# Update Device into DB
def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue))
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return

# Update Device UpdateDevice(1,1,"On")  UpdateDevice(1,0,"Off")

def checkState():
	if broadlinkConnect():
		state = device.check_power();
		if state:
			UpdateDevice(1,1,"On")
		else:
			UpdateDevice(1,0,"Off")

# connect to Broadlink
def broadlinkConnect():
    global device, isConnected

    if isConnected:
    	return True

    try:
        device = broadlink.mp1(host=(Parameters["Address"],80), mac=bytearray.fromhex(Parameters["Mode1"]))
        device.auth()
        device.host
        isConnected = True
        Domoticz.Log( "Connected to Broadlink device.")        
    except Exception as e:
        Domoticz.Error( "Error Connecting to Broadlink device.... " + str(e))
        isConnected = False
        return False

    return True
