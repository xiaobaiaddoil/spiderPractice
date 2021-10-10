import requests
import uuid
import hashlib
import Myheaders
from lxml import etree


class getAuthorBooks():
    '''
    获取一个作者全部作品的url类

    '''
    urlOrgin = 'https://m.xyyuedu.com'

    def __init__(self, Author):
        '''
        初始化这个作者的相关信息
        '''
        self.dic = {}
        self.dic["Aid"] = uuid.uuid4()
        self.dic["Aname"] = Author.name
        self.dic["Aurl"] = Author.url
        self.dic["books"] = []
        self.dic["Astatus"] = 0
        leng = str(len(self.dic['books']))
        self.dic["Akey"] = hashlib.md5(leng.encode(encoding='utf-8')).hexdigest()

    def setBooksUrl(self):
        self.dic['Astatus'] = 1
        try:
            r = requests.get(self.dic['Aurl'])
        except Exception:
            print('error')
        else:
            if r.status_code == 200:
                html = etree.HTML(r.content)
                listBook = html.xpath('.//div[@class="q_top c_big"]')[0]
                listBook = listBook.xpath('./following-sibling::div[2]/div')
                for i in listBook:
                    Burl = self.urlOrgin+''.join(i.xpath('./a/@href'))
                    bookname = ''.join(i.xpath('./a/i/following-sibling::text()'))
                    dicBook = {}
                    dicBook['Bid'] = uuid.uuid4()
                    dicBook['Bname'] = bookname
                    dicBook['Burl'] = Burl
                    dicBook['childUrls'] = []
                    dicBook['Bstatus'] = 0
                    leng = str(len(dicBook['childUrls']))
                    dicBook['Bkey'] = hashlib.md5(leng.encode(encoding='utf-8')).hexdigest()
                    self.dic['books'].append(dicBook)
                self.dic['Astatus'] = 2
                leng = str(len(self.dic['books']))
                self.dic["Akey"] = hashlib.md5(leng.encode(encoding='utf-8')).hexdigest()
    
    def getBooksUrl(self):
        self.setBooksUrl()
        return self.dic
