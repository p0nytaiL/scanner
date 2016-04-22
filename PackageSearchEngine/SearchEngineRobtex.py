import requests
import urllib,urlparse
from lxml import html
from PackageSearchEngine.SearchEngine import SearchEngine
from PackageHTTP.UserAgents import getRandomAgent
from PackageHTTP.Body import HTTPBodyResponse

class RobtexResponse(HTTPBodyResponse):
    def __init__(self, body, encoding):
        HTTPBodyResponse.__init__(self, body, encoding)
        self.filter = ''

    def extractResults(self):
        links = self.dom_body.xpath('//table[@class="sortable noinit scrollable noanchor"]')
        links = links[0].xpath('.//tr/td/i')

        records = []
        others = []
        for index, link in enumerate(links):
            if index % 2 == 0:
                ip = links[index].text
                hostname = links[index+1].text
                if len(self.filter) and hostname.find(self.filter) >=0:
                    records.append([ip, hostname])
                else:
                    others.append([ip, hostname])

        records.extend(others)
        return records

class SearchEngineRobtex(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.hostname = 'www.robtex.com'
        self.filter = ''
        self.url = ''

    def CreateFirstSearchPageUrl(self):
        return self.url

    def GoNextPage(self, next_page_url):
        headers ={
            'User-Agent':getRandomAgent()
        }
        response = requests.get(url=next_page_url, headers = headers)
        body = RobtexResponse(response.content, response.apparent_encoding)

        return body, None

    def AnalyzeResult(self, keyword):
        result = []
        pages = self.Search(keyword)

        for page in pages:
            page.filter = self.filter
            records = page.extractResults()
            for record in records:
                print record[0], record[1]
                result.append(record[1])

        return result

if __name__ == '__main__':
    s = SearchEngineRobtex()
    results = s.AnalyzeResult('')

