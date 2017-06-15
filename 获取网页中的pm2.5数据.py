#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import urllib2
import re

#Domoticz服务器
domoticzserver = "127.0.0.1:8080"
#目标网页
url = 'http://www.pm25.com/beijing.html'

#此方法向Domoticz服务器发送请求
def domoticzrequest (url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return response.read()

#此方法用于提取字符串中的数字
def OnlyNum(s,oth=''):
    s2 = s.lower();
    fomart = '0123456789'
    for c in s2:
        if not c in fomart:
            s = s.replace(c,'');
    return s;


results = urllib2.urlopen(url).read()

#匹配目标数据的正则
#pm2.5浓度
data1 = re.findall(r"当前浓度\d+", results)
#空气质量指数
data2 = re.findall(r"指数为\d+", results)

#将pm2.5浓度发送到domoticz，需要修改idx值
domoticzrequest("http://"+domoticzserver+"/json.htm?type=command&param=udevice&idx=22&nvalue=0&svalue="+OnlyNum(data1[0]))

#将空气质量指数发送到domoticz
#domoticzrequest("http://"+domoticzserver+"/json.htm?type=command&param=udevice&idx=23&nvalue=0&svalue="+OnlyNum(data2[0]))
