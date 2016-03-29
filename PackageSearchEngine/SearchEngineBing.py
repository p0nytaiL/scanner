import urllib,urlparse
from lxml import html
from PackageSearchEngine.SearchEngine import SearchEngine,PageParse
from PackageHTTP.UserAgents import getRandomAgent
import requests

class SearchEngineBing(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)

    def CreateByPassCookie(self):
        # ------------- cookie ------------
        cookie_k1 = 'SRCHHPGUSR'
        cookie_v1 = urllib.urlencode({'NTAB': '0',
                               'NEWWND': '0',
                               'SRCHLANG': '',
                               'AS': '1'})

        cookie_k2 = '_FS'
        cookie_v2 = urllib.urlencode({'mkt': 'en-us',
                               'ui': '#en-us'})

        cookie_k3 = '&NRSLT'
        cookie_v3 = 50

        cookie = "%s=%s;%s=%s;%s=%s" % (cookie_k1, cookie_v1,
                                        cookie_k2, cookie_v2,
                                        cookie_k3, cookie_v3)
        return cookie

    def CreateFirstSearchPageUrl(self):
        '''
               query_string['qs']='n'
        query_string['go']='submit'
        query_string['form']='QBLH'
        query_string['sc']='0-7'
        query_string['sp']='-1'
        query_string['sk']=''
        :return:
        '''
        query_string={
            'q' : self.keyword,
            'count' : '50'
        }
        #url = urlparse.ParseResult('http','link.aizhan.com','/','',urllib.urlencode(query_string),'')
        url = urlparse.ParseResult('http','cn.bing.com','/search','',urllib.urlencode(query_string),'')
        return url.geturl()

    def GoNextPage(self, next_page_url):
        print next_page_url
        headers ={
            'Cookie':'SRCHD=D=4157510&AF=NOFORM; SRCHUSR=AUTOREDIR=0&GEOVAR=&DOB=20151127; _EDGE_V=1; MUID=2F2195A82AB36CD323ED9DC42B126D4B\
; SRCHHPGUSR=CW=1280&CH=243&DPR=2; SRCHUID=V=2&GUID=A3398A472384489FB0BCECAA822C8EDE; MUIDB=2F2195A82AB36CD323ED9DC42B126D4B\
; HPSHRLAN=CLOSE=1; _SS=SID=0B472366C4E76A200A642BCAC5466BAB&HV=1454139963; _EDGE_S=mkt=zh-cn&SID=0B472366C4E76A200A642BCAC5466BAB\
; WLS=C=&N=; SNRHOP=TS=635897356787832176&I=1; SCRHDN=ASD=0&DURL=#',
            'User-Agent':getRandomAgent()
        }
        response = requests.get(url=next_page_url, headers = headers)
        '''
        m = HTTPMethodGET()
        m.setHostInfo(url = next_page_url)
        m.setCookie('SRCHD=D=4157510&AF=NOFORM; SRCHUSR=AUTOREDIR=0&GEOVAR=&DOB=20151127; _EDGE_V=1; MUID=2F2195A82AB36CD323ED9DC42B126D4B\
; SRCHHPGUSR=CW=1280&CH=243&DPR=2; SRCHUID=V=2&GUID=A3398A472384489FB0BCECAA822C8EDE; MUIDB=2F2195A82AB36CD323ED9DC42B126D4B\
; HPSHRLAN=CLOSE=1; _SS=SID=0B472366C4E76A200A642BCAC5466BAB&HV=1454139963; _EDGE_S=mkt=zh-cn&SID=0B472366C4E76A200A642BCAC5466BAB\
; WLS=C=&N=; SNRHOP=TS=635897356787832176&I=1; SCRHDN=ASD=0&DURL=#')
        #m.setCookie(self.CreateByPassCookie())
        response, error = m.getResponse()

        body = HTTPBodyResponse()
        body = body.decodeBody(response['headers'], response['body'])
        #print body.encode('utf-8')
        '''
        body = response.content
        dom_body = html.fromstring(body.decode(response.encoding))

        next_page_url=''
        hrefs = dom_body.xpath("//a[@class='sb_pagN']")
        if len(hrefs) == 0:
            return dom_body, body, None

        for next_page_link in hrefs:
            next_page_url = next_page_link.attrib['href']
            next_page_url = ('http://cn.bing.com' + next_page_url)
            return dom_body, body, next_page_url

'''
Bing Result Parses
'''

class PageParseLinks(PageParse):
    def __init__(self):
        pass

    def ExtractResult(self,dom_page, page):
        results = []
        hrefs = dom_page.xpath('//h2/a[@href]')
        for link in hrefs:
            parse_result = urlparse.urlparse(link.attrib['href'])
            results.append(parse_result[1])

        return results

if __name__ == '__main__':
    s = SearchEngineBing()
    s.pageParse = PageParseLinks()
    s = s.AnalyzeResult("domain:github.com")
    print s
