from re import A
import sys
import subprocess

ANSI = {
    "RED": "\x1b[91m",
    "GREEN": "\x1b[92m",
    "BLUE": "\x1b[94m",
    "BOLD": "\x1b[1m",
    "BOLDR": "\x1b[1;91m",
    "BOLDG": "\x1b[1;92m",
    "ENDC": "\x1b[0m"
}


def eprint(text, *args, **kwargs):
    print(ANSI["BOLDR"] + "Error :", text +
          ANSI["ENDC"], *args, file=sys.stderr, **kwargs)


def wprint(text, *args, **kwargs):
    print(ANSI["BOLD"] + "Warning :", text +
          ANSI["ENDC"], *args, file=sys.stderr, **kwargs)


def binput(prompt):
    str_input = input(prompt)
    while str_input not in ['true', '1', 't', 'y', 'yes', 'o', 'oui', 'false', '0', 'f', 'n', 'no', 'non']:
        str_input = input("\x1b[1F\x1b[K" + prompt)
    if str_input.lower() in ['true', '1', 't', 'y', 'yes', 'o', 'oui']:
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
            cipher += chr(abs(ord(c) - (counter_alpha + 97)) + 97)
            counter_alpha += 1
            counter_alpha %= 26
        elif c.isnumeric() and crypt_numeric is True:
            cipher += chr(abs(ord(c) - (counter_num + 48)) + 48)
            counter_num += 1
            counter_num %= 10
        else:
            cipher += c
    return cipher


def main():
    action = input(
        "Do you want to encrypt or decrypt a string ? (e/d)")
    while action not in ['e', 'd']:
        action = input(
            "\x1b[1F\x1b[KDo you want to encrypt or decrypt a string ? (e/d)")

    # Encrypt plain text
    if action == 'e':

        if use_diacritics is False:
            plain = input("Enter a string:\n")
            while is_ascii(plain) is False:
                plain = input("Please use ASCII characters only: ")
        else:
            plain = unidecode(input("Enter a string:\n"))

        crypt_numeric = binput("Do you want to encrypt numeric characters ? (y/n)")

        print("Encrypted text :\n" + encrypt(plain, crypt_numeric))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user...")
        exit(1)
