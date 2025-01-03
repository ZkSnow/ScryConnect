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

TAB_WIDTH = 570
class Client(QMainWindow):
    """
    Represents the main application window containing all the tabs.

    This class initializes the main window for the application, setting its 
    properties, including size, title, and icon, and manages the user data.

    Parameters
    ----------
    - userdata (`dict`): A dictionary containing the user data, which is used to 
    initialize and manage application state.
    """
    def __init__(self, userdata: dict):
        super().__init__()
        self.userdata = userdata
        self.setMinimumWidth(TAB_WIDTH)
        self.resize(TAB_WIDTH, 700)
        self.non_concurrent_buttons = []
        self.setWindowIcon(QIcon(join(":", "icon.ico")))
        
        self.setWindowTitle("Scrcpy Client")
        self.start_ui()
     
    def charge_theme(self, charge_theme_button: QPushButton) -> None:
        """
        Toggles the application theme between light and dark modes.

        This function changes the application's theme based on the current theme 
        state stored in the user data. It updates the theme's appearance, changes 
        the button text to reflect the current theme, and saves the updated theme 
        state to the configuration file.

        Parameters
        ----------
        - charge_theme_button (`QPushButton`): The button used to toggle the theme.
        Its text will be updated to indicate the active theme.

        Notes
        -----
        - The dark theme is represented by a moon emoji ("\U0001f319") and the light 
        theme by a sun emoji ("\U00002600") on the button text.
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
        Saves the scrcpy version to the configuration file on Linux systems.

        This function initializes a thread to retrieve the scrcpy version and 
        save it to the configuration file. It is specifically designed for use 
        on Linux systems.
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
        """
        Initializes and configures the user interface (UI) for the main application window.

        This function sets up the main window's UI, including tabs, themes, and 
        interactive elements such as buttons. It also checks the operating system 
        and triggers additional setup for Linux users.

        UI Components
        -------------
        - `ConnectTab`: Manages all of Scrcpy's connection features. (e.g. connecting to Scrcpy via usb debug or wifi debug)
        - `StartTab`: Manages all Scrcpy and UI initialization functionalities. (e.g. starting Scrcpy with specific arguments) 
        - `ConfigTab`: Manages all Scrcpy settings or variants (e.g. by configuring the directory where Scrcpy is located) 
        """
        if system() == "Linux":
            self.save_scrcpy_version_if_linux()
        
        self.setMinimumWidth(TAB_WIDTH)
        self.tabs = QTabWidget()
        
        # Create all the tabs
        ConnectTab(self.userdata, self.non_concurrent_buttons, self.tabs)
        StartTab(self.userdata, self.non_concurrent_buttons, self, self.tabs)
        ConfigTab(self.userdata, self.non_concurrent_buttons, self, self.tabs)
        self.setCentralWidget(self.tabs)
        
        theme_icon = "\U0001f319" if self.userdata["Theme_Active"] == 0 else "\U00002600"
        self.setStyleSheet(black_theme if self.userdata["Theme_Active"] == 0 else white_theme)
        
        charge_theme_button = Create.Button(theme_icon, (33, 33), "ThemeButton")
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
    
        
    

    
    

    


