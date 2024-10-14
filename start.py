from sys import argv
from os import mkdir
from os.path import isdir, join

from PyQt5.QtWidgets import QApplication
from Script.Utilities.Utils import open_or_save_data_json
from Script.Utilities.Static_Datas import USERDATA
from UI.ClientUI import Client 

if not isdir(join(".", "Data")):
    mkdir("Data")    

userdata_path = join("Data", "UserData.json")
try:
    userdata = open_or_save_data_json(userdata_path, "r")
except FileNotFoundError:
    open_or_save_data_json(userdata_path, "w", USERDATA)
    userdata = open_or_save_data_json(userdata_path, "r")

app = QApplication(argv)
program = Client(userdata)
app.exec_()
