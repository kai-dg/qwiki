#!/usr/bin/env python3
"""Classes that hold models for dynamic database swapping.
These models are controllers for adding, updating, and deleting from db.
"""
from difflib import SequenceMatcher as SM
import utils.models as db


class ModelCtrl:
    """Controls all model's create, update, and delete methods"""
    def __init__(self):
        """Switch to another db by overwriting this class by initing
        it again.
        """
        self.page = db.Page
        self.cont = db.Content
        self.tag = db.Tag
        self.dd_info = db.DatabaseInfo
        #self.rel = db.Relations

    def add_page(self, data:dict) -> dict:
        """Args:
            data: keys are name, notes, img_path, img_title
        Returns:
            res: contains Page model obj and a message for display
        """
        p = self.page.create(
            name = data["name"].title().rstrip(),
            notes = data["notes"].capitalize().rstrip(),
            img_path = "",
            img_title = ""
        )
        p.save()
        return p

    def add_content(self, data:dict, target):
        """Args:
            data: {idx: {title: content}, ...}
            target: s.TARGET_PAGE
        """
        for k, v in data.items():
            res = self.cont.create(
                page = target,
                title = v["title"].title().rstrip(),
                idx = k,
                content = v["cont"].capitalize().rstrip(),
                content_img = "",
                content_img_title = ""
            )
            res.save()

    def update_page(self, target_name, data):
        """Data keys: name, notes"""
        q = None
        if data["name"] != "" and data["notes"] != "":
            q = (db.Page.update(name=data["name"], notes=data["notes"]).
                 where(db.Page.name==target_name))
            q.execute()
        elif data["name"] != "":
            q = (db.Page.update(name=data["name"].title().rstrip()).
                 where(db.Page.name==target_name))
            q.execute()
        else:
            q = (db.Page.update(notes=data["notes"].capitalize().rstrip()).
                 where(db.Page.name==target_name))
            q.execute()
        return q

    def update_content(self, target_page, data):
        """data keys: title, idx, content
        TODO: implement idx swapping
        """
        q = None
        if data.get("title", "") != "":
            q = (db.Content.update(title=data["title"].title().rstrip()).
                 where(db.Content.page==target_page,
                 db.Content.idx==data["idx"]))
            q.execute()
        else:
            q = (db.Content.update(content=data["content"].capitalize().rstrip()).
                 where(db.Content.page==target_page,
                 db.Content.idx==data["idx"]))
            q.execute()
        return q

    def set_tag(self, new:str) -> str:
        """`new` should be just the tag without commas."""
        q = self.d_info.select()[0] # Only 1 column should exist
        res = f"{q.set_tags},{new}"
        save = (self.d_info.update({self.d_info.set_tags:res}).where(self.d_info.id==1))
        return f"Made new tag {new}"

class Query:
    def __init__(self):
        self.tag = db.Tag
        self.page = db.Page
        self.content = db.Content
        #self.rel = db.Relations

    def pages(self, name):
        q = self.page.select().where(self.page.name==name)
        return q

    def page_content(self, target):
        """Args:
            target: s.TARGET_PAGE
        """
        q = self.content.select().where(self.content.page==target)
        return q

    def full_page_match(self, name) -> list:
        p = self.page.select().where(self.page.name==name)
        if len(p) == 1:
            return p
        return []

    def fuzzy_finder(self, query, target):
        return SM(None, target, query).ratio()

    def fuzzy_page_match(self, name) -> list:
        """iterator method needed for less mem by no caching"""
        res = []
        maxi = 0
        tolerance = 0.55
        for p in self.page.select().iterator():
            perc = self.fuzzy_finder(p.name, name)
            if perc > tolerance:
                if maxi < perc:
                    maxi = perc
                    res.insert(0, p)
                else:
                    res.append(p)
        return res
        