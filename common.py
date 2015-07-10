#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import re
import urllib2
import os
import hashlib
import time
import cookielib 
import StringIO
import gzip

def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)

def getHtml(url): 
    r=urllib2.Request(url)
    r.add_header("Accept-Language","zh-cn,en-us;q=0.7,en;q=0.3")
    r.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.2; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0")
    try:
        content=urllib2.urlopen(r, timeout=2).read()
        time.sleep(0.3)
        return content
    except:
        return None
    
def getHtmlwithGoogleCookie(url): 
    cookiejar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    opener.addheaders = [('Host', 'www.google.com.hk'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'),
                         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
                         ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                         ('Referer', 'https://www.google.com.hk/search?q=%E6%9E%AA&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:zh-CN:official&client=firefox-a&channel=fflb&gws_rd=ssl')]    
    try:
        content=opener.open(url).read()
        time.sleep(0.3)
        return content
    except:
        return None
    
def getTextwithGoogleCookie(url):
    cookiejar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    opener.addheaders = [('Host', 'www.google.com.hk'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0'),
                         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
                         ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                         ('Accept-Encoding',  'gzip, deflate'),  
                         ('Referer','https://www.google.com.hk/search?q=%E8%AF%81%E4%BB%B6%E7%85%A7&newwindow=1&safe=strict&tbm=isch&tbo=u&source=univ&sa=X&ei=KRb9VML_D8LlmAWy1oGoCA&ved=0CBwQsAQ&biw=1440&bih=761'),
                         ('Cookie','PREF=ID=42e7dea4368f1af9:U=8e996a8daf43b08c:FF=1:LD=zh-CN:NW=1:TM=1422263659:LM=1425872444:S=91wJ4yp3nwNyUwCt; NID=67=PPFhvcW6OZ493EKySKb1JVU_jvSXx5RPfr7eVotL6b7id5Y9hJmN1aNMKjr-D10S8phMSRvxEhvnPDrTTcCofB9FbetNOtdpiVmbmre_LK8S-LY9GemD286MLPNg9rkl'),                       
                         ('Connection', 'keep-alive')]   
    try:
        response = opener.open(url)
        if response.info().get('Content-Encoding') == 'gzip':
            compressedstream = StringIO.StringIO( response.read())
            time.sleep(0.3)
            f = gzip.GzipFile(fileobj=compressedstream)
            content = f.read() 
            return content
        else:
            content=response.read()
            time.sleep(0.3)
            return content
    except:
        return None
    
def getHtmlwithBaiduCookie(url): 
    cookiejar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    opener.addheaders = [('Host', 'image.baidu.com'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'),
                         ('Accept', 'text/plain, */*; q=0.01'), 
                         ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                         ('Accept-Encoding' ,'gzip, deflate'),
                         ('X-Requested-With','XMLHttpRequest'),
                         ('Referer', 'http://image.baidu.com/i?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&word=%E6%9E%AA&ie=utf-8&ie=utf-8&ie=utf-8')]    
    try:
        response = opener.open(url)
        if response.info().get('Content-Encoding') == 'gzip':
            compressedstream = StringIO.StringIO( response.read())
            time.sleep(0.3)
            f = gzip.GzipFile(fileobj=compressedstream)
            content = f.read() 
            return content
        else:
            content=response.read()
            time.sleep(0.3)
            return content
    except:
        return None    
    
def filewriteb(filepath, content):
    if os.path.isfile(filepath):
        return
    fp = open(filepath, 'wb')
    fp.write(content)
    fp.close()

def md5(content):
    if not content:
        return None
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()

if __name__ == "__main__":
    url = 'http://movie.douban.com/subject_search?search_text=Hello Dolly&cat=1002'
    print getHtml(url)