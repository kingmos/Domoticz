#           DT27 Getting AQI Python Plugin for Domoticz
#
#           Dev. Platform : Win10 x64 & Py 3.5.0 x86
#
#           Author:     Zack, 2017
#           1.0.0:  code compatible py  3.x


# Below is what will be displayed in Domoticz GUI under HW
#
"""
<plugin key="DT27-AQI" name="DT27-AQI" author="Zack" version="1.0.0" externallink="http://www.pm25.com/">
    <params>
        <param field="Address" label="城市" width="80px" required="true" default="上海"/>
        <param field="Mode1" label="监测点" width="120px" required="true" default="浦东张江"/>
        <param field="Mode2" label="更新频率(分钟)" width="30px" required="true" default="60"/>
    </params>
</plugin>
"""
#
# Main Import
import Domoticz
import urllib.parse
import urllib.request
import re


#Target URI
AQI_URI = "http://www.pm25.com/city/mon/aqi/{}/{}.html"
PM25_URI = "http://www.pm25.com/city/mon/pm2_5/{}/{}.html"
PM10_URI = "http://www.pm25.com/city/mon/pm10/{}/{}.html"

# Domoticz call back functions
#

# Executed once at HW creation/ update. Can create up to 255 devices.
def onStart():
	Domoticz.Debugging(1)

	repeatTime = int(Parameters["Mode2"]) * 60

	if ( 1 not in Devices):  
		Domoticz.Device(Name=Parameters["Address"] + "空气指数",  Unit=1, TypeName="Custom", Options={"Custom":"1;AQI"}, Used=1).Create()

	if ( 2 not in Devices):
		Domoticz.Device(Name=Parameters["Address"] + "PM2.5浓度",  Unit=2, TypeName="Custom", Options={"Custom":"1;μg/m³"}, Used=1).Create()

	if ( 3 not in Devices): 
		Domoticz.Device(Name=Parameters["Address"] + "PM10浓度",  Unit=3, TypeName="Custom", Options={"Custom":"1;μg/m³"}, Used=1).Create()

	Domoticz.Heartbeat(repeatTime)

	return True

def onMessage(Data, Status, Extra):    
    Domoticz.Log('onMessage: '+str(Data)+" ,"+str(Status)+" ,"+str(Extra))    
    return True

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):

    Domoticz.Log("Notification: " + str(Name))

    return

# execution depend of Domoticz.Heartbeat(x) x in seconds
def onHeartbeat():
    aqi = getAirQuality(AQI_URI)
    UpdateDevice(1,0,aqi)

    pm25 = getAirQuality(PM25_URI)
    UpdateDevice(2,0,pm25)

    pm10 = getAirQuality(PM10_URI)
    UpdateDevice(3,0,pm10)

    return True

def getAirQuality(url):
	url = urllib.parse.quote_plus(url.format(Parameters["Address"], Parameters["Mode1"]),safe='http://')
	results=urllib.request.urlopen(url).read().decode('utf-8')
	data = re.findall(r"data:[[\d+,]+]", results)
	data = data[0]
	l24 = data.split(',')
	airquality=onlyNum(l24[23],oth='')
	return airquality

def onlyNum(s,oth=''):
    s2 = s.lower();
    fomart = '0123456789'
    for c in s2:
        if not c in fomart:
            s = s.replace(c,'');
    return s;

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