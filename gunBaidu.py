#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-10-26

@author: JohnDannl

usage:

<1 replace the keywords in __main__

<2 commented out the last two lines,run the first three lines to get the image urls

<3 commented out the first three lines,run the last two lines to download the images,resuming from break point supported
'''

from common import getHtml,getHtmlwithBaiduCookie,r1,md5
from urllib import quote,unquote
import re
import os
import json
from multiprocessing import Pool,Lock

img_url_file=r'img_url.log'
download_log=r'download.log'

fileLock=Lock()

def extract_imageurl(url):    
    url_list=[]    
    content=getHtmlwithBaiduCookie(url)
    if not content:
        print 'getHtml is none'
        return url_list 
    try:
        info=json.loads(content,encoding='utf-8')
        if info.has_key('data'):
            data=info['data']
            for img in data:
                if img.has_key('hoverURL'):
                    url_list.append(img['hoverURL'])
    except:
        print 'parse error:%s'%url        
#         print content
    return url_list

def crawl_img_urls(page=25,keyword=''):
    # return 60 image urls every page
    #http://image.baidu.com/i?tn=resultjson_com&ps=1&ct=201326592&lm=-1&cl=2&nc=1&word=%C7%B9&ie=gbk&ipn=rj&oe=utf-8&rn=60&pn=180&700181138096.0983&635849489996.466
    quoteStr=quote(keyword.decode('utf-8').encode('gbk')).decode('utf-8')
    extra_url_prefix=r'http://image.baidu.com/i?tn=resultjson_com&ie=gbk&word='+quoteStr+r'&oe=utf-8&rn=60&pn='
    search_urls=[extra_url_prefix+str(i*60) for i in range(page)]
    pool=Pool() # default core number
    results=pool.map(extract_imageurl, search_urls)
#     url_list1=extract_imageurl2(extra_url_prefix+str(0))
#     url_list2=extract_imageurl2(extra_url_prefix+str(1))
    pool.close()
    pool.join()
    url_list=[]
    for result in results:
        url_list+=result
    url_set=set(url_list)
    savetoImgUrls(url_set)
    printFile(img_url_file)
    
def printFile(filename):   
    urls=readFromFile(filename)
    if urls==None:
        print 'urls is none'
        return
    if len(urls)<1:
        print 'urls is empty'
    count=0
    for url in urls:
        count+=1
        print count,url   
          
def dumpToFile(filename,infoList,mode='a'):
    filePath=r'./'+filename
    strInfo=''
    count=0
    for item in infoList:
        count+=1
        strInfo+=item+'\n'     
        print count,item      
    with open(filePath,mode) as fout:
        fout.write(strInfo) 
        
def readFromFile(filename,mode='r'):   
    filePath=r'./'+filename
    if not os.path.exists(filePath):
        print filePath,'does not exist'
        return
    with open(filePath,mode) as fin:
        temp= list(fin)  
        return [l.strip('\r\n') for l in temp]
    
def getDownloaded(): 
    downloads=readFromFile(download_log) 
    if not downloads:
        return []
    return [l.split(r' --> ')[0] for l in downloads]  

def savetoDownloaded(img_url,img_name): 
    msg=img_url+r' --> '+img_name
    dumpToFile(download_log,[msg,],'a')

def getImgUrls():  
    imgUrls= readFromFile(img_url_file)
    if not imgUrls:
        return []
    return imgUrls

def savetoImgUrls(imgUrls): 
    dumpToFile(img_url_file,imgUrls,'w')
    
def saveasImage(imgname,content):
    if not os.path.exists(r'./imgs'):
        os.mkdir(r'./imgs')
    filePath=os.path.join(r'./imgs',imgname)
    if os.path.exists(filePath):
        print filePath,'already exists'
        return
    with open(filePath,'wb') as fout:
        fout.write(content)
def getImage(imgurl,lock=fileLock):  
    content=getHtmlwithBaiduCookie(imgurl)   
    if not content:
        print 'getImage failure'
        return    
    imgname=md5(imgurl)+r'.jpg'
    saveasImage(imgname,content) 
    lock.acquire()
    savetoDownloaded(imgurl,imgname)
    lock.release()
      
def download_images():
    downloaded=getDownloaded()
    downloaded_set=set(downloaded)
    imgUrls=getImgUrls()
    imgUrls_set=set(imgUrls)
    undownloaded=imgUrls_set-downloaded_set
    print 'undownloaded:',len(undownloaded)
    pool=Pool()
    pool.map(getImage, undownloaded)
    pool.close()
    pool.join()
            
if __name__=='__main__':  
    keyword='明星证件照'
    crawl_img_urls(20,keyword)
    printFile(img_url_file)
 
#     download_images()
#     printFile(download_log)
