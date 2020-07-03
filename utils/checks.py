#!/usr/bin/env python3
"""Every check should sys.exit if fails, otherwise pass return None"""
import sys
from utils.models import Card


def card_format(args:str):
    """Checks the card's content format.
    'c' is for a content slot.
    's' is for a subcontent slot.
    """
    accepted = {
        "c": 0,
        "s": 0
    }
    for i in args.split():
        if accepted.get(i, "") == "":
            sys.exit("Error >>> {i} is not a card format. Only use 'c' or 's'.")
    return args

def is_int(num):
    try:
        num = int(num)
        return num
    except ValueError:
        sys.exit("Error >>> Not a number.")

def card_exists(cards, name):
    if len(cards) == 0:
        sys.exit(f"Error >>> Page for {name} does not exist.")
    if len(cards) > 2:
        print("select card")
        # Return selected
    return cards[0]

if __name__ == "__main__":
    pass
