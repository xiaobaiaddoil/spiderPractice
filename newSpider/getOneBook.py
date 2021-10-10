
import requests
import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import threading
from Myheaders import headers
from config import urlOrgin
import gevent


class getBook():
    def __init__(self, dic):
        self.dic = dic
        
    def isRecive(self, r):
        if r.status_code == 200:
            return True
        else:
            return False

    def isFolderExist(self, Mypath):
        self.Folderpath = Mypath
        if not os.path.exists(Mypath):
            os.mkdir(Mypath)
            
    def getOneBookCharpter(self, book):
        print('子线程{}开始获取{}的内容'.format(threading.current_thread().name, book['Bname']))
        text = requests.get(book['Burl'], headers)
        if self.isRecive(text):
            html = etree.HTML(text.content)
            # 判断是否存在该文件夹
            self.isFolderExist('./爬取内容存储/'+self.dic['Aname'])
            charpters = html.xpath('//div[@id="box2"]/ul/li')
            # 创建协程的任务列表
            gaventList = []
            f = open(self.Folderpath+'/'+book['Bname']+'.txt', 'a', encoding='utf-8')
            for charpter in charpters:
                i = urlOrgin+''.join(charpter.xpath('./a/@href'))
                gaventList.append(gevent.spawn(self.getContent, i))
            gevent.joinall(gaventList)
            for g in gaventList:
                gvalue = g.value
                # 写入文章章节的标题
                f.write(gvalue[0])
                # 写入章节的内容
                f.writelines(gvalue[1])
            f.close()
        else:
            print('请求失败')
            
    def getContent(self, url):
        try:
            text = requests.get(url, headers)
        except Exception:
            print('error'+url)
        else:
            if self.isRecive(text):
                html = etree.HTML(text.content)
                title = ''.join(html.xpath('//div[@id="nr_title"]//text()'))
                txt = ''.join(html.xpath('//div[@id="nr1"]//text()'))
                print('协程正在读取'+url+'内容')
                return [title, txt]

    def getBooks(self):
        print('多线程开始获取{}的所有作品'.format(self.dic['Aname']))
        with ThreadPoolExecutor(max_workers=20) as pool:
            for book in self.dic['books']:
                pool.submit(self.getOneBookCharpter, book)
        print('————————获取完成————————')
        self.deleteEmptyTxt()
    
    def deleteEmptyTxt(self):
        delPath = os.path.join(self.Folderpath, ".txt")
        os.remove(delPath)

    