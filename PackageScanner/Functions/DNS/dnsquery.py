#!/usr/bin/python
#coding=utf-8

from PackageScanner.Functions.DNS.dnslib.dns import *


'''
从root节点开始查询

如果auth区块中包含域名 && addition区块中包含域名对应ip则结束
auth区块中可能包含不同top level domian的域名,需要重新开始解析

;; AUTHORITY SECTION:
授权响应对应域名的记录

;; ADDITIONAL SECTION:

'''
top_level_nameservers = [
    {'type': 'A', 'address': '198.41.0.4'},
    {'type': 'A', 'address': '192.228.79.201'},
    {'type': 'A', 'address': '192.33.4.12'},
    {'type': 'A', 'address': '199.7.91.13'},
    {'type': 'A', 'address': '192.203.230.10'},
    {'type': 'A', 'address': '192.5.5.241'},
    {'type': 'A', 'address': '192.112.36.4'},
    {'type': 'A', 'address': '198.97.190.53'},
    {'type': 'A', 'address': '192.36.148.17'},
    {'type': 'A', 'address': '192.58.128.30'},
    {'type': 'A', 'address': '193.0.14.129'}]

class resolver:
    #Google's DNS servers are only used if zero resolvers are specified by the user.
    pos = 0
    rcode = ""
    wildcards = {}
    failed_code = False
    last_resolver = ""

    def __init__(self, nameservers = ['8.8.8.8']):
        self.nameservers = nameservers

    def query(self, hostname, query_type = 'ANY', name_server = False, use_tcp = False):
        ret = []
        response = None
        if name_server == False:
            name_server = self.get_ns()
            #print name_server
        else:
            self.wildcards = {}
            self.failed_code = None
        self.last_resolver = name_server
        query = DNSRecord.question(hostname, query_type.upper().strip())
        try:
            response_q = query.send(name_server, 53, use_tcp)
            if response_q:
                response = DNSRecord.parse(response_q)
            else:
                raise IOError("Empty Response")
        except Exception as e:
            #IOErrors are all conditions that require a retry.
            raise IOError(str(e))
        if response:
            self.rcode = RCODE[response.header.rcode]
            for r in response.rr:
                try:
                    rtype = str(QTYPE[r.rtype])
                except:#Server sent an unknown type:
                    rtype = str(r.rtype)
                #Fully qualified domains may cause problems for other tools that use subbrute's output.
                rhost = str(r.rname).rstrip(".")
                ret.append((rhost, rtype, str(r.rdata)))
            #What kind of response did we get?
            if self.rcode not in ['NOERROR', 'NXDOMAIN', 'SERVFAIL', 'REFUSED']:
                pass
                #trace('!Odd error code:', self.rcode, hostname, query_type)
            #Is this a perm error?  We will have to retry to find out.
            if self.rcode in ['SERVFAIL', 'REFUSED', 'FORMERR', 'NOTIMP', 'NOTAUTH']:
                #查询过于频繁,返回该错误
                raise IOError('DNS Failure: ' + hostname + " - " + self.rcode)
            #Did we get an empty body and a non-error code?
            elif not len(ret) and self.rcode != "NXDOMAIN":
                raise IOError("DNS Error - " + self.rcode + " - for:" + hostname)
        return ret

    def was_successful(self):
        ret = False
        if self.failed_code and self.rcode != self.failed_code:
            ret = True
        elif self.rcode == 'NOERROR':
            ret = True
        return ret

    def get_returncode(self):
        return self.rcode

    def get_ns(self):
        if self.pos >= len(self.nameservers):
            self.pos = 0
        ret = self.nameservers[self.pos]
        # we may have metadata on how this resolver fails
        try:
            ret, self.wildcards, self.failed_code = ret
        except:
            self.wildcards = {}
            self.failed_code = None
        self.pos += 1
        return ret

    def add_ns(self, resolver):
        if resolver:
            self.nameservers.append(resolver)

    def get_authoritative(self, hostname):
        ret = []
        while not ret and hostname.count(".") >= 1:
            try:
                #trace("Looking for nameservers:", hostname)
                nameservers = self.query(hostname, 'NS')
                print 'nameservers',nameservers
            except IOError:#lookup failed.
                nameservers = []
            for n in nameservers:
                #A DNS server could return anything.
                rhost, record_type, record = n
                if record_type == "NS":
                    #Return all A records for this NS lookup.
                    import time
                    time.sleep(2)
                    a_lookup = self.query(record.rstrip("."), 'A')
                    for a_host, a_type, a_record in a_lookup:
                        print a_host, a_record
                        ret.append(a_record)
                #If a nameserver wasn't found try the parent of this sub.
            hostname = hostname[hostname.find(".") + 1:]
        return ret

    def get_last_resolver(self):
        return self.last_resolver
def recursion_reuqest_a_record(hostname, nameserver = qq_nameservers):
    query = dnslib.DNSRecord.question(hostname, 'A')
    try:
        response_q = None
        for i in range(0,3):
            try:
                import random
                index = random.randint(0,len(nameserver)-1)
                use_ipv6 = False
                if nameserver[index]['type'] == 'AAAA':
                    use_ipv6 = True
                response_q = query.send(nameserver[index]['address'], 53, False, timeout=5, ipv6=use_ipv6)
                if response_q: break
            except:
                continue

        if response_q:
            response = dnslib.DNSRecord.parse(response_q)

            if len(response.rr):
                r = []
                for a_record in response.rr:
                    r.append({'type':str(dnslib.QTYPE[a_record.rtype]),'address':str(a_record.rdata)})
                print hostname, r
                return r

            if len(response.auth) == 0 and len(response.ar) == 0:
                raise Exception('AUTHORITY, ADDITIONAL both None')

            auth_section_ns_name = []
            #获取Auth区中的NS记录
            if len(response.auth):
                for auth_record in response.auth:
                    rtype = str(dnslib.QTYPE[auth_record.rtype])
                    if rtype == 'NS':
                        auth_section_ns_name.append(str(auth_record.rdata).rstrip("."))

            #获取Additional中NS记录的A记录
            addition_section_records = dict((k, []) for k in auth_section_ns_name)
            if len(response.ar):
                for addition_record in response.ar:
                    rtype = str(dnslib.QTYPE[addition_record.rtype])
                    if rtype in ['A','AAAA']:
                        rname = str(addition_record.rname).strip(".")
                        ns = addition_section_records.get(rname)
                        ns.append({'type':rtype,'address':str(addition_record.rdata)})

            if len(response.ar) <= len(response.auth):
                for ns_name, ns_ip in addition_section_records.items():
                    if len(ns_ip) == 0:
                        addition_section_records[ns_name]=recursion_reuqest_a_record(ns_name)

            #合并当前相应中的Auth区中的ns记录,用于查询域名
            nameservers = []
            for k,v in addition_section_records.items():
                nameservers.extend(v)
                #print k, v

            return recursion_reuqest_a_record(hostname, nameservers)


        else:
            raise Exception('%s 解析失败' % (hostname))

    except Exception as e:
        print e

    return [{'type':'A','address':''}]

def recursion_reuqest_ns_record(domain_name, nameserver):
    query = DNSRecord.question(domain_name, 'NS')
    response_q = None
    for i in range(0,3):
        try:
            import random
            index = random.randint(0,len(nameserver)-1)
            use_ipv6 = False
            if nameserver[index]['type'] == 'AAAA':
                use_ipv6 = True
            response_q = query.send(nameserver[index]['address'], 53, False, timeout=5, ipv6=use_ipv6)
            if response_q: break
        except:
            continue

    if response_q:
        response = DNSRecord.parse(response_q)

        if len(response.auth) == 0 and len(response.ar) == 0:
            raise Exception('AUTHORITY, ADDITIONAL both None')

        auth_section_ns_name = []
        domain_nameservers=[]
        #获取Auth区中的NS记录
        if len(response.auth):
            for auth_record in response.auth:
                rtype = str(QTYPE[auth_record.rtype])
                rname = str(auth_record.rname).rstrip(".")
                rdata = str(auth_record.rdata).rstrip(".")
                if rtype == 'NS':
                    if rname == domain_name:
                        domain_nameservers.append(rdata)

                    auth_section_ns_name.append(rdata)

        #获取Additional中NS记录的A记录
        addition_section_records = dict((k, []) for k in auth_section_ns_name)
        if len(response.ar):
            for addition_record in response.ar:
                rtype = str(QTYPE[addition_record.rtype])
                if rtype in ['A','AAAA']:
                    rname = str(addition_record.rname).strip(".")
                    ns = addition_section_records.get(rname)
                    ns.append({'type':rtype,'address':str(addition_record.rdata)})

        r = resolver()
        nameservers = []
        for ns_name, ns_ip in addition_section_records.items():
                if len(ns_ip) == 0:
                    a_records = r.query(hostname=ns_name, query_type='A')
                    for a_record in a_records:
                        rname, rtype, rdata = a_record
                        nameservers.append({'type':'A','address':rdata})
                        ns_ip.append({'type':'A','address':rdata})
                nameservers.extend(ns_ip)

        if len(domain_nameservers):
            return addition_section_records

        return recursion_reuqest_ns_record(domain_name, nameservers)


    else:
        raise Exception('%s 解析失败' % (domain_name))



if __name__ == '__main__':
        #t = []
    #for ns in qq_nameservers:
    #    t.append({'type':'A','address':ns})
    #print t
    #r = resolver()
    #auth_ns_servers = r.get_authoritative('qq.com')
    #print auth_ns_servers
    r = recursion_reuqest_ns_record('sina.cn', top_level_nameservers)
    for k,v in r.items():
        print k,v