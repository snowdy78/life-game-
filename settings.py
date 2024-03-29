from tkinter import *
import os
import json
from colors import *
from math import floor

root = Tk()
# получение системного разрешение
WIN_WIDTH = root.winfo_screenwidth()
WIN_HEIGHT = root.winfo_screenheight()
JSON_FILE_NAME = "settings.json"
jsonfile_is_created = False
path = os.getcwd()  # текущая дериктория

# проверка создан ли уже файл settings.json
for file in os.listdir(path):
    if file == JSON_FILE_NAME:
        jsonfile_is_created = True

# если файл не создан, то он создается и ему
# устанавливаются настройки поумолчанию
if not jsonfile_is_created:
    jsstr = json.dumps({
        'Window-size': (WIN_WIDTH, WIN_HEIGHT),
        'When-cells-will-alive': [3],
        'When-cells-still-live': [2, 3],
        'cell-count': [48, 27]
    })
    with open(JSON_FILE_NAME, 'w') as file:
        file.write(jsstr)
# после выгрузка текста из файла
string = str()
with open(JSON_FILE_NAME, 'r') as file:
    for line in file:
        string += line
# загрузка json...
json_settings = json.loads(string)
# обновление содержимого WIN_WIDTH, WIN_HEIGHT
WIN_WIDTH = json_settings['Window-size'][0]
WIN_HEIGHT = json_settings['Window-size'][1]

