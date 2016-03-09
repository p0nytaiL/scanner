#!/usr/bin/python
#coding=utf-8

from PackageHTTPBase.Body import HTTPBodyResponse
from lxml import html

'''
Form, input, select, and textarea elements each have special methods.
'''
class FormDetector(HTTPBodyResponse):
    def __init__(self):
        HTTPBodyResponse.__init__(self)

    def detectForm(self, headers, body):
        readable_body = self.decodeBody(headers, body)
        dom_body = html.fromstring(readable_body)
        form = dom_body.forms[0]
        self.printFormDetail(form)


    '''
    action
    inputs
    fields 简化版的input

    method
    '''
    def printFormDetail(self, form):
        if None != form:
            print form.action
            print form.method
            for input in form.inputs:
                print input.type, input.name

            for field in form.fields:
                print field
