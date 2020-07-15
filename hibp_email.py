#!/usr/bin/python3
import os, sys, csv

def logo():
    print('''
##############################################################
##############################################################
#
# PYTHON 3
# HaveIBeenPwned EMAIL CREATION & DELIVERY SCRIPT v0.1
# Created by: Andrew Sturm
# Created on: 2020-07-13
#
##############################################################
##############################################################

This script will be used to notify users if their accounts are on HIBP.
It notifies the user via email and expires their Google password.

Usage: hibp_email.py ../csv/update.csv
''')

def clear():

    # Clear command for Windows
    if os.name == 'nt':
        _ = os.system('cls')

    # Clear command for Mac/*nix
    else:
        _ = os.system('clear')

def main():
# Start off with a clean slate
    clear()
    logo()

# Declare variables
    staffEmail = []
    dictPwned = {}
    emails = {}
    pwnedEmail = ""
    pwnedBreach = ""
    userChoice = ""

    while True:
        userChoice = input('''
In order for the script to work, CSVs must be located in ../csv and be named the following:
\'hibp.csv\' and \'staffemails.csv\'.

Are you ready to run the script? (Y/N): 
''')

        if userChoice.lower() not in ('y', 'n'):
            print('Invalid input.\n')
        else:
            break

    if userChoice.lower() == 'y':
        clear()
        logo()

# Call staffemails in .csv
        try:
            with open('../csv/staffemails.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    staffEmail.append(row['email'])
        except KeyboardInterrupt:
            print("Keyboard interrupt signal detected.\nExiting...")
            exit()

# Call hibp.csv
        try:
            with open(sys.argv[1], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['email'] in staffEmail:
                        pwnedEmail = row['email']
                        pwnedBreach = row['breach']
                        dictPwned.update({pwnedEmail:pwnedBreach})

        except KeyboardInterrupt:
            print("Keyboard interrupt signal detected.\nExiting...")
            exit()

        except IndexError:
            print("Invalid Argument.\n\nUsage: hibp_email.py ../csv/update.csv")
            exit()

# Begin emailing everyone in the list this message

        try:
            for key in dictPwned:
                pwnedEmail = key
                pwnedBreach = dictPwned[key]
                cmd = "../../gam user webmaster sendemail message \"This is an automated email to inform you that your account has appeared in a HaveIBeenPwned.com database. \
This means your email/password combination may be compromised.\n\nFor your safety, your Google password has been expired and will need to be changed shortly.\n\nNOTE: The \
following list may include items that you do not recognize. This is normal. \n\nListed Breaches: "+pwnedBreach+"\n\nPlease feel encouraged to search your \
email address(es) on https://www.HaveIBeenPwned.com for more information on what information may have been exposed.\n\nPlease do not respond to this email, the email is used for \
automation and is not monitored.\" subject \"HaveIBeenPwned.com Alert\" recipient " +pwnedEmail
                os.system(cmd)
                print("Notifying account owner and expiring password for "+pwnedEmail)

# Expire the password of the Google account
                cmd = "../../gam update user "+pwnedEmail+" changepassword on"
                os.system(cmd)

        except KeyboardInterrupt:
            print("Keyboard interrupt signal detected.\nExiting...")
            exit()


    elif userChoice.lower() == 'n':
        exit()

    exit()

# Call the main procedure
main()
