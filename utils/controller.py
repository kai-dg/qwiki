#!/usr/bin/env python3
"""Classes that hold models for dynamic database swapping.
These models are controllers for adding, updating, and deleting from db.
"""


class ModelCtrl:
    """Controls all model's create, update, and delete methods"""
    def __init__(self, dpage, dcontent, dtag, ddinfo):
        """Switch to another db by overwriting this class by initing
        it again.
        """
        self.page = dpage
        self.cont = dcontent
        self.tag = dtag
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

    def add_content(self, data:dict) -> str:
        """Args:
            data: keys are page, title, idx, content, content_img,
                  content_img_title
        Returns:
            str: message for display
        """
        res = self.cont.create(
            page = data["page"],
            title = data["title"],
            idx = data["idx"],
            content = data["content"],
            content_img = "",
            content_img_title = ""
        )
        return f"Added {data['page'].name} Content Header: {data['title']}"

    def set_tag(self, new:str) -> str:
        """`new` should be just the tag without commas."""
        q = self.d_info.select()[0] # Only 1 column should exist
        res = f"{q.set_tags},{new}"
        save = (self.d_info.update({self.d_info.set_tags:res}).where(self.d_info.id==1))
        return f"Made new tag {new}"
