from getpass import getpass
import math
import subprocess
import os

def eval_input(x,y,message=''):
    choice = input(message)
    if choice==x:
        return True
    elif choice==y:
        return False
    else:
        print('Invalid input. Try again\n')
        return eval_input(x,y)

def encrypt():
    encoded_data = int.from_bytes(getpass('Enter string to be encrypted:\n').encode(),'big')
    key = int.from_bytes(getpass('Enter Key:\n').encode(),'big')
    try:
        with open('passwords.txt') as pwds:
            num = len(pwds.read().split('\n'))
    except FileNotFoundError:
        os.system('touch passwords.txt')
        num = 1
    key_hashed = int(float("{:.25f}".format(key%(num*math.pi)))*10**25)
    encrypted_data = encoded_data+key_hashed
    print(f"Here is the encrypted string: {encrypted_data}")
    if eval_input('y','n','Would you like to store the encrypted string in passwords.txt (y/n)?\n'):
        label = input('Enter label for the encrypted string:\n')
        with open('passwords.txt','a') as pwds:
            pwds.write(f'{label}: {encrypted_data}\n')
            print('Successfully updated. Here is what passwords.txt looks like now:\n')
        with open('passwords.txt') as pwds:
            print(pwds.read()+'\n')

def decrypt():
    while True:
        try:
            line = str(subprocess.check_output('grep -n \''+input('Enter label (or part of label) of encrypted string:\n')+'\' passwords.txt',shell=True))[2:]
        except Exception:
            print('Input label not found in file or file does not exist. Try again.')
            continue
        if len(line.split('\\n'))!=2:
            print('Input label not specific enough. Try again.')
        else:
            break
    num = int(line[0:line.index(':')])
    encrypted_data = int(''.join(filter(str.isdigit, line[line.index(':'):])))
    key = int.from_bytes(getpass('Enter Key:\n').encode(),'big')
    key_hashed = int(float("{:.25f}".format(key%(num*math.pi)))*10**25)
    encoded_data = int(encrypted_data-key_hashed)
    data = encoded_data.to_bytes((encoded_data.bit_length()+7)//8,'big').decode()
    print(f'Here is the decrypted string: {data}')
    if eval_input('y','n','Clear screen? (y/n)\n'):
        os.system('clear')

if eval_input('n','d','Encrypt or decrypt (n/d)?\n'):
    encrypt()
else:
    decrypt()

