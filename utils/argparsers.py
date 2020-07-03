#!/usr/bin/env python3
import sys
import utils.argfuncs as f
from utils.helpers import print_helps
COMMANDS = {
    "add": f.add_page,
    "update": f.update_page,
    "delete": f.delete_page,
    "q": f.query_page
}
HELPS = {
    "help": 0,
    "-help": 0,
    "-h": 0,
    "h": 0
}


def argparser(args:list):
    if len(args) == 0:
        sys.exit("Error >>> Please enter a command.")
    if len(args) > 1:
        COMMANDS[args[0]](args[1:])
    elif len(args) == 1 and COMMANDS.get(args[0], "") != "":
        COMMANDS[args[0]]()
    elif HELPS.get(args[0], "") != "":
        print_helps()
    else:
        sys.exit(f"Error >>> {args[0]} is not a valid command.")

if __name__ == "__main__":
    pass
