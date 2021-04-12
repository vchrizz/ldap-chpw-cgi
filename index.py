#!/usr/bin/env python3
import cgi, cgitb
import re
import sys, os
import ldap

ldap_proto = 'ldap://'
ldap_server = 'localhost'
ldap_basedn = 'dc=ldap,dc=freiesnetz,dc=at'
ldap_userdn = 'ou=Users' +','+ ldap_basedn

cgitb.enable(display=0, logdir='logs/')


def check_form(formvars, form):
    for varname in formvars:
        if varname not in form.keys():
            return False
        else:
            if type(form[varname].value) is not type(''):
                return None
    return True


def read_template_file(filename, **vars):
    with open('tpl/' + filename, mode='r', encoding='utf-8') as f:
        template = f.read()
    for key in vars:
        template = template.replace('{$' + key + '}', vars[key])
    return template


def check_oldpw(accountname, oldpass):
    try:
        conn = ldap.initialize(ldap_proto+ldap_server)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        if conn.simple_bind("uid="+accountname+","+ldap_userdn, oldpass) == True:
            return True
    except ldap.INVALID_CREDENTIALS:
        conn.unbind()
        return False

    return False


def generate_headers():
    return "Content-Type: text/html; charset=utf-8\n"


def main():
    main_content = ''

    form = cgi.FieldStorage()
    http_host = os.environ.get('HTTP_HOST')
    if 'submit' in form.keys():
        formvars = ['accountname', 'oldpass', 'newpass', 'newpass2']
        form_ok = check_form(formvars, form)
        if form_ok == True:
            accountname = form['accountname'].value
            accountname = accountname.split("@")[0]
            oldpass = form['oldpass'].value
            newpass = form['newpass'].value
            newpass2 = form['newpass2'].value
            if newpass == newpass2:
                if check_oldpw(accountname, oldpass):
                    conn = ldap.initialize(ldap_proto+ldap_server)
                    conn.set_option(ldap.OPT_REFERRALS, 0)
                    conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                    conn.simple_bind(accountname, oldpass)
                    results = conn.search_s(ldap_basedn, ldap.SCOPE_SUBTREE, "(uid="+accountname+")", ["dn"])
                    conn.unbind()
                    for dn in results:
                        conn = ldap.initialize(ldap_proto+ldap_server)
                        conn.set_option(ldap.OPT_REFERRALS, 0)
                        conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                        # do a synchronous ldap bind
                        conn.simple_bind_s(dn[0], oldpass)
                        conn.passwd_s(dn[0], oldpass, newpass)
                        conn.unbind_s()
                    conn = ldap.initialize(ldap_proto+ldap_server)
                    conn.set_option(ldap.OPT_REFERRALS, 0)
                    conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                    if conn.simple_bind(accountname, newpass) == True:
                        # We did it
                        conn.unbind()
                        main_content = read_template_file('success.tpl', http_host=http_host)
                    else:
                        conn.unbind()
                        main_content = read_template_file('fail.tpl', message=cgi.escape(ldap.LDAPError))
                else:
                    main_content = read_template_file('fail.tpl', message='User not found or wrong password entered.')
            else:
                main_content = read_template_file('fail.tpl', message='Passwords do not match.')
        elif form_ok == False:
            main_content = read_template_file('fail.tpl', message='All fields are required.')
        else:
            main_content = read_template_file('fail.tpl', message='Invalid data type supplied.')
    else:
        formaction = cgi.escape("https://" + os.environ["HTTP_HOST"] + os.environ["REQUEST_URI"])
        #accountname = os.environ.get('REMOTE_USER')
        accountname = os.environ.get('AUTHENTICATE_UID')
        form = read_template_file('form.tpl', formaction=formaction, accountname=accountname, http_host=http_host)
        main_content = form

    response = generate_headers() + "\n"
    response += read_template_file('main.tpl', main_content=main_content)
    sys.stdout.buffer.write(response.encode('utf-8'))


if __name__ == "__main__":
    main()
