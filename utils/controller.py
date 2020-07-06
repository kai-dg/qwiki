#!/usr/bin/env python3
"""Classes that hold models for dynamic database swapping.
These models are controllers for adding, updating, and deleting from db.
"""
from difflib import SequenceMatcher as SM


class ModelCtrl:
    """Controls all model's create, update, and delete methods"""
    def __init__(self, dpage, dcontent, dtag, ddinfo, drel):
        """Switch to another db by overwriting this class by initing
        it again.
        """
        self.page = dpage
        self.cont = dcontent
        self.tag = dtag
        self.rel = drel
        self.d_info = ddinfo

    def add_page(self, data:dict) -> dict:
        """Args:
            data: keys are name, notes, img_path, img_title
        Returns:
            res: contains Page model obj and a message for display
        """
        res = {}
        p = self.page.create(
            name = data["name"],
            notes = data["notes"],
            img_path = "",
            img_title = ""
        )
        p.save()
        res["message"] = f"Added Page: {data['name']}"
        res["page"] = p
        return res

    def add_content(self, data:dict, target) -> str:
        """Args:
            data: {idx: {title: content}, ...}
            target: page obj
        Returns:
            str: message for display
        """
        for k, v in data.items():
            res = self.cont.create(
                title = v["title"],
                idx = k,
                content = v["cont"],
                content_img = "",
                content_img_title = ""
            )
            res.save()
            target.content.add(res)
        return ""

    def set_tag(self, new:str) -> str:
        """`new` should be just the tag without commas."""
        q = self.d_info.select()[0] # Only 1 column should exist
        res = f"{q.set_tags},{new}"
        save = (self.d_info.update({self.d_info.set_tags:res}).where(self.d_info.id==1))
        return f"Made new tag {new}"

class Query:
    def __init__(self, name, dpage, drel, dtag=None):
        self.tag = dtag
        self.page = dpage
        self.rel = drel
        self.name = name

    def full_page_match(self) -> list:
        p = self.page.select().where(self.page.name==self.name)
        if len(p) == 1:
            return p
        return []

    def fuzzy_finder(self, query, target):
        return SM(None, target, query).ratio()

    def fuzzy_page_match(self) -> list:
        """iterator method needed for less mem by no caching"""
        res = []
        maxi = 0
        tolerance = 0.62
        for p in self.page.select().iterator():
            perc = self.fuzzy_finder(p.name, self.name)
            if perc > tolerance:
                if maxi < perc:
                    maxi = perc
                    res.insert(0, p)
                else:
                    res.append(p)
        return res
        