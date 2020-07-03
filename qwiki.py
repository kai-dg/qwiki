#!/usr/bin/env python3
import sys
from utils.argparsers import argparser
from utils.model_funcs import Query


def main():
    """
    a = Card.create(title="Hello World", content="", subcards=True)
    a.save()
    b = Subcard.create(card=a, title="Hello World Sub", content="This is a test")
    b.save()
    q1 = Card.select().where(Card.id==1)
    #c = Subcard.create(card=q1[0], title="Hello Japan", content="Test2")
    #c.save()
    q2 = Subcard.select().where(Subcard.card==q1[0])
    print(len(q2))
    print(q2[0].title)
    """
    args = sys.argv[1:]
    argparser(args)

def test():
    q = Query("bronze ingot")

if __name__ == "__main__":
    main()
