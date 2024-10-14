from os.path import join, exists
from functools import partial
from platform import system
import webbrowser

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QComboBox, QFileDialog, QWidget

from UI.DeviceSelection import DeviceSelectionUI
from Script.Thread_Config_Tab import ConfigTAB_Thread
from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Static_Datas import USERDATA, PATH_DATA_DIR
from Script.Utilities.Utils import (
    toggle_button_state,
    verify_scrcpy_path, 
    update_data_file,
    open_or_save_data_json
)

running_on_windows = system() == "Windows"
class ConfigTAB():
    """This class contains all the functions of the `ConfigTAB`."""
    charge_resolution = pyqtSignal()
     
    def __init__(self):
        self.terminal = None
    
    def new_version(self, line_edit: QLineEdit) -> None:
        """
        This function allows the user to choose the `scrcpy folder`.
        
        Parameters
        ----------
        - line_edit (`QLineEdit`): The line edit where the scrcpy address will be placed.
        """
        if running_on_windows:
            Directory = QFileDialog.getExistingDirectory(None, "Select Scrcpy Folder")
            line_edit.setText(Directory)
        else:
            create_alert(
                "Unsupported OS",
                "Sorry, it's functional only on Windows",
            )
    
    def save_scrcpy_version(self, line_edit: QLineEdit, combo_box_target: QComboBox, data: dict) -> None:
        """
        This function allows the user to save the scrcpy version in the config file.
        
        Parameters
        ----------
        - line_edit (`QLineEdit`): The line edit with the address of the scrcpy.
        - combo_box_target (`QComboBox`): The combo box where the name will be added.
        - data (`dict`): The data dictionary.      
        """
        if running_on_windows:
            path = line_edit.text().rstrip().lstrip()
            if not isinstance(path, str):
                raise TypeError("path must be a string")
            
            if exists(path):
                if verify_scrcpy_path(path):
                    version_name, confirm_name = create_alert(
                        "Choose a Name",
                        "Name ↓", 
                        "input",
                    )
                    if confirm_name:
                        version_name = version_name.title().rstrip().lstrip()
                        if version_name and version_name not in data["Versions"]["Saved_Versions"].keys():
                            combo_box_target.addItem(version_name)
                            combo_box_target.setCurrentIndex(combo_box_target.count()-1)
                            self.terminal = ConfigTAB_Thread(
                                "get_scrcpy_version_and_save",
                                path,
                                version_name,
                                data["Versions"],
                            )
                            self.terminal.start()
                        else:
                            create_alert(
                                "Invalid Name", 
                                f"The name >> {version_name} << is invalid or already exists",
                            )
                else:
                    create_alert(
                        "Scrcpy not found",
                        ("Verify that the directory address is correct\n" 
                        "and that SCRCPY and ADB are properly installed"),
                    )
            else:
                create_alert(
                    "Directory Invalid",
                    ("The given directory is not valid or does not exist\n"
                    "enter a valid directory and try again "),
                )
        else:
            create_alert(
                "Unsupported OS",
                "Sorry, it's functional only on Windows",
            )
            
    def delete_scrcpy_version(self, combo_box: QComboBox, data: dict) -> None:
        """
        This function is used to delete a `scrcpy version`.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): the combo box with the name of the version.
        - data (`dict`): The data dictionary.
        """
        if running_on_windows:
            if (old_version := combo_box.currentText()) in data["Saved_Versions"].keys():
                if create_alert(
                    "Delete Version",
                    f"You are about to delete '{old_version}', do you want to continue?",
                    "confirm",
                ):
                    combo_box.removeItem(combo_box.findText(old_version))
                    del data["Saved_Versions"][old_version]
                    if current_version := combo_box.currentText():
                        new_value = data["Saved_Versions"][current_version]
                        data["Selected_Version"] = new_value
                    else:
                        new_value = {"Path": "", "Version": ""}
                        data["Selected_Version"] = new_value
                        
                    update_data_file(
                        new_value,
                        ["Versions", "Selected_Version"],
                    )
                    update_data_file(
                        None,
                        ["Versions", "Saved_Versions", old_version],
                        delete_value=True,
                    )
            else:
                create_alert(
                    "None Selected", 
                    "No version has been selected",
                )
        else:
            create_alert(
                "Unsupported OS",
                "Sorry, it's functional only on Windows",
            )
    
    def charge_device_resolution(self, data: str, combo_box: QComboBox) -> None:
        """
        This function is used to charge the resolution of the device.
        
        Parameters
        ----------
        - data (`dict`): A dictionary containing the user data.
        - combo_box (`QComboBox`): The resolution combo box widget.
        """
        if combo_box != None:
            if resolution := combo_box.currentText().rstrip().lstrip():
                resolution = data["Resolutions"]["Saved_Resolution"][resolution]
                resolution = f"{resolution[0]}x{resolution[1]}"
        else:
            resolution = None
            
        if path := data["Versions"]["Selected_Version"]["Path"] or not running_on_windows:	
            if verify_scrcpy_path(path):
                if resolution != "":
                    self.terminal = ConfigTAB_Thread(
                        "get_devices",
                        path,
                        DeviceSelectionUI,
                        resolution,
                    )
                    self.terminal.start()
                    self.terminal.get_device_output.connect(
                        partial(
                            self.terminal.start_resolution_ui,
                        )
                    )
                else:
                    create_alert(
                        "Nothing Selected",
                        "No resolution has been selected",
                    )
            else:
                create_alert(
                    "Error in finding scrcpy",
                    ("the scrcpy/adb was not found in the version folder\n" 
                    "check the folder and try again"),
                )
        else:
            create_alert(
                "Nothing Selected",
                ("No version has been selected -> "
                "<a href='https://github.com/Genymobile/scrcpy/releases'>Scrcpy Releases</a> or "
                "<a href='https://github.com/Genymobile/scrcpy/blob/master/doc/linux.md#latest-version'>Scrcpy for Linux</a>"),
            )
    
    def new_custom_resolution(self, combo_box_target: QComboBox, data: dict) -> None:
        """
        This function allows the user to add `custom resolutions` to the config file.
        
        Parameters
        ----------
        combo_box_target (`QComboBox`): The combo box where the new resolution will be added.
        data (`dict`): The data dictionary.
        """
        width, confirm_width = create_alert(
                "Width", 
                "Enter a Width",
                "input",
                "^[0-9]*$"
        )
        if confirm_width:
            height, confirm_height = create_alert(
                    "Height",
                    "Enter a Height",
                    "input",
                    "^[0-9]*$"
            )
            if confirm_height:
                    res_size = [int(width), int(height)] if all([width, height]) else None
                    if res_size and all(w_h > 0 and w_h < 10**8 for w_h in res_size):
                        if (resolution_name := f"{res_size[0]}x{res_size[1]}") not in data.keys():
                            combo_box_target.addItem(resolution_name)
                            combo_box_target.setCurrentIndex(combo_box_target.count()-1)
                            data[resolution_name] = res_size
                            
                            update_data_file(
                                res_size,
                                ["Resolutions", "Saved_Resolution", resolution_name],
                            )
                        else:
                            create_alert(
                                "Existing Resolution", 
                                f"The name '{resolution_name}' already exists",
                            )
                    else:
                        create_alert(
                            "invalid values", 
                            ("Width and Height must be a positive number and\n"
                            "have less than 8 digits"),
                        )
                                 
    def delete_custom_resolution(self, combo_box: QComboBox, saved_resolution: dict) -> None:
        """
        This function deletes a custom resolution from the `combo box`.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box to delete the resolution from.
        - saved_resolution (`dict`): The saved resolution dictionary.
        """
        if (current_text := combo_box.currentText()) in saved_resolution:
            if create_alert(
                    "Delete Resolution",
                    (f"You are about to delete '{current_text}'\n"
                    "do you want to continue?"),
                    "confirm",
            ):
                combo_box.removeItem(combo_box.findText(current_text))
                del saved_resolution[current_text]
                update_data_file(
                    None,
                    ["Resolutions", "Saved_Resolution", current_text],
                    delete_value=True
                )
        
        else:
            create_alert(
                "None Selected", 
                "No resolution has been selected",
            )
  
    def save_file_path(self, line_edit: QLineEdit, combo_box_target: QComboBox, data: dict) -> None:
        """
        This function saves the file path to the `config file`.
        
        Parameters
        ----------
        - line_edit (`QLineEdit`): The line edit widget.
        - combo_box_target (`QComboBox`): The combo box to add the path to.
        - data (`dict`): The data dictionary.
        """
        if exists(line_edit.text()):
            path_name, confirm_name = create_alert(
                "Choose a Name",
                "Name ↓",
                "input",
            )
            path_name = path_name.title().rstrip().lstrip()
            if confirm_name:
                if path_name and path_name not in data["Saved_Path_Files"].keys():
                    combo_box_target.addItem(path_name)
                    combo_box_target.setCurrentIndex(combo_box_target.count()-1)
                    
                    path = line_edit.text()
                    data["Saved_Path_Files"][path_name] = path
                    data["Path_selected"] = path
                    update_data_file(
                        path,
                        ["File_Path_Config", "Saved_Path_Files", path_name],
                    )
                    update_data_file(
                        path,
                        ["File_Path_Config", "Path_selected"],
                    )
                else:
                    create_alert(
                        "Name Error",
                        f"The name >> {path_name} << is invalid or already exists",
                    )   
        else:
            create_alert(
                "Directory Invalid",
                ("The given directory is not valid or does not exist\n"
                "enter a valid directory and try again"),
            )
        
    def delete_file_path(self, combo_box: QComboBox, data: dict) -> None:
        """
        This function is used to delete a `file path`.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box to delete.
        - data (`dict`): The data dictionary.
        """
        if (old_path := combo_box.currentText()) in data["Saved_Path_Files"].keys():
            if create_alert(
                "Delete Path",
                (f"You are about to delete '{old_path}'\n" 
                "do you want to continue?"),
                "confirm",
            ):
                combo_box.removeItem(combo_box.findText(old_path))
                del data["Saved_Path_Files"][old_path]
                if current_path:= combo_box.currentText():
                    new_value = data["Saved_Path_Files"][current_path] 
                    data["Path_selected"] = new_value
                else:
                    new_value = None
                    data["Path_selected"] = new_value
                
                update_data_file(
                    None,
                    ["File_Path_Config", "Saved_Path_Files", old_path],
                    delete_value=True
                )
                update_data_file(
                    new_value,
                    ["File_Path_Config", "Path_selected"],
                )
                
        else:
            create_alert(
                "None Selected", 
                "No path has been selected",
            )
  
    def open_github_page(self):
        """
        This function opens my github page in a web browser :D
        """
        webbrowser.open(r"https://github.com/ZkSnow")
    
    def reset_data(self, client: QWidget) -> None:
        """
        This function resets the `data` file.
        
        Parameters
        ----------
        - client (`QWidget`): The client widget to close.        
        """
        if create_alert(
            "ARE YOU SURE?", 
            ("You are about to erase RESET ALL DATA\n"
            "do you want to continue?"), 
            "confirm",
        ):  
            open_or_save_data_json(join(PATH_DATA_DIR, "UserData.json"), "w", USERDATA)
            create_alert(
                "Closing",
                "The client will CLOSE to APPLY the CHANGES",
            )
            client.close()
            
    def reset_adb_server(self, buttons: list, data: dict) -> None:
        """
        This function resets the `adb server`.
        
        Parameters
        ----------
        - buttons (`list`): A list of non-concurrent buttons.
        - data (`dict`): A dictionary containing the user data.
        
        """
        
        if path := data["Versions"]["Selected_Version"]["Path"] or not running_on_windows:
            if verify_scrcpy_path(path):
                if create_alert(
                    "Warning",
                    ("You are about to reset the ADB SERVER\n"
                    "are you sure you want to continue?"),
                    "confirm",
                ):
                    original_text = toggle_button_state(
                        buttons,
                        False
                    )
                    self.terminal = ConfigTAB_Thread(
                        "reset_adb_server",
                        path,
                        buttons,
                        original_text,
                    )
                    self.terminal.start()
                    self.terminal.reset_server_output.connect(
                        self.terminal.check_emit_reset,   
                    )
                    
            else:
                create_alert(
                    "Scrcpy not found",
                    ("Verify that the directory address is correct\n" 
                    "and that SCRCPY and ADB are properly installed"),
                )
        else:
            create_alert(
                "Nothing Selected",
                ("No version has been selected -> "
                "<a href='https://github.com/Genymobile/scrcpy/releases'>Scrcpy Releases</a> or "
                "<a href='https://github.com/Genymobile/scrcpy/blob/master/doc/linux.md#latest-version'>Scrcpy for Linux</a>"),
            )   
    
    def path_to_save_file(self, line_edit_target: QLineEdit) -> None:
        """
        This function lets you choose the directory in which to save the video files.
        
        Parameters
        ----------
        - line_edit_target (`QLineEdit`): The line edit widget to get the text from.
        """
        Directory = QFileDialog.getExistingDirectory(None, "Select Save Directory")
        line_edit_target.setText(Directory)
            
    def path_mode(self, index: int, data: dict) -> None:
        """
        This function updates the `Path_Mode_Radio` in `File_Path_Config`.
        
        Parameters
        ----------
        - index (`int`): The index of the radio button.
        - data (`dict`): The data dictionary.
        """
        path_mode = [True, False] if index == 0 else [False, True]
        data["Path_Mode_Radio"] = path_mode
        update_data_file(
            path_mode,
            ["File_Path_Config", "Path_Mode_Radio"],
        )
    
    def version_selected(self, combo_box: QComboBox, line_edit_target: QLineEdit, data: dict) -> None:
        """
        This function updates the `Saved_Versions` in `Versions`.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget to get the index from.
        - line_edit_target (`QLineEdit`): The line edit widget to get the text from.
        - data (`dict`): The data dictionary.
        """
        if (current_version_name := combo_box.currentText()) in data["Saved_Versions"].keys():
            current_version = data["Saved_Versions"][current_version_name]
            line_edit_target.setText(current_version["Path"])
            data["Selected_Version"] = current_version
            
            update_data_file(
                current_version,
                ["Versions", "Selected_Version"],
            )
            
            update_data_file(
                current_version,
                ["Versions", "Saved_Versions", current_version_name],
            )
              
    def path_selected(self, combo_box: QComboBox, line_edit_target: QLineEdit, data: dict) -> None:
        """
        This function updates the `Path_selected` in `File_Path_Config`.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget to get the index from.
        - line_edit_target (`QLineEdit`): The line edit widget to get the text from.
        - data (`dict`): The data dictionary.
        """
        if (current_path := combo_box.currentText()) in data["Saved_Path_Files"].keys():
            current_path = data["Saved_Path_Files"][current_path]
            line_edit_target.setText(current_path)
            update_data_file(
                current_path,
                ["File_Path_Config", "Path_selected"],
            )
        
    def last_index_selected(self, combo_box_num: int, comobo_box: QComboBox) -> None:
        """
        This function updates the `index_combox` in `Last_Session_Config`.
        
        Parameters
        ----------
        - combo_box_num (`int`): The index of the `index_combox` in `Last_Session_Config`.
        - comobo_box (`QComboBox`): The combo box widget to get the index from.
        """
        update_data_file(
            comobo_box.currentIndex(),
            ["Last_Session_Config", "ConfigTAB", "Index_Combox", combo_box_num],
        )

        
