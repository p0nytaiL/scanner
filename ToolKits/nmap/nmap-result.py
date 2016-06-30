#!/opt/local/bin/python
from xml.etree import ElementTree

def parseNmapResult(file):
    result = set()
    node_nmap = ElementTree.parse(file)
    nodes_address = node_nmap.getiterator('address')
    for node_address in nodes_address:
        result.add(node_address.attrib['addr'])

    print '%d hosts from %s' % (len(result), file)
    return result



if __name__ == '__main__':
   files =['PE','PP','PA','PS','PS8000-9000']
   alive_hosts = set()
   for file in files:
       alive_hosts_old = alive_hosts
       alive_hosts = alive_hosts | parseNmapResult(file)
       new_alive_hosts = alive_hosts - alive_hosts_old
       print '\t%d alive hosts found in %s' % (len(new_alive_hosts), file)
       for ip in new_alive_hosts:
           print '\t',ip

   print 'total %d hosts alive' % (len(alive_hosts))
   f = open('result.txt','w')
   for ip in alive_hosts:
       f.write(ip + '\r\n')
   f.close()

