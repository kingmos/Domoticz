#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 中国天气数据

import urllib2
import re

#Domoticz服务器
domoticzserver = "127.0.0.1:8080"
#今日天气idx
today_idx = "49"
#明日天气idx
tomorrow_idx = "48"
#地区编号，来源：http://www.weather.com.cn/weather/101120501.shtml
area = "101120501"

#此方法向Domoticz服务器发送请求
def domoticzrequest (url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return response.read()

'''
当日天气预报
'''

'''
day1_url = "http://d1.weather.com.cn/weather_index/"+area+".html"

#伪造来源Referer
header = {
    'Host':'d1.weather.com.cn',
    'Referer':'http://www.weather.com.cn/',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:45.0) Gecko/20100101 Firefox/45.0'
}
day1_req = urllib2.Request(day1_url,headers=header)
day1_response = urllib2.urlopen(day1_req)
day1_result = day1_response.read()
#汉字编码转换
day1_result = day1_result.decode('utf8')

# Temp + Humidity + Baro 25.9 C, 35 %, 1014 hPa
# Wind 91.00;E;45;0;25.9;25.9
# Rain 0;0.0
# Solar Radiation 305.2 Watt/m2

#天气预报，阴转阵雨
weather = re.findall(u'"weather":"([\u4e00-\u9fa5]+)"', day1_result)
#获取天气
weather = re.findall(u'"weather":"([\u4e00-\u9fa5]+)"', day1_result)
#当前温度
tempture = re.findall(u'"temp":"\d+","tempf"', day1_result)
#
'''

'''
七日预报
'''
weather_url = "http://www.weather.com.cn/weather/"+area+".shtml"
weather_response = urllib2.urlopen(weather_url)
weather_result = weather_response.read()

# 七日预报结果
# 天气,weathers[0-6]
weathers = re.findall(u'title="(.*)" class="wea">',weather_result)
# 高低温度,temps[0-6][0-1]
temps = re.findall(u'<span>(\d+)</span>/<i>(\d+)',weather_result)

#今日,weathers[0]
domoticzrequest("http://"+domoticzserver+"/json.htm?type=command&param=udevice&idx="+today_idx+"&nvalue=0&svalue="+weathers[0]+","+temps[0][0]+"/"+temps[0][1]+"℃")

#明日,weathers[1]
domoticzrequest("http://"+domoticzserver+"/json.htm?type=command&param=udevice&idx="+tomorrow_idx+"&nvalue=0&svalue="+weathers[1]+","+temps[1][0]+"/"+temps[1][1]+"℃")

