import sys
import subprocess
import random

ANSI = {
    "BOLD": "\x1b[1m",
    "BOLDR": "\x1b[1;91m",
    "ENDC": "\x1b[0m"
}

ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
NUM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def eprint(text, *args, **kwargs):
    print(ANSI["BOLDR"] + "Error :", text +
          ANSI["ENDC"], *args, file=sys.stderr, **kwargs)


def wprint(text, *args, **kwargs):
    print(ANSI["BOLD"] + "Warning :", text +
          ANSI["ENDC"], *args, file=sys.stderr, **kwargs)


def binput(prompt):
    str_input = input(prompt)
    bool_input = ['true', '1', 't', 'y', 'yes',
                  'false', '0', 'f', 'n', 'no']

    while str_input not in bool_input:
        str_input = input("\x1b[1F\x1b[K" + prompt)
    if str_input.lower() in bool_input[:7]:
        return True
    return False


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


use_diacritics = 'y'

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
    # Encrypt or Decrypt
    action = input(
        "Do you want to encrypt or decrypt a string ? (e/d)")
    while action not in ['e', 'd']:
        action = input(
            "Do you want to encrypt or decrypt a string ? (e/d)")

    # Random shuffle with key
    shuffle = binput("Do you want to use a key ? (y/n)")

    if shuffle is True:
        key = int(input("Enter a key (integer): "))
        random.Random(key).shuffle(ALPHA)
        random.Random(key).shuffle(NUM)
        print(ALPHA)

    # Encrypt plain text
    if action == 'e':

        if use_diacritics is False:
            plain = input("Enter a string:\n")
            while plain.isascii() is False:
                plain = input("Please use ASCII characters only: ")
        else:
            plain = unidecode(input("Enter a string:\n"))

        crypt_numeric = binput(
            "Do you want to encrypt numeric characters ? (y/n)")

        print("Encrypted text :\n" + encrypt(plain.lower(), crypt_numeric))

    # Decrypt cipher text
    elif action == 'd':

        cipher = input("Enter a string:\n")
        while cipher.isascii() is False:
            cipher = input("Please use ASCII characters only: ")

        crypt_numeric = binput(
            "Do you want to decrypt numeric characters ? (y/n)")

        print("Plain text :\n" + decrypt(cipher.lower(), crypt_numeric))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\x1b[2K\rProcess interrupted by user...")
        exit(1)
