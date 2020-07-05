#!/usr/bin/env python3
"""Classes that hold models for dynamic database swapping.
These models are controllers for adding, updating, and deleting from db.

entry -> check page info first -> check content -> format -> modelctrl ->
    form content -> make page -> print made page -> make content -> print made content
"""


class ModelCtrl:
    """Controls all model's create, update, and delete methods"""
    def __init__(self, dpage, dcontent, dtag):
        """Switch to another db by overwriting this class by initing
        it again.
        """
        self.page = dpage
        self.cont = dcontent
        self.tag = dtag

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
            img_path = data["img_path"],
            img_title = data["img_title"]
        )
        self.page.save()
        res["message"] = f"Created Page: {data['name']}"
        res["page"] = p
        return res

    def make_content(self, data:dict) -> str:
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
            content_img = data["content_img"],
            content_img_title = data["content_img_title"]
        )
        return f""

    def add_tag(self, name) -> str:
        pass
