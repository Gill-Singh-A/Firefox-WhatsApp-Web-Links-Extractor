#! /usr/bin/env python3

import os, subprocess
from pathlib import Path
from datetime import date
from optparse import OptionParser
from colorama import Fore, Back, Style
from time import strftime, localtime

status_color = {
    '+': Fore.GREEN,
    '-': Fore.RED,
    '*': Fore.YELLOW,
    ':': Fore.CYAN,
    ' ': Fore.WHITE
}

folder_name = ".mozilla"
default_path = Path.home() / folder_name

def display(status, data, start='', end='\n'):
    print(f"{start}{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}", end=end)

def get_arguments(*args):
    parser = OptionParser()
    for arg in args:
        parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
    return parser.parse_args()[0]

def correctLink(link):
    for i in range(len(link)):
        if link[i:].startswith("http"):
            return link[i:]
    return ''

if __name__ == "__main__":
    arguments = get_arguments(('-p', "--path", "path", f"Path to Firefox Cache Folder (Default={default_path})"),
                              ('-w', "--write", "write", "Write to File (Default=Current Date and Time)"))
    if not arguments.path:
        arguments.path = default_path
    if not os.path.isdir(arguments.path):
        display('-', f"No Directory as {Back.YELLOW}{arguments.path}{Back.RESET}")
        exit(0)
    if not arguments.write:
        arguments.write = f"{date.today()} {strftime('%H_%M_%S', localtime())}"
    paths = []
    for path, folders, files in os.walk(arguments.path):
        if "whatsapp" in path:
                paths.extend([f"{path}/{file}" for file in files if "sqlite" in file])
    links = []
    for path in paths:
        links.extend([correctLink(link) for link in subprocess.check_output(["strings", f"{path}"]).decode().split('\n') if "http" in link])
    links = list(set(links))
    links.sort()
    display('+', f"Links Extracted => {Back.MAGENTA}{len(links)}{Back.RESET}")
    print('\n'.join([f"* {Fore.CYAN}{link}{Fore.RESET}" for link in links]))
    with open(arguments.write, 'w') as file:
        file.write('\n'.join(links))