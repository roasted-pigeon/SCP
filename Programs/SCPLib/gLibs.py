import os
import socket
import getpass
import sys

import settings

from colorama import Fore as FColor, Back as BColor, Style


def cls():
    if sys.stdin.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')


def printError(text: str):
    print(FColor.RED, end='')
    print(text, end='')
    print(Style.RESET_ALL)


def noLogException(exception: Exception):
    printError("Произошла ошибка!")
    if hasattr(exception, 'message'):
        printError(exception.message if settings.debug else settings.veiledError)
    else:
        printError(exception if settings.debug else settings.veiledError)
    sys.exit()


def auth():
    try:
        login = input("Введите логин: ")
        # password = sys.stdin.readline().rstrip()
        if sys.stdin.isatty():
            password = getpass.getpass(prompt="Введите пароль: ", stream=sys.stderr)
        else:
            printError("Внимание! Ошибка инициализации скрытого ввода пароля! Пароль будет отображён.")
            password = input("Введите пароль: ")
        return login, password
    except Exception as exception:
        noLogException(exception)


def has_connection(hostname: str):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass  # we ignore any errors, returning False
    return False
