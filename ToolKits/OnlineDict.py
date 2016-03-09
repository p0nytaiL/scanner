#!/usr/bin/python
#coding=utf-8

import sys
import os
from lxml import html
from urllib import urlencode,quote
import platform

from PackageHTTP.MethodEx import MethodGET

class OnlineDict:
    def __init__(self):
        self.m = MethodGET()
        self.onlinedict_url = None

    def getOnlineDictUrl(self, word):
        pass

    def printPronunciation(self, html_content):
        pass

    def printExplain(self,html_content):
        pass

    def searchWord(self, word):
        try:
            self.m.setHostInfo(url = self.getOnlineDictUrl(word))
            resp, error = self.m.getResponse()
            html_content = resp
            html_content = html_content.decode('utf-8')
            html_content = html.fromstring(html_content)
            self.printPronunciation(html_content)
            self.printExplain(html_content)
        except Exception as e:
            print 'error %s' % (e)


class OnlineDictBing(OnlineDict):

    def getOnlineDictUrl(self, word):
        print '\r\n--- from bing ---'
        #FORM=BDVSP6&mkt=zh-cn
        query_string = {
            'q':word,
            'FORM':'BDVSP6',
            'mkt':'zh-cn'
        }
        return "http://www.bing.com/dict/?"+urlencode(query_string)

    def printPronunciation(self, html_content):
        pr_US = html_content.xpath("//div[@class='qdef']/div[@class='hd_area']/div[@class='hd_tf_lh']/div[@class='hd_p1_1']/div[@class='hd_prUS']")
        pr_UK = html_content.xpath("//div[@class='qdef']/div[@class='hd_area']/div[@class='hd_tf_lh']/div[@class='hd_p1_1']/div[@class='hd_pr']")
        if len(pr_US) > 0:
            print pr_US[0].text,
        if len(pr_UK) > 0:
            print pr_UK[0].text,

        print ''

    '''
    word_type = html_content.xpath("//div[@class='qdef']/ul/li/span[@class='pos']")
    word_def = html_content.xpath("//div[@class='qdef']/ul/li/span[@class='def']/span")
    web_word_type = html_content.xpath("//div[@class='qdef']/ul/li/span[@class='pos_web']")
    web_word_def = html_content.xpath("//div[@class='qdef']/ul/li/span[@class='def']/span")
    '''
    def printExplain(self,html_content):
        nodes_word_def = html_content.xpath("//div[@class='qdef']/ul/li")
        for node_word_def in nodes_word_def:
            for node in node_word_def.getchildren():
                if node.attrib['class'].startswith('pos'):
                    print '%s ' %(node.text),
                if node.attrib['class'] == 'def':
                    nodes_def =  node.getchildren();
                    for node_def in nodes_def:
                        print node_def.text,
                    print ''



class OnlineDictICIBA(OnlineDict):

     def getOnlineDictUrl(self, word):
        print '\r\n--- from iciba ---'
        return "http://www.iciba.com/"+quote(word)


     def printPronunciation(self, html_content):
        prs = html_content.xpath("//div[@class='result-info']/div[@class='info-article info-base']/div[@class='base-speak']/span")
        for pr in prs:
            print pr.text,
        print ''

     def printExplain(self,html_content):
         nodes_word_def = html_content.xpath("//div[@class='result-info']/div[@class='info-article info-base']/ul[@class='base-list switch_part']/li")
         for node_word_def in nodes_word_def:
             if len(node_word_def.attrib) == 0:
                 for item in node_word_def:
                     explain =  item.text
                     explain =  item.text.replace('  ','').replace('\r','').replace('\n','')
                     print explain


             elif node_word_def.attrib['class'] == 'change':
                 for item in node_word_def:
                     if 'span' == item.tag:
                         print item.text + ":"
                     elif 'p' == item.tag:
                         for change in item:
                             if 'span' == change.tag:
                                print '\t' + change.text,
                             elif 'a' == change.tag:
                                 print change.text
             print ''




