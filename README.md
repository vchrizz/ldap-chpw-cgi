# LDAP chpw CGI

This is a Python CGI script that lets ldap users change
their own ldap passwords via a web interface.

If users with same UID and same oldpassword are found in other OUs,
those passwords are updated too.

## Installation
To install the script, simply extract all the repository contents into a folder
under your document root. No paths need to be configured. Only make sure that the
location is reachable via HTTPS. If used with Apache2, this module is required: `a2enmod authnz_ldap`

Configure LDAP settings for your LDAP server in index.py:
```
ldap_proto = 'ldap://'
ldap_server = 'localhost'
ldap_basedn = 'dc=ldap,dc=freiesnetz,dc=at'
ldap_userdn = 'ou=Users' +','+ ldap_basedn
ldap_bind_attr = 'uid'
```

Configure LDAP settings for your LDAP server in .htaccess:
```
AuthLDAPBindDN UID=bind,OU=Users,DC=ldap,DC=freiesnetz,DC=at
AuthLDAPBindPassword ldapbindpassword
AuthLDAPURL ldap://localhost/OU=Users,DC=ldap,DC=freiesnetz,DC=at?uid
```

## Acknowledgements
This is a majorly for ldap-support rewritten version of a script originally developed by Dirk Boye.
See [dirkboye/mailpw_change](https://github.com/dirkboye/mailpw_change) at GitHub
for the original source code.

## FAQ
* *Q:* Can I use the script via unencrypted HTTP?<br>
  *A:* No, HTTPS is hard-coded. So unless you change that in the code, you can't.
  And honestly, you really shouldn't.

* *Q:* Do I need to put the script in `/cgi-bin/`?<br>
  *A:* In most cases, no. The script comes with an `.htaccess` that enables CGI
  execution for the current directory. Generally, that should work. If not, your
  administrator may have disabled option overriding in which case you actually
  need to put it in `/cgi-bin/`. But in most cases (and especially on Uberspaces)
  it should work just fine.

* *Q:* I only get an error 500 and the log file says something about suEXEC
  policy violation. How do I fix that?<br>
  *A:* Make sure both the `index.py` as well as the containing directory have
  the permissions `0755`. Any higher permissions will usually result in that error.
  If you have trouble finding the root cause, possibly a look at `journalctl -b`
  will help you.
