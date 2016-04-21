#!/usr/bin/python
from datetime import datetime
from datetime import timedelta
'''
sc           :$1$$1q2w3e4r              :15460:  0  :  99999  :  7  :   :   :
|------1-----|---------------2----------|--3--|--4--|----5----|--6--|-7-|-8-|

1.	Username field: This field denotes the username (or the user account name), that should be used while logging in to the system.
2.	Password field: This field stores the password in encrypted format (explained in detail below).
3.	Last Password Change: This field denotes the number of days, since UNIX time (1-Jan-1970), the last password change happened.
4.	Minimum days between password changes: This field denotes the minimum number of days after which a user can change his password.
5.	Password validity: This field denoted the maximum number of days for which password is valid. After that, the password will expire and the user will have to change the password.
6.	Warning threshold: This field denotes the number of days before which the user will receive a warning notification about the password expiry.
7.	Account inactive: This field denotes the number of days after which the account will be disabled, when the password is expired.
8.	Time since account is disabled: This field denotes the number of days, from UNIX time, since which the account is disabled.


'''
def accountCreateData(day):
	now = datetime(1970,1,1)
	return now + timedelta(days=day)

#shadow file content
shadow = '''
root:$6$FhhyXXGoNYZSKTKm$WRX.s3ONYDxccJDE6qrxi6cIZA2E47y8aEg7sAG.d07EvGKf5ZDNitsFRnv8lBiJQVLYik6aQrJwyaeThC1zx.:16851:0:99999:7:::
bin:*:15980:0:99999:7:::
daemon:*:15980:0:99999:7:::
adm:*:15980:0:99999:7:::
lp:*:15980:0:99999:7:::
sync:*:15980:0:99999:7:::
shutdown:*:15980:0:99999:7:::
halt:*:15980:0:99999:7:::
mail:*:15980:0:99999:7:::
uucp:*:15980:0:99999:7:::
operator:*:15980:0:99999:7:::
games:*:15980:0:99999:7:::
gopher:*:15980:0:99999:7:::
ftp:*:15980:0:99999:7:::
nobody:*:15980:0:99999:7:::
vcsa:!!:16851::::::
saslauth:!!:16851::::::
postfix:!!:16851::::::
sshd:!!:16851::::::
apache:!!:16895::::::
tcpdump:!!:16896::::::
'''

rows = shadow.split('\n')

for row in rows:

    if len(row) == 0:
        continue
    else:
        items = row.split(':')
        print 'account: ', items[0]
        print 'password_information: '
        password_info = items[1].split('$')
        if len(password_info) == 1:
            print '\t',items[1]
        else:
            algorithm =  {
                '1':'MD5',
                '2':'Blowfish',
                '2a':'eksBlowfish',
                '5':'SHA-256',
                '6':'SHA-512'
            }
            print '\talgorithm: ' , algorithm[password_info[1]]
            print '\tsalt: ', password_info[2]
            print '\tencrypted password: ', password_info[3]

        print 'create: ', accountCreateData(int(items[2]))
        print '\r\n'
