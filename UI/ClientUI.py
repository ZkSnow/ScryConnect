from os.path import join
from platform import system
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, 
                             QGridLayout, QPushButton)

from Theme.icon_scrcpy import * 
from PyQt5.QtGui import QIcon
from Script.Utilities import Create_Elements as Create
from Theme.Style_UI import black_theme, white_theme
from Script.Utilities.Utils import connect_signal, update_data_file
from UI.Tabs.ConnectTabUI import ConnectTab
from UI.Tabs.StartTabUI import StartTab
from UI.Tabs.ConfigTabUI import ConfigTab
from Script.Thread_Config_Tab import ConfigTAB_Thread

TAB_WIDTH = 555
TAB_HEIGHT = 700 #736

class Client(QMainWindow):
    """
    This class represents the `main window` and contains all the `tabs`.
    
    Parameters
    ----------
    - userdata (`dict`): A dictionary containing the user data.
    """
    def __init__(self, userdata: dict):
        super().__init__()
        self.userdata = userdata
        self.setMinimumSize(TAB_WIDTH, TAB_HEIGHT)
        self.non_concurrent_buttons = []
        self.setWindowIcon(QIcon(join(":", "icon.ico")))
        
        self.setWindowTitle("Scrcpy Client")
        self.start_ui()
     
    def charge_theme(self, charge_theme_button: QPushButton) -> None:
        """
        This function changes the theme of the application.
        
        Parameters
        ----------
        - charge_theme_button (`QPushButton`): The button that was clicked to change the theme.
        
        """
        if self.userdata["Theme_Active"]:
            charge_theme_button.setText("\U0001f319")
            self.userdata["Theme_Active"] = 0
            self.setStyleSheet(black_theme)
        else:
            charge_theme_button.setText("\U00002600")
            self.userdata["Theme_Active"] = 1
            self.setStyleSheet(white_theme)
        
        update_data_file(
            self.userdata["Theme_Active"],
            ["Theme_Active"],
        )
    
    def save_scrcpy_version_if_linux(self):
        """
        This function saves the scrcpy version in the config file if the user is on Linux.
        """
        self.terminal = ConfigTAB_Thread(
            "get_scrcpy_version_and_save",
            r"./",
            None,
            self.userdata["Versions"],
            self,
            
        )
        self.terminal.start()
    
    def start_ui(self):
        if system() == "Linux":
            self.save_scrcpy_version_if_linux()
            
        self.tabs = QTabWidget()
        self.tabs.setMinimumSize(TAB_WIDTH, TAB_HEIGHT)
        
        # Create all the tabs
        ConnectTab(self.userdata, self.non_concurrent_buttons, self.tabs)
        StartTab(self.userdata, self.non_concurrent_buttons, self, self.tabs)
        ConfigTab(self.userdata, self.non_concurrent_buttons, self, self.tabs)
        self.setCentralWidget(self.tabs)
        
        theme_icon = "\U0001f319" if self.userdata["Theme_Active"] == 0 else "\U00002600"
        self.setStyleSheet(black_theme if self.userdata["Theme_Active"] == 0 else white_theme)
        
        charge_theme_button = Create.Button(theme_icon, self, (33, 33), "ThemeButton")
        corner_container = QWidget()
        layout = QGridLayout(corner_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(charge_theme_button)
        self.tabs.setCornerWidget(corner_container)
       
        connect_signal(
            charge_theme_button,
            "clicked",
            self.charge_theme,
            charge_theme_button,
        )
        
        self.show()
    
        
    

    
    

    


