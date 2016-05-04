import requests
import urllib,urlparse
from PackageSearchEngine.SearchEngine import SearchEngine
from PackageHTTP.UserAgents import getRandomAgent
from PackageHTTP.Body import HTTPBodyResponse
'''
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
'''


class BingResponse(HTTPBodyResponse):
    def __init__(self, body, encoding):
        HTTPBodyResponse.__init__(self, body, encoding)


    @property
    def next_page_url(self):
        hrefs = self.dom_body.xpath("//a[@class='sb_pagN']")
        if len(hrefs) == 0:
            return None

        else:
            return ('https://www.bing.com' + (hrefs[0].attrib['href']))

    def extractResults(self):
        pass

class BingResponseLinks(BingResponse):
    def __init__(self, body, encoding):
        HTTPBodyResponse.__init__(self, body, encoding)
        self.bool_raw = False

    def extractResults(self):
        results = []
        hrefs = self.dom_body.xpath('//h2/a[@href]')
        for link in hrefs:
            if self.bool_raw:
                parse_result = urlparse.urlparse(link.attrib['href'])
                results.append(parse_result[1])
            else:
                results.append(link.attrib['href'])

        return results

class SearchEngineBing(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.hostname = 'www.bing.com'

    def CreateFirstSearchPageUrl(self):
        query_string={
            'q' : self.keyword,
            'count' : '50'
        }
        url = urlparse.ParseResult('https',self.hostname,'/search','',urllib.urlencode(query_string),'')
        return url.geturl()

    def GoNextPage(self, next_page_url):
        headers ={
            'Cookie':'SRCHD=D=4157510&AF=NOFORM; SRCHUSR=AUTOREDIR=0&GEOVAR=&DOB=20151127; _EDGE_V=1; MUID=2F2195A82AB36CD323ED9DC42B126D4B\
; SRCHHPGUSR=CW=1280&CH=243&DPR=2; SRCHUID=V=2&GUID=A3398A472384489FB0BCECAA822C8EDE; MUIDB=2F2195A82AB36CD323ED9DC42B126D4B\
; HPSHRLAN=CLOSE=1; _SS=SID=0B472366C4E76A200A642BCAC5466BAB&HV=1454139963; _EDGE_S=mkt=zh-cn&SID=0B472366C4E76A200A642BCAC5466BAB\
; WLS=C=&N=; SNRHOP=TS=635897356787832176&I=1; SCRHDN=ASD=0&DURL=#',
            'User-Agent':getRandomAgent(),
            'X-Forwarded-For':'203.69.42.169'
        }
        response = requests.get(url=next_page_url, headers = headers)
        body = BingResponseLinks(response.content, response.apparent_encoding)

        return body, body.next_page_url

'''
Bing Result Parses
'''
if __name__ == '__main__':
    s = SearchEngineBing()
    results = s.AnalyzeResult('domain:github.com')
    for domain in results:
        print domain
