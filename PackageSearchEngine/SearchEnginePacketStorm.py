import requests
import urllib,urlparse
from PackageSearchEngine.SearchEngine import SearchEngine
from PackageHTTP.UserAgents import getRandomAgent
from PackageHTTP.Body import HTTPBodyResponse

class PacketStromResponse(HTTPBodyResponse):
    def __init__(self, body, encoding):
        HTTPBodyResponse.__init__(self, body, encoding)

    #<a href="/files/page2/" accesskey="]">Next</a>
    @property
    def next_page_url(self):
        hrefs = self.dom_body.xpath('//a[@accesskey="]"]')

        if len(hrefs) == 0 or hrefs[0].attrib.get('href') == None:
            return None

        else:
            return ('https://packetstormsecurity.com' + (hrefs[0].attrib['href']))

    def extractResults(self):
        records = self.dom_body.xpath('//div[@id="c"]/div[@id="cc"]/div[@id="m"]/dl')
        results = []
        for index, record in enumerate(records):
            result = {
                'title': '',
                'tags': []
            }
            #title
            dom_title = record.xpath('./dt/a')
            result['title'] = dom_title[0].text
            #tags
            dom_tages = record.xpath('./dd[@class="tags"]')
            if len(dom_tages):
                dom_tages = dom_tages[0].xpath('./a')
                for tags in dom_tages:
                    result['tags'].append(tags.text)

            results.append(result)

        return results


class SearchEnginePacketStrom(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.hostname = 'packetstormsecurity.com'

    def GoNextPage(self, next_page_url):
        headers ={
            'User-Agent':getRandomAgent()
        }
        response = requests.get(url=next_page_url, headers = headers)
        body = PacketStromResponse(response.content, response.apparent_encoding)

        return body, body.next_page_url

    def AnalyzeResult(self, keyword):
        results = []
        pages = self.Search(keyword)

        for page in pages:
            results.extend(page.extractResults())

        return results


class SearchEnginePacketStromToday(SearchEnginePacketStrom):
    def __init__(self):
        SearchEnginePacketStrom.__init__(self)

    def CreateFirstSearchPageUrl(self):
        import time
        current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        return 'https://packetstormsecurity.com/files/date/' + current_time + '/'

class SearchEnginePacketStromSearch(SearchEnginePacketStrom):
    def __init__(self):
        SearchEnginePacketStrom.__init__(self)

    def CreateFirstSearchPageUrl(self):
        query_string={
            'q' : self.keyword,
        }
        return 'https://packetstormsecurity.com/search/?'+urllib.urlencode(query_string)


def echoResults(records):

    advisories = []
    tools = []
    others = []

    for i in records:
        if 'tool' in i['tags']:
            tools.append(i)
        elif 'advisory' in i['tags']:
            advisories.append(i)
        else:
            others.append(i)

    advisories.sort()
    tools.sort()
    others.sort()

    print 'TOOLS[%d]:'%(len(tools))
    for tool in tools:
        print '\t', tool['title']

    print '\r\n'

    print 'ADVISORIES[%d]:'%(len(advisories))
    for advisory in advisories:
        print '\t', advisory['title']

    print '\r\n'

    print 'OTHERS[%d]:'%(len(others))
    for other in others:
        print '\t', other['title']
        print '\t\t', other['tags']


if __name__ == '__main__':
    s = SearchEnginePacketStromSearch()
    records = s.AnalyzeResult('ssh')
    echoResults(records)