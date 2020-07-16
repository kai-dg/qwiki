#!/usr/bin/env python3
import tkinter as tk
import utils.globals as g
import ui.settings as s
import ui.tk_helper as tkh
from PIL import Image
from PIL import ImageTk


class ImageWindow:
	def __init__(self, image_path=None):
		"""TODO Create if case: if none, display image error message in new window"""
		self.height = 480
		self.width = 0
		self.image_window = tk.Toplevel(g.ROOT, height=s.IW_HEIGHT, width=s.IW_WIDTH)
		self.image_window.minsize(s.IW_WIDTH, s.IW_HEIGHT)
		self.image_window.focus()
		self.image = Image.open(image_path)
		self.initial_size()
		self.background = ImageTk.PhotoImage(self.image)
		self.image_bg = tk.Label(self.image_window, image=self.background)
		self.image_bg.pack(fill="both", expand=True)
		self.image_window.bind("<Escape>", lambda event: self.image_window.destroy())
		#self.image_bg.bind("<Configure>", self.resizing)

	def initial_size(self):
		wpercent = (self.height / float(self.image.size[1]))
		self.width = int(self.image.size[0] * float(wpercent))
		self.image = self.image.resize((self.width, self.height), Image.ANTIALIAS)
	"""
	def resizing(self, event):
		if self.height != event.height:
			self.height = event.height
			wpercent = (self.height / float(self.image.size[1]))
			self.width = int(self.image.size[0] * float(wpercent))
			self.image = self.image.resize((self.width, self.height), Image.ANTIALIAS)
			self.background = ImageTk.PhotoImage(self.image)
			self.image_bg.config(image=self.background)
	"""