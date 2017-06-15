#           Broadlink SP Mini Switch Python Plugin for Domoticz
#
#           Dev. Platform : Win10 x64 & Py 3.5.0 x86
#
#           Author:     Zack, 2017
#           1.0.0:  code compatible py  3.x


# Below is what will be displayed in Domoticz GUI under HW
#
"""
<plugin key="BroadlinkSPmini" name="Broadlink SP-mini" author="Zack" version="1.0.0">
    <params>
        <param field="Address" label="IP" width="100px" required="true" default=""/>
        <param field="Mode1" label="Mac" width="100px" required="true" default="000000000000"/>
        <param field="Mode2" label="检测间隔(秒)" width="40px" required="true" default="30"/>
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

#
import broadlink


isConnected = False




# Domoticz call back functions
#

# Executed once at HW creation/ update. Can create up to 255 devices.
def onStart():
	#Domoticz.Debugging(1)

	if ( 1 not in Devices):  
		Domoticz.Device(Name="SP mini",  Unit=1, TypeName="Switch", Used=1).Create()

	Domoticz.Heartbeat(int(Parameters["Mode2"]))

	return True

def onMessage(Data, Status, Extra):    
    Domoticz.Log('onMessage: '+str(Data)+" ,"+str(Status)+" ,"+str(Extra))    
    return True

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):

    Domoticz.Log("Notification: " + str(Name))

    return

# executed each time we click on device thru domoticz GUI
def onCommand(Unit, Command, Level, Hue):

    if Command == 'On':
    	if broadlinkConnect():
    		device.set_power(True)
    elif Command == 'Off':
    	if broadlinkConnect():
    		device.set_power(False)
    else:
        Domoticz.Error('Unknown command')

    checkState()
    
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
        device = broadlink.sp2(host=(Parameters["Address"],80), mac=bytearray.fromhex(Parameters["Mode1"]))
        device.auth()
        isConnected = True
        Domoticz.Log( "Connected to Broadlink device.")        
    except Exception as e:
        Domoticz.Error( "Error Connecting to Broadlink device.... " + str(e))
        isConnected = False
        return False

    return True