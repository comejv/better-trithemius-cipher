import sys
import subprocess
import random

ANSI = {
    "BOLD": "\x1b[1m",
    "BOLDR": "\x1b[1;91m",
    "UNDER": "\x1b[4m",
    "REVB": "\x1b[5;7m",
    "ENDC": "\x1b[0m"
}

ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
NUM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def clear():
    print("\x1b[2J\x1b[H")


def eprint(text, *args, **kwargs):
    print(ANSI["BOLDR"] + "Error :", text +
          ANSI["ENDC"], *args, file=sys.stderr, **kwargs)


def wprint(text, *args, **kwargs):
    print(ANSI["BOLD"] + "Warning :", text +
          ANSI["ENDC"], *args, file=sys.stderr, **kwargs)


def binput(prompt):
    str_input = input(ANSI['BOLD'] + prompt + ANSI['ENDC'])
    bool_input = ['true', '1', 't', 'y', 'yes', 'i',
                  'false', '0', 'f', 'n', 'no', 'p']

    while str_input not in bool_input:
        str_input = input("\x1b[1F\x1b[K" +
                          ANSI["BOLD"] + prompt + ANSI["ENDC"])
    if str_input.lower() in bool_input[:6]:
        return True
    return False


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


use_diacritics = 'y'

clear()
try:
    from unidecode import unidecode
except ImportError:
    wprint("Unidecode module not found.")
    use_diacritics = binput(
        "Do you want to install it or skip and continue without diacritic characters ?\n(y : install / n : pass)")
    if use_diacritics is True:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "unidecode"])
        from unidecode import unidecode
    else:
        wprint("Diacritics will not be handled.")


def encrypt(plain, crypt_numeric):
    """Encrypts each character according to its distance to the letter of the alphabet
    corresponding to its position in the string modulo 25.

    Args:
        plain (string): the text to encrypt
        crypt_numeric (bool): weather to encrypt numeric characters or not

    Returns:
        string: the encrypted text
    """
    cipher = ""
    counter_alpha, counter_num = 0, 0

    cipher = ""
    for c in plain:
        if c.isalpha():
            cipher += ALPHA[(ALPHA.index(c) + counter_alpha) % 26]
            counter_alpha += 1
            counter_alpha %= 26
        elif c.isnumeric() and crypt_numeric is True:
            cipher += NUM[(NUM.index(c) + counter_num) % 10]
            counter_num += 1
            counter_num %= 10
        else:
            cipher += c
    return cipher


def decrypt(cipher, crypt_numeric):
    """Decrypts each character according to its distance to the letter of the alphabet
    corresponding to its position in the string modulo 25.

    Args:
        cipher (string): the text to decrypt
        crypt_numeric (bool): weather to encrypt numeric characters or not

    Returns:
        string: the decrypted text
    """
    plain = ""
    counter_alpha, counter_num = 0, 0

    for c in cipher:
        if c.isalpha():
            plain += ALPHA[(ALPHA.index(c) - counter_alpha) % 26]
            counter_alpha += 1
            counter_alpha %= 26
        elif c.isnumeric() and crypt_numeric is True:
            plain += NUM[(NUM.index(c) - counter_num) % 10]
            counter_num += 1
            counter_num %= 10
        else:
            plain += c
    return plain


def main():
    clear()

    # Encrypt or Decrypt
    action = input(
        ANSI['BOLD'] + "Encrypt or Decrypt ? (e : encrypt / d : decrypt)" + ANSI['ENDC'])

    while action not in ['e', 'd']:
        action = input(
            ANSI['BOLD'] + "Encrypt or Decrypt ? (e : encrypt / d : decrypt)" + ANSI['ENDC'])

    # Random shuffle with key
    shuffle = binput("Do you want to use a key ? (y/n)")

    if shuffle is True:
        key = int(
            input(ANSI['BOLD'] + "Enter a key (integer): " + ANSI['ENDC']))
        random.Random(key).shuffle(ALPHA)
        random.Random(key).shuffle(NUM)
        print(ALPHA)

    clear()
    text = input("Enter a string:\n")
    if use_diacritics is False:
        while text.isascii() is False:
            text = input("Please use ASCII characters only:\n")
    else:
        text = unidecode(text)

    crypt_numeric = False
    if any(char.isdigit() for char in text):
        crypt_numeric = binput(
            "Do you want to encrypt numeric characters ? (y/n)")

    clear()

    # Encrypt plain text
    if action == 'e':
        print("Encrypted text :\n\n" + encrypt(text.lower(), crypt_numeric))

    # Decrypt cipher text
    elif action == 'd':
        print("Plain text :\n\n" + decrypt(text.lower(), crypt_numeric))

    input('\n\n' + ANSI["REVB"] + "PRESS ENTER TO CLEAR THE SCREEN" + ANSI['ENDC'])
    clear()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\x1b[2K\rProcess interrupted by user...")
        exit(1)
