#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-10-25

@author: JohnDannl

usage:
<1 replace the keywords in __main__

<2 commented out the last two lines,run the first three lines to get the image urls

<3 commented out the first three lines,run the last two lines to download the images,resuming from break point supported
'''
from common import getHtml,getHtmlwithGoogleCookie,getTextwithGoogleCookie,r1,md5
from urllib import quote
import re
import os
from multiprocessing import Pool,Lock

img_url_file=r'img_url.log'
download_log=r'download.log'

fileLock=Lock()

def extract_imageurl(url):
    content=getHtmlwithGoogleCookie(url)
    if not content:
        print 'getHtml is none'
        return []
    url_list=re.findall(r'http://www.google.com.hk/imgres\?imgurl=(.*?)&amp', content)
    return url_list if url_list!=None else []
def extract_imageurl2(url):
    content=getTextwithGoogleCookie(url)
    if not content:
        print 'getHtml is none'
        return []
    url_list=re.findall(r'/imgres\?imgurl=(.*?)&amp', content)
    return url_list if url_list!=None else []
def crawl_img_urls(page=10,keyword=''):
    # return 100 image urls every page
# https://www.google.com.hk/search?q=%E6%9E%AA&newwindow=1&safe=strict&client=firefox-a&hs=EMi&sa=X&rls=org.mozilla:zh-CN:official&channel=fflb&biw=1440&bih=763&tbm=isch&ijn=2&ei=QqJLVLKrBsqkygP6_YHwDg&start=200
# https://www.google.com.hk/search?q=%E8%AF%81%E4%BB%B6%E7%85%A7&newwindow=1&safe=strict&biw=1440&bih=761&tbm=isch&ijn=1&ei=6gH9VNmoA4TAmAWkooGgAg&start=100
#     extra_url_mid='&ei=QqJLVLKrBsqkygP6_YHwDg&start=0' # is no needed
#     url_list1=extract_imageurl(the_first_load_url) #just equls 'ijn=0'
    quoteStr=quote(keyword).decode('utf-8')    
    extra_url_prefix=r'https://www.google.com.hk/search?q='+quoteStr+'&newwindow=1&safe=strict&sa=X&biw=1440&bih=761&tbm=isch&ijn='
    search_urls=[extra_url_prefix+str(i) for i in range(page)]
    pool=Pool() # default core number
    results=pool.map(extract_imageurl2, search_urls)
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
    content=getHtml(imgurl)   
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

#     url=r'https://www.google.com.hk/search?q=%E8%AF%81%E4%BB%B6%E7%85%A7&newwindow=1&safe=strict&sa=X&biw=1440&bih=761&tbm=isch&ijn=0'
#     extract_imageurl2(url)
if __name__=='__main__':
    keyword='证件照'
    crawl_img_urls(5,keyword)
    printFile(img_url_file)
    
#     download_images()
#     printFile(download_log)
