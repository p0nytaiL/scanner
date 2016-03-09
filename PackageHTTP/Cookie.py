#!/usr/bin/python
#coding=utf-8

import cookielib
class MyCookieJar(cookielib.CookieJar):
    def __init__(self, policy=None):
        cookielib.CookieJar.__init__(self, policy)

    '''
    @property
    def value(self):
        return 'value'
    '''


    '''
        from http response/string
    '''
    def my_make_cookies(self, cookie_string, cookie2_string):
        m = HTTPMethodGET()
        m.setHostInfo('http://10.211.55.11/1.asp')
        response, error = m.getResponse()
        cookie_tuples = self._normalized_cookie_tuples(cookielib.parse_ns_headers(cookie_string))
        print cookie_tuples
        '''
        cookie_count=0
        if None == cookie_string or len(cookie_string) == 0:
            return cookie_count
        """Return sequence of Cookie objects extracted from response object."""
        # get cookie-attributes for RFC 2965 and Netscape protocols
        rfc2965_hdrs = cookie2_string#headers.getheaders("Set-Cookie2")
        ns_hdrs = cookie_string#headers.getheaders("Set-Cookie")

        rfc2965 = self._policy.rfc2965
        netscape = self._policy.netscape

        if ((not rfc2965_hdrs and not ns_hdrs) or
            (not ns_hdrs and not rfc2965) or
            (not rfc2965_hdrs and not netscape) or
            (not netscape and not rfc2965)):
            return []  # no relevant cookie headers: quick exit

        try:
            cookies = self._cookies_from_attrs_set(
                split_header_words(rfc2965_hdrs), request)  #rfc2965 cookie handler
        except Exception:
            _warn_unhandled_exception()
            cookies = []

        if ns_hdrs and netscape:
            try:
                # RFC 2109 and Netscape cookies
                ns_cookies = self._cookies_from_attrs_set(
                    parse_ns_headers(ns_hdrs), request)     #ns cookie handler
            except Exception:
                _warn_unhandled_exception()
                ns_cookies = []
            self._process_rfc2109_cookies(ns_cookies)

            # Look for Netscape cookies (from Set-Cookie headers) that match
            # corresponding RFC 2965 cookies (from Set-Cookie2 headers).
            # For each match, keep the RFC 2965 cookie and ignore the Netscape
            # cookie (RFC 2965 section 9.1).  Actually, RFC 2109 cookies are
            # bundled in with the Netscape cookies for this purpose, which is
            # reasonable behaviour.
            if rfc2965:
                lookup = {}
                for cookie in cookies:
                    lookup[(cookie.domain, cookie.path, cookie.name)] = None

                def no_matching_rfc2965(ns_cookie, lookup=lookup):
                    key = ns_cookie.domain, ns_cookie.path, ns_cookie.name
                    return key not in lookup
                ns_cookies = filter(no_matching_rfc2965, ns_cookies)

            if ns_cookies:
                cookies.extend(ns_cookies)

        return cookies
        '''

    def my_get_cookies(self,name):
        pass



if __name__ == '__main__':
    cookiejar = MyCookieJar()
    '''
        返回多个set-cookie头,逐个解析
        不同的web应用,http服务器,网络基础设施等,返回的Set-Cookie在格式上有差异


    '''
    #apache phpcms
    cookies_reponse = ['GKzSD_admin_username=e87ddEfBZJp4vlvTaO0qACznBKMHdjUxcpFEUa06s_539IE; expires=Sun, 14-Feb-2016 13:39:25 GMT',
                       'GKzSD_siteid=efb4nnx0Hx0vPefcedxrgg3qMNIwrJQbwE69KtWA; expires=Sun, 14-Feb-2016 13:39:25 GMT',
                       'GKzSD_userid=2b2bcuRYsU8ffKCl-m-rSwGcCWLdKmQorItloSUp; expires=Sun, 14-Feb-2016 13:39:25 GMT',
                       'GKzSD_admin_email=b23dApSHO2rS2zV6iGrc4JsUbslml_SNBK8SEPiFSh0CNFZt4bNt6ZWeoBbl; expires=Sun, 14-Feb-2016 13:39:25 GMT',
                       'GKzSD_sys_lang=8e466Fl7568RKAi430uqKBMPKBbexu1ZZJN_-gWWaFAcTQ; expires=Sun, 14-Feb-2016 13:39:25 GMT']
    #iis webshell
    cookies_reponse1 = ['ASPSESSIONIDCCCCTQAB=HPNJEIHANPMOJHGFOINOFBKG; path=/']

    cookiejar.my_make_cookies(cookies_reponse,[])