#coding=utf-8

__author__ = 'copy'
import requests
from requests.packages.urllib3.exceptions import *
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
'''
ponytail 2015-10-15
    SearchEngine 负责对页面进行遍历
        SearchEngingBing,
        SearchEngineBaidu,
        SearchEngineGoogle,...

    搜索引擎对象功能相对独立，只负责页面的抓取，
    统一抓取完毕之后提交给解析对象进行页面分析
    返回两类页面对象：（页面的规范性问题可能导致解析失败，所以提供原始页面，再lxml解析失败的情况下采用正则匹配）
        字符串形式的HTML页面
        lxml解析过的HTML页面

    调用方式：
        pages,dom_pages = SearchEngine.Search(keyword)


    PageParse   负责对页面内容进行解析
        PageParseGetLinks
        PagePraseGetTitles

    调用方式：
        results ＝ PageParse.ExtractResults(page, dom_pages)


    同时返回page与dom_page的原因在于,在解析next页面的时候,已经将page处理成dom_page了,干脆一起返回

ponytail 2015-10-15
  SearchEngine返回HTTPResponseBody(同时包含html文本,以及html dom对象)
  结果存入数组返回,重写用HTTPResponseBody的extractResults方法
  用xpath提取出感兴趣的内容

'''

class SearchEngine(object):
    def __init__(self):
        self.keyword = None
        self.response_handler = None

    def CreateFirstSearchPageUrl(self):
        pass

    def GoNextPage(self, next_page_url):
        pass

    def HasResult(self,dom_page):
        pass

    def Search(self,keyword):
        print 'Start Searching...'
        pages=[]
        self.keyword = keyword#urllib.quote(keyword)
        next_page_url = self.CreateFirstSearchPageUrl()
        if next_page_url != None and len(next_page_url) == 0 :
            print 'Missing first page url ???'
            return pages

        while True:
            print next_page_url
            page, next_page_url = self.GoNextPage(next_page_url)
            if page != None :
                pages.append(page)

            if next_page_url == None or next_page_url == '':
                break

        print '\r\nFinish (%d Pages)!\r\n' % (len(pages))
        return pages

    #无法统一处理,不同的搜索功能要求返回的结果均不相同
    #默认处理有问题的话可以重写此方法
    def AnalyzeResult(self, keyword):
        result = []
        pages = self.Search(keyword)

        for page in pages:
            tmp = page.extractResults()
            result.extend(tmp)

        #结果去重
        result_set = set()
        for r in result:
            result_set.add(r)

        print '%d result parsed' % (len(result_set))
        return result_set