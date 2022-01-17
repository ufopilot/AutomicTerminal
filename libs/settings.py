import json
import os
import sys


class Settings():
	def __init__(self):
		super(Settings, self).__init__()
		if getattr(sys, 'frozen', False):
			# Rrunning in a |PyInstaller| bundle
			base_path = sys._MEIPASS
			extDataDir = os.getcwd()
			self.json_file = f"settings.json"
		else:
			# Running in a normal Python environment
			base_path = os.getcwd()
			extDataDir = os.getcwd()
			
			self.json_file = "settings.json"
		
		self.settings_path = os.path.join(extDataDir, self.json_file)
		self.items = {}
		self.deserialize()
	
	def serialize(self):
		# WRITE JSON
		with open(self.settings_path, "w", encoding='utf-8') as write:
			json.dump(self.items, write, indent=4)

	def deserialize(self):
		# READ JSON
		with open(self.settings_path, "r", encoding='utf-8') as reader:
			settings = json.loads(reader.read())
			self.items = settings
		
