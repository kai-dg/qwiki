#!/usr/bin/env python3
from utils.model_funcs import CardInput
from utils.model_funcs import CardController
from utils.model_funcs import Query
from utils.model_funcs import Display
import utils.checks as c
import utils.parsers as parser
CARD_INPUT = CardInput()
CARD_CTRL = CardController()


def add_page():
    """Creates a card first, then parses the format to create the
    content for it"""
    CARD_INPUT.add()
    card_format = c.card_format(input("Enter content format: "))
    CARD_INPUT.format_content(card_format)
    new = CARD_CTRL.add_card(CARD_INPUT)
    card_format = card_format.split()
    for i in range(len(card_format)):
        data = {"subcont": False, "subcont_type": False, "content_type": False}
        data["title"] = CARD_INPUT.titles[i]
        data["content"] = CARD_INPUT.contents[i]
        if card_format[i] == "c":
            if card_format[i + 1] == "s":
                data["subcont"] = True
            data["content_type"] = True
        if card_format[i] == "s":
            data["subcont_type"] = True
        CARD_CTRL.add_content(data)
    print("Created a new wiki page:")
    # Display wiki page
    q = Query(CARD_INPUT.name)
    d = Display(q.card)

def add_page_text():
    pass

def update_page():
    pass

def delete_page():
    pass

def query_page(name=""):
    name = " ".join(name)
    q = Query(name)
    d = Display(q)
    d.card()

if __name__ == "__main__":
    pass
