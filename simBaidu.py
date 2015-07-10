#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-11

@author: JohnDannl

usage:

<1 replace the url (the visiting page) in __main__, 

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


pattern=re.compile('queryImageUrl=(.*?)&')
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
                if img.has_key('objURL'):
                    url_list.append(img['objURL'])
    except:
        print 'parse error:%s'%url        
#         print content
    return url_list

def extract_imageurl_face(url):    
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
                if img.has_key('flowURL'):
                    url_list.append(img['flowURL'])
    except:
        print 'parse error:%s'%url        
#         print content
    return url_list

def crawl_img_urls(url,page=25,face=None):
    # return 60 image urls every page
    # url is like 'http://image.baidu.com/n/pc_search?queryImageUrl=http%3A%2F%2Fb.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2F0eb30f2442a7d9334945b2c7a84bd11372f00190.jpg&querySign=408832356%2C3878106824&fm=result&pos=upload'
    query_url=r1(pattern,url)
    if face:
        search_url='http://image.baidu.com/n/face?queryImageUrl=%s&rn=60&pn='%query_url
    else:
        search_url='http://image.baidu.com/n/similar?queryImageUrl=%s&rn=60&pn='%query_url 
    search_urls=[search_url+str(i*60) for i in range(page)]
    pool=Pool() # default core number
    if face:
        results=pool.map(extract_imageurl_face, search_urls)
    else:
        results=pool.map(extract_imageurl, search_urls)
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
    url='http://image.baidu.com/n/pc_search?queryImageUrl=http%3A%2F%2Fb.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2F0eb30f2442a7d9334945b2c7a84bd11372f00190.jpg&querySign=408832356%2C3878106824&fm=result&pos=upload'
    crawl_img_urls(url,1,face=True)
    printFile(img_url_file)
    
#     download_images()
#     printFile(download_log)
