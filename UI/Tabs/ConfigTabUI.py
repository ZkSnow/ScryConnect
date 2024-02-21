from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QSpacerItem, 
                             QComboBox, QTabWidget, QMainWindow)

from Script.ConfigTAB_Functions import ConfigTAB
from Script.Utilities import Create_Elements as Create
from Script.Utilities.Utils import connect_signal
from Script.Utilities.Auxiliary_Funcs import assemble_grid_layout, get_datas_for_ui

class ConfigTab(QWidget):
    """
    This class is used to create the `Config Tab` UI.
    
    Parameters
    ----------
    - userdata (`dict`): the user data.
    - nconc_btns (`list`): the list of the non-concurrent buttons.
    - client (`QMainWindow`): the main window of the application.
    - tabs (`QTabWidget`): the tab widget that contains all the tabs.
    """
    def __init__(self, userdata: dict, nconc_btns: list, client: QMainWindow, tabs: QTabWidget):
        super().__init__()
        self.userdata = userdata
        self.non_concurrent_buttons = nconc_btns
        self.client = client
        
        self.create_elements()
        self.assemble_elements()
        self.connect_functions_elements()
        tabs.addTab(self, "Config")
        
    def create_elements(self):
        """
        This function `creates` all the elements of the `Config Tab`.
        """
        selected_version, versions, resolution, path_mode, last_path_file,\
        directory_name, combox_index = get_datas_for_ui(self.userdata, "config")
        
        self.label_scrcpy_versions = Create.Label("Scrcpy Versions", self)
        self.label_custom_resolution = Create.Label("Custom Resolution", self)
        self.label_path_save_recording = Create.Label("Path To Save Recording", self)
        
        self.combox_versions = Create.Combox(versions, self, (451, 22), combox_index[0])
        self.combox_resolutions = Create.Combox(resolution, self, (451, 22), combox_index[1])
        self.combox_file_path = Create.Combox(directory_name, self, (451, 22), combox_index[2])
        
        self.text_path_scrcpy = Create.LineEdit("Path to Scrcpy...", self, (451, 20), selected_version)
        self.text_path_file = Create.LineEdit("Path to Save File...", self, (451, 20), last_path_file)
        
        self.button_version = Create.Button("Save Version", self, (221, 23))
        self.button_delete_version = Create.Button("Delete Version", self, (221, 23))
        self.button_new_version = Create.Button("New Version", self, (451, 23))
        self.button_new_resolution = Create.Button("New Resolution", self, (221, 23))
        self.button_delete_resolution = Create.Button("Delete Resolution", self, (221, 23))
        self.button_charge_resolution = Create.Button("Charge Resolution", self, (451, 23))
        self.button_native_resolution = Create.Button("Native Resolution", self, (451, 23))
        self.button_path_file = Create.Button("Save Path", self, (221, 23))
        self.button_delete_path_file = Create.Button("Delete Path", self, (221, 23))
        self.button_find_save_path = Create.Button("Find Path", self, (451, 23))
        self.button_reset_data = Create.Button("Reset Data", self, (75, 23), "Reset_Button")
        self.button_reset_server = Create.Button("Reset Server", self, (75, 23), "Reset_Button")
        self.button_github_button = Create.Button("\U0001F5A5", self, (20, 20), "Github_Button")
        self.button_github_button.setMaximumSize(20, 20)
        
        self.radio_custom = Create.RadioButton("Custom Path", self, (91, 16), path_mode[0])
        self.radio_default = Create.RadioButton("Default path", self, (91, 20), path_mode[1])
        
    def assemble_elements(self):
        """
        This function `assembles` all the elements into a `grid layout`.
        """
        upper_layout = assemble_grid_layout(
            "config_tab",
            "upper",
            self.label_scrcpy_versions,
            self.text_path_scrcpy,
            self.combox_versions,
            self.button_version,
            self.button_delete_version,
            self.button_new_version,
            self.label_custom_resolution,
            self.combox_resolutions,
            self.button_new_resolution,
            self.button_delete_resolution,
            self.button_charge_resolution,
            self.button_native_resolution,
            self.label_path_save_recording,
            self.text_path_file,
            self.combox_file_path,
            self.button_path_file,
            self.button_delete_path_file,
            self.button_find_save_path,
        )
        lower_layout = assemble_grid_layout(
            "config_tab",
            "lower",
            self.radio_custom,
            self.radio_default,
            self.button_github_button,
            self.button_reset_data,
            self.button_reset_server,
        )
        
        upper_layout.addItem(QSpacerItem(0, 20), 5, 0)
        upper_layout.addItem(QSpacerItem(0, 20), 12, 0)
        lower_layout.addItem(QSpacerItem(0, 70), 2, 0)
        lower_layout.setSpacing(1)
        
        upper_content = QWidget()
        lower_content = QWidget()
        main_layout = QGridLayout()
        main_layout.addWidget(upper_content, 0, 0, Qt.AlignTop)
        main_layout.addWidget(lower_content, 1, 0)
        
        upper_content.setLayout(upper_layout)
        lower_content.setLayout(lower_layout)
        self.setLayout(main_layout)
        
    def connect_functions_elements(self):
        """
        This function `connects` the functions to the `elements`.
        """
        self.non_concurrent_buttons.extend(
            [
            self.button_charge_resolution,
            self.button_native_resolution,
            ]
        )
        config_tab_instance = ConfigTAB()
        for combo_box_num, combo_box in enumerate(self.findChildren(QComboBox)):
            connect_signal(
                combo_box,
                "currentIndexChanged",
                config_tab_instance.last_index_selected,
                combo_box_num,
                combo_box,
            )
        
        for index, radio in enumerate([self.radio_custom, self.radio_default]):
            connect_signal(
                radio,
                "clicked",
                config_tab_instance.path_mode,
                index,
                self.userdata["File_Path_Config"],
            )
        
        connect_signal(
            self.combox_versions,
            "activated",
            config_tab_instance.version_selected,
            self.combox_versions,
            self.text_path_scrcpy,
            self.userdata["Versions"],
        )

        connect_signal(
            self.combox_file_path,
            "activated",
            config_tab_instance.path_selected,
            self.combox_file_path,
            self.text_path_file,
            self.userdata["File_Path_Config"],
        )

        connect_signal(
            self.button_new_version,
            "clicked",
            config_tab_instance.new_version, 
            self.text_path_scrcpy,
        )

        connect_signal(
            self.button_version,
            "clicked",
            config_tab_instance.save_scrcpy_version, 
            self.text_path_scrcpy, 
            self.combox_versions, 
            self.userdata,
        )

        connect_signal(
            self.button_delete_version,
            "clicked",
            config_tab_instance.delete_scrcpy_version, 
            self.combox_versions, 
            self.userdata["Versions"],
        )

        connect_signal(
            self.button_new_resolution,
            "clicked",
            config_tab_instance.new_custom_resolution, 
            self.combox_resolutions,
            self.userdata["Resolutions"]["Saved_Resolution"],
        )

        connect_signal(
            self.button_delete_resolution,
            "clicked",
            config_tab_instance.delete_custom_resolution, 
            self.combox_resolutions,
            self.userdata["Resolutions"]["Saved_Resolution"],
        )
        
        connect_signal(
            self.button_charge_resolution,
            "clicked",
            config_tab_instance.charge_device_resolution,
            self.userdata,
            self.combox_resolutions,
        )
        
        connect_signal(
            self.button_native_resolution,
            "clicked",
            config_tab_instance.charge_device_resolution,
            self.userdata,
            None,
        )
        
        connect_signal(
            self.button_path_file,
            "clicked",
            config_tab_instance.save_file_path,
            self.text_path_file,
            self.combox_file_path,
            self.userdata["File_Path_Config"]
        )
        
        connect_signal(
            self.button_delete_path_file,
            "clicked",
            config_tab_instance.delete_file_path,
            self.combox_file_path,
            self.userdata["File_Path_Config"]
        )
        
        connect_signal(
            self.button_find_save_path,
            "clicked",
            config_tab_instance.path_to_save_file, 
            self.text_path_file,
        )
        
        connect_signal(
            self.button_github_button,
            "clicked",
            config_tab_instance.open_github_page,
        )
        
        connect_signal(
            self.button_reset_data,
            "clicked",
            config_tab_instance.reset_data, 
            self.client,
        )
        
        connect_signal(
            self.button_reset_server,
            "clicked",
            config_tab_instance.reset_adb_server, 
            self.non_concurrent_buttons,
            self.userdata,
        )