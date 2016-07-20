#!/usr/bin/python
#coding=utf-8

'''
Internet Data Handling
    https://docs.python.org/2/library/netdata.html

email message (MIME, RFC 2822-based message documents)
不支持发信(SMTP,NNTP),要发信找smtplib,nntplib支持
其实现尽可能遵守RFC 2821规范, 部分RFC 2822规范
MIME相关的RFC规范 2045,2046,2047,2231

主要负责构造,解析邮件对象

email.message 邮件对象
email.parser   解析器
email.generator MIME文档生成器
email.mime  创建email与MIME对象
email.header    邮件头
email.charset   字符集
email.encoders  编码器
email.errors    标准错误
email.utils 辅助工具
email.iterators 迭代器

功能类似的还有mimelib
'''

'''
example of email.message
'''

'''
example of email.header

    RFC 2822用7位的ASCII描述email消息的格式(继承自RFC 822,用8位的ASCII来描述消息)
    大量RFC描述了如何将邮件内容编码为符合RFC 2822规范的7位的ASCII.
    RFC 2045,2046,2047,2231等

    email对这部分的支持实现在email.header与email.charset中

    https://docs.python.org/2/library/email.header.html
'''
'''
example of email.parser

    non-MIME message
    MIME message

    incremental FeedParser API:
        流式解析器

    classic Parser API:
        完整消息解析器

        从string或者file中读入mail内容
        如果仅对Header内容感兴趣,可使用HeaderParser


'''
class EMLLoader:
    def __init__(self):
        pass

    def load(self, file):
        #fp = open('/Users/ponytail/Desktop/Private/网上购票系统-用户支付通知','r')
        fp = open(file, 'r')
        from email import parser,message,header,utils
        eml_parser = parser.HeaderParser()
        eml_msg =  eml_parser.parse(fp)
        result = {
            'subject':'',
            'from':''
        }
        for k,v in eml_msg.items():

            if k.lower() in ['subject']:
            #if 1 == 1:
                value, charset = header.decode_header(v)[0]
                if charset != None:
                    value = value.decode(charset)
                #print '%s : %s (%s)' % (k, value, v)
                result['subject'] = value

            if k.lower() in ['from']:
                v = utils.parseaddr(v)
                result['from'] = v[1]

        return result

if __name__ == '__main__':
    import os
    path = '/Users/ponytail/Desktop/Private/mail/hotmail/'
    dict_summary = {}
    for parent,dirnames,filenames in os.walk(path):
        for filename in filenames:
            loader = EMLLoader()
            result = loader.load(path + filename)
            result = result['from'].split('@')
            name = result[0]
            corp = result[1]
            if dict_summary.get(corp) == None:
                dict_summary[corp] = set()
            dict_summary[corp].add(name)

    for k, v in dict_summary.items():
        print 'corp: ', k

        for i in v:
            print '\t', i,'('+i+'@'+k+')'



