#!/usr/bin/env python3
"""Functions that deal with adding, deleting, and updating images"""
import utils.globals as g
import os


def create_base_folder():
    if not os.path.exists(g.BASE_IMG_FOLDER):
        os.makedirs(g.BASE_IMG_FOLDER)
        
def initial_base_folder():
    """Creates"""
    create_base_folder()
    default = os.path.join(g.BASE_IMG_FOLDER, g.DEFAULT_DB)
    os.makedirs(default)