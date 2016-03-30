#coding=utf-8

__author__ = 'copy'
import urllib
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
'''
class PageParse():
    def __init__(self):
        pass

    def ExtractResult(self,dom_page, page):
        return [page.encode('utf-8')]


class SearchEngine(object):
    def __init__(self):
        self.keyword = None
        self.pageParse = PageParse()

    def CreateFirstSearchPageUrl(self):
        pass

    def GoNextPage(self, next_page_url):
        pass

    def HasResult(self,dom_page):
        pass

    def Search(self,keyword):
        print 'Start Searching...'
        dom_pages=[]
        pages=[]
        self.keyword = keyword#urllib.quote(keyword)
        next_page_url = self.CreateFirstSearchPageUrl()
        if next_page_url == '':
            return None

        cnt_page=0
        while True:
            print next_page_url
            dom_page, page, next_page_url = self.GoNextPage(next_page_url)
            if dom_page != None:
                dom_pages.append(dom_page)
                pages.append(page)

            if next_page_url == None or next_page_url == '':
                break

        print '\r\nFinish (%d Pages)!\r\n' % (cnt_page)
        return dom_pages, pages

    def AnalyzeResult(self, keyword):
        result = []
        dom_pages, pages = self.Search(keyword)

        if self.pageParse != None:
            for i in xrange(0,len(pages)):
                tmp = self.pageParse.ExtractResult(dom_pages[i], pages[i])
                result.extend(tmp)

        #结果去重
        result_set = set()
        for r in result:
            result_set.add(r)

        print '%d result parsed' % (len(result_set))
        return result_set