#!/usr/bin/python
#coding=utf-8

import re
import zlib
import requests
from lxml import html

'''
import sys
DEFAULT_BODY_ENCODING = sys.getdefaultencoding()

大陆地区扫描 在没有取得编码的情况下默认使用gb2312

尝试解压页面内容
尝试从HTTP头,HTTP页面中获取,页面内容编码(失败情况下默认编码为gb2312)
统一转换为unicode进行处理

使用lxml前注意事项：先确保html经过了utf-8解码，即code = html.decode('utf-8', 'ignore')，否则会出现解析出错情况。
因为中文被编码成utf-8之后变成 '/u2541'　之类的形式，lxml一遇到　“/”就会认为其标签结束。
将页面解码为unicode，再传递给lxml.html.fromstring使用


requests 中已包含完整的压缩,解码处理
HTTPBody部分代码暂时保留备用
'''

class HTTPBody:
    def __init__(self):
        self.content_type = ''
        self.exception = None

    '''
        RFC 1950 (zlib compressed format)
        RFC 1951 (deflate compressed format)
        RFC 1952 (gzip compressed format)
    '''
    def decompressBody(self, header, body):

        if header != None:
            compress_type = header.get('content-encoding')

            if compress_type == 'zlib':
                body = zlib.decompress(body, zlib.MAX_WBITS)
            elif compress_type == 'gzip':
                body = zlib.decompress(body, zlib.MAX_WBITS|16)
            elif compress_type == 'deflate':
                body = zlib.decompress(body, -zlib.MAX_WBITS)
            else:
                #print "unknown content-encoding: %s" % (compress_type)
                pass

        return body

    def searchPattern(self, pattern, text):
        search_text = None
        match_text = pattern.search(text)
        if match_text is not None:
            search_text = match_text.group(1)
        return search_text

    '''
    优先获取页面中的编码类型
    '''
    def getContentType(self,header, body):
        #<meta http-equiv="Content-Type" content="text/html; charset=big5">
        content_type = self.searchPattern(re.compile('<meta.+?charset=([-\w\d]+)',re.I), body)
        if content_type == None or len(content_type) == 0:
            if header != None and header.get('content-type') != None:
                #Content-Type	text/html; charset=utf-8
                content_type = self.searchPattern(re.compile('charset=([-\w\d]+)',re.I), header.get('content-type'))

        if content_type == '' or content_type == None:
            content_type = 'utf-8'

        return content_type

    '''
        加ignore解码页面内容，如果返回'gb2312' codec can't decode bytes in position 135-136: illegal multibyte sequence
        错误，可能导致解析页面内容的时候出现乱码

        解压页面内容后，尝试decode为Unicode
        如果解析失败，则返回解压后的原始页面
        这种策略下返回的页面，在lxml.html.fromstring加载过程中一样可能导致失败。
    '''
    def decodeBody(self, header, body):
        try:
            decompressed_body = self.decompressBody(header, body)
            content_type = self.getContentType(header, decompressed_body)

            default_content_type=['utf-8','shift_jis','gb2312','gbk','big5']
            #default_content_type=[]
            default_content_type.insert(0, content_type)
            for content_type in default_content_type:
                try:
                    body = decompressed_body.decode(content_type)
                    self.content_type = content_type
                    break
                except UnicodeDecodeError as e:
                    continue
                except LookupError as e:
                    continue

        except Exception as e:
            print 'error decode body %s' % (e.message)
            raise e

        return body


class HTTPBodyRequest(HTTPBody):
    def __init__(self):
        HTTPBody.__init__(self)



#http://liguangming.com/python-requests-ge-encoding-from-headers
def get_requests_response_encoding(response):
    encoding = ''
    encodings = requests.utils.get_encodings_from_content(response.content)
    if encodings:
        encoding = encodings[0]
    else:
        encoding = response.apparent_encoding
    return encoding

class HTTPBodyResponse(HTTPBody):
    def __init__(self):
        pass


#媒体类型数据处理
class HTTPBodyResponseMedia(HTTPBodyResponse):
    def __init__(self):
        pass

#文本类型数据处理
class HTTPBodyResponseText(HTTPBodyResponse):
    def __init__(self, body, encoding):
        self.body = body
        self.encoding = encoding

#XML类型数据处理
class HTTPBodyResponseXML(HTTPBodyResponseText):
    def __init__(self, body, encoding):
        HTTPBodyResponseText.__init__(self, body, encoding)

#HTML页面类型数据处理
class HTTPBodyResponseHTML(HTTPBodyResponseText):
    def __init__(self, body, encoding):
        HTTPBodyResponseText.__init__(self, body, encoding)
        self.dom_body = None
        self._parse()

    def _parse(self):
        if self.dom_body != None:
            return
        try:
            self.dom_body = html.fromstring(self.body.decode(self.encoding))
        except Exception as e:
            self.exception = e

    @property
    def title(self):

        title = ''
        try:
            if self.dom_body != None:
                title_tags = ['title','h1','h2']
                for tag in title_tags:
                    node_title = self.dom_body.xpath('//'+tag)
                    if len(node_title) > 0:
                        text_title = node_title[0].text
                        if text_title != None:
                            title = text_title.encode('utf-8')
                            title = title.strip()

                    if len(title) != 0:break

        except Exception as e:
            self.exception = e

        return title

    #页面解析
    def extractResults(self):
        pass

import json
class HTTPBodyJsonResponse(HTTPBody):
    def __init__(self, body, encoding):
        HTTPBody.__init__(self)
        self.body = body
        self.encoding = encoding
        self.json_body = None
        self._parse()

    def _parse(self):
        if self.json_body != None:
            return
        try:
            self.dom_body = json.loads(self.body)
        except Exception as e:
            self.exception = e

    @property
    def title(self):
        return ''

    #页面解析
    def extractResults(self):
        pass



