from tkinter import *
import os
import json

root = Tk()
WIN_WIDTH = root.winfo_screenwidth()
WIN_HEIGHT = root.winfo_screenheight()
JSON_FILE_NAME = "settings.json"
jsonfile_is_created = False
path = os.getcwd()

for file in os.listdir(path):
    if file == JSON_FILE_NAME:
        jsonfile_is_created = True

if not jsonfile_is_created:
    jsstr = json.dumps({
        'Window-size': (WIN_WIDTH, WIN_HEIGHT),
        'When-cells-will-alive': [3],
        'When-cells-still-live': [2, 3],
        'cell-count': [48, 27]
    })
    with open("settings.json", 'w') as file:
        file.write(jsstr)

string = str()
with open("settings.json", 'r') as file:
    for line in file:
        string += line
json_settings = json.loads(string)
WIN_WIDTH = json_settings['Window-size'][0]
WIN_HEIGHT = json_settings['Window-size'][1]

