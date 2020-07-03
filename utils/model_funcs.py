#!/usr/bin/env python3
from utils.models import Card
from utils.models import Content
from utils.models import Subcontent
import utils.checks as c


class CardInput:
    """Titles and contents should align with each other's indexes.
    self.format helps with displaying the page in terminal.
    """
    def __init__(self):
        self.card = None
        self.name = ""
        self.notes = ""
        self.format = ""
        self.titles = []
        self.contents = []

    def add(self):
        self.name = input("New page name: ").title()
        self.notes = input("Notes (Can leave blank): ")

    def add_by_text(self, data):
        self.name = data["name"]
        self.notes = data["notes"]

    def format_content(self, f):
        self.format = f
        c_idx = 1
        for i in f.split():
            res = []
            if i == "c":
                self.titles.append(input(f"[{c_idx}] Content Title: ").title())
                c_idx += 1
            if i == "s":
                self.titles.append(input("Subcontent Title: ").title())
            bullets = c.is_int(input(">>> How many bullet points? "))
            if bullets == 0:
                self.contents.append("")
            else:
                for b in range(bullets):
                    res.append(input("Content: ").capitalize())
                self.contents.append("\n".join(res))

    def format_content_by_text(self, data):
        self.titles.append(data["title"])
        self.contents.append(data["contents"])

class CardController:
    def __init__(self):
        self.card = None
        self.cont = None
        self.subcont = None

    def add_card(self, card_input):
        """card_input (obj): CardInput object"""
        card = Card.create(
            name = card_input.name,
            notes = card_input.notes,
            card_format = card_input.format
        )
        card.save()
        self.card = card

    def add_content(self, data):
        if data["content_type"] == True:
            cont = Content.create(
                card = self.card,
                title = data["title"],
                content = data["content"],
                subcontent = data["subcont"]
            )
            cont.save()
            self.cont = cont
        if data["subcont_type"] == True:
            subcont = Subcontent.create(
                card = self.cont,
                title = data["title"],
                content = data["content"]
            )
            subcont.save()
            self.subcont = subcont

    def update_card(self, data):
        pass

    def update_content(self, data):
        pass

    def delete_card(self, data):
        pass

    def delete_content(self, data):
        pass

class Query:
    def __init__(self, name):
        """self.contents format:
            idx: {
                "c": Content,
                "s": List of Subcontents
            },
            ...
        """
        self.name = name.title()
        self.card = None
        self.contents = {}
        self.find_cards()

    def find_cards(self):
        q = Card.select().where(Card.name==self.name)
        self.card = c.card_exists(q, self.name)
        conts = Content.select().where(Content.card==self.card)
        for i in range(len(conts)):
            self.contents[i] = {"c": conts[i]}
            if conts[i].subcontent:
                self.contents[i]["s"] = Subcontent.select().where(Subcontent.card==conts[i])

class Display:
    """Should take in a Query object"""
    def __init__(self, query):
        self.query = query

    def card(self):
        print(f"=== {self.query.name} ===")
        print(f"[Notes] {self.query.card.notes}\n")
        conts = self.query.contents
        for i in conts:
            print(f"+ {conts[i]['c'].title}")
            if conts[i]["c"].content != "":
                temp = conts[i]["c"].content.replace("\n", "\n    - ")
                print("    - " + temp)
            if conts[i]["c"].subcontent:
                for s in conts[i]["s"]:
                    print(f"    ++ {s.title}")
                    temp = s.content.replace("\n", "\n      - ")
                    print("      - " + temp)
            print()

if __name__ == "__main__":
    pass
