import sys
from keypad_read import *
from time_lockout import *
from led_display import *
from console_clear import *
from led_flash import *
from logfile import *
from menu import *
from global_variables import *

def read_from_file():
    '''
    This function tries to get the passwords from the config csv file.
    If the file isn't found, it sets the passwords to the default values of '1234'
    and '9999'
    and returns them in a list.
    '''
    try:
        dico = read()
        passwords = [str(dico['PASSWORD']),str(dico['ADMIN_PASSWORD'])]
    except IOError:
        passwords = ['1234', '9999']

    return tuple(passwords)

#print(read_from_file())


def password_read(passwords):
    '''
    This function reads the sequence entered by the user, displays it in the console
    and compares it to the password read from Read_From_File() function.
    It compares both digit-by-digit, so as soon as the wrong digit is entered,
    it flashed the red LED and returns False. If the whole password was entered
    correctly, it returns True
    '''
    password_input = '' #This variable will hold the sequence entered by the user
    sys.stdout.flush()
    console_clear()
    sys.stdout.write("Enter password:\n")

    for i in range(len(passwords[0])):
        if i == 0: #If nothing has been entered yet, wait for the input indifinitely
            letter = str(keypad_read())
        else: #If it's the 2nd or nth entered number, wait only for the INTER_DIGIT time
            letter = str(keypad_read(3))

        letters = [x[i] for x in passwords]

        password_input += letter
        led_display(password_input)

        if (letter not in letters):
            logtime(False)
            sys.stdout.write("\nACCESS DENIED\n")
            flash_red()
            return False

    if password_input == passwords[0]:
        sys.stdout.write("\nACCESS GRANTED\n")
        logtime(True)
        flash_green()
        return True
    elif password_input == passwords[1]:
        logtime(True)
        print_line(0, read_menu())
        return True
    else:
        logtime(False)
        sys.stdout.write("\nACCESS DENIED\n")
        flash_red()
        return False

def safe_password_read(passwords):
    '''
    This function implements the 'Remove side-channel vulnerability' optional
    software functionality. It's the safe version of the basic passwordRead() function.
    It reads the sequence entered by the user, displays it in the console
    and compares it to the password read from ReadFromFile() function.
    It only compares the entered sequence and the password from the file when there
    are 4 digits entered, which makes it safe and not vulnerable for the side-channel
    attacks.
    If the whole password was entered correctly, it returns True.
    '''
    password_input = '' #This variable will hold the sequence entered by the user
    sys.stdout.flush()
    console_clear()
    sys.stdout.write("Enter password:\n")

    for i in range(len(passwords[0])):
        if i == 0: #If nothing has been entered yet, wait for the input indifinitely
            letter = str(keypad_read())
        else: #If it's the 2nd or nth entered number, wait only for the INTER_DIGIT time
            letter = str(keypad_read(3))

        password_input += letter
        led_display(password_input)

    if password_input == passwords[0]:
        sys.stdout.write("\nACCESS GRANTED\n")
        logtime(True)
        flash_green()
        return True
    elif password_input == passwords[1]:
        logtime(True)
        print_line(0, read_menu())
        return True
    else:
        logtime(False)
        sys.stdout.write("\nACCESS DENIED\n")
        flash_red()
        return False
