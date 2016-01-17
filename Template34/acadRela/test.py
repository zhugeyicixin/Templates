# -*- coding:utf-8 -*-
import urllib
import urllib2
 
 
page = 1
url = 'http://www.sciencedirect.com/science/article/pii/S0010218003001615'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    print response.read()
    fw = file('test9.html','w')
    fw.write(response.read())
    fw.close()
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason