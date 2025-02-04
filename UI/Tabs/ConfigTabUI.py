from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, 
    QGridLayout, 
    QSpacerItem, 
    QComboBox, 
    QTabWidget, 
    QMainWindow,
    QScrollArea,
)

from Script.ConfigTAB_Functions import ConfigTAB
from Script.Utilities import Create_Elements as Create
from Script.Utilities.Utils import connect_signal
from Script.Utilities.Auxiliary_Funcs import assemble_grid_layout, get_datas_for_ui

class ConfigTab(QScrollArea):
    """
    Represents the configuration tab UI in the application.

    This class is responsible for creating and managing the user interface (UI) elements 
    within the "Config" tab. It provides functionality for setting up the configuration data, 
    handling user inputs, and interacting with other components of the application such as 
    buttons and the main window. The `ConfigTab` is added to a `QTabWidget` to make it a part 
    of the main application's tab-based interface.

    Parameters
    ----------
    - userdata (`dict`): The dictionary containing user-specific data, which is used 
    to populate the configuration fields.
    - nconc_btns (`list`): A list of buttons that are non-concurrent, i.e., buttons that 
    should not be pressed simultaneously, which are toggled during various actions.
    - client (`QMainWindow`): The main window of the application, which serves as the container 
    for all tabs, including this configuration tab.
    - tabs (`QTabWidget`): The `QTabWidget` that holds all the tabs in the application, to which 
    this configuration tab will be added.
    """
    def __init__(self, userdata: dict, nconc_btns: list, client: QMainWindow, tabs: QTabWidget):
        super().__init__()
        self.userdata = userdata
        self.non_concurrent_buttons = nconc_btns
        self.client = client
        
        self.setWidgetResizable(True)
        self.content = QWidget()
        self.setWidget(self.content)
        
        self.create_elements()
        self.assemble_elements()
        self.connect_functions_elements()
        tabs.addTab(self, "Config")
        
    def create_elements(self):
        """
        Creates and initializes all the UI elements for the `Config Tab`.

        This method is responsible for setting up the widgets and controls that will be displayed 
        in the "Config" tab. These include labels, combo boxes, line edits, and buttons, which 
        allow the user to configure various aspects of the application. The method also retrieves 
        necessary data for populating these elements from the `userdata` dictionary.
        """
        selected_version, versions, resolution, path_mode, last_path_file,\
        directory_name, combox_index = get_datas_for_ui(self.userdata, "config")
        
        self.label_scrcpy_versions = Create.Label("Scrcpy Versions")
        self.label_custom_resolution = Create.Label("Custom Resolution")
        self.label_path_save_recording = Create.Label("Path To Save Recording")
        
        self.combox_versions = Create.Combox(versions, (451, 22), combox_index[0])
        self.combox_resolutions = Create.Combox(resolution, (451, 22), combox_index[1])
        self.combox_file_path = Create.Combox(directory_name, (451, 22), combox_index[2])
        
        self.text_path_scrcpy = Create.LineEdit("Path to Scrcpy...", (451, 20), selected_version)
        self.text_path_file = Create.LineEdit("Path to Save File...", (451, 20), last_path_file)
        
        self.button_version = Create.Button("Save Version", (221, 23))
        self.button_delete_version = Create.Button("Delete Version", (221, 23))
        self.button_new_version = Create.Button("New Version", (451, 23))
        self.button_new_resolution = Create.Button("New Resolution", (221, 23))
        self.button_delete_resolution = Create.Button("Delete Resolution", (221, 23))
        self.button_charge_resolution = Create.Button("Charge Resolution", (451, 23))
        self.button_native_resolution = Create.Button("Native Resolution", (451, 23))
        self.button_path_file = Create.Button("Save Path", (221, 23))
        self.button_delete_path_file = Create.Button("Delete Path", (221, 23))
        self.button_find_save_path = Create.Button("Find Path", (451, 23))
        self.button_reset_data = Create.Button("Reset Data", (75, 23), "Reset_Button")
        self.button_reset_server = Create.Button("Reset Server", (75, 23), "Reset_Button")
        self.button_github_button = Create.Button("\U0001F5A5", (20, 20), "Github_Button")
        self.button_github_button.setMaximumSize(20, 20)
        
        self.radio_custom = Create.RadioButton("Custom Path", (91, 16), path_mode[0])
        self.radio_default = Create.RadioButton("Default path", (91, 20), path_mode[1])
        
    def assemble_elements(self):
        """
        Assembles all the UI elements into a grid layout for the `Config Tab`.

        This method arranges and organizes the previously created UI elements into a layout 
        structure. It splits the UI into an upper and lower section, each containing related 
        widgets. The elements are then added to the layout using grid-based positioning. 
        Additionally, spacers are inserted at specific positions to improve the overall layout 
        structure.
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
        
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.content.setLayout(main_layout)
        
    def connect_functions_elements(self):
        """
        Connects the UI elements with their corresponding functions in the `ConfigTab`.

        This method establishes the necessary signal-slot connections for the UI elements in the 
        `ConfigTab` to ensure that user interactions trigger the appropriate actions. The method 
        connects various signals (such as `currentIndexChanged` and `clicked`) to the relevant 
        functions responsible for handling these events.

        The method also extends the `non_concurrent_buttons` list with specific buttons that should 
        be handled separately in the layout.

        Notes
        -----
        - This method relies on the `connect_signal` utility function to connect the UI elements' 
        signals to the appropriate functions.
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
