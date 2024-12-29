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
        Opens a directory selection dialog and sets the scrcpy folder path in the specified QLineEdit.

        This function allows the user to select the `scrcpy` folder path through a directory selection dialog. 
        The chosen path is displayed in the provided `QLineEdit` widget. This feature is currently supported 
        only on Windows operating systems. On unsupported OS, an alert dialog is shown to notify the user.

        Parameters
        ----------
        - line_edit (`QLineEdit`): The QLineEdit widget where the selected `scrcpy` folder path will be displayed.
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
        Saves the scrcpy version in the configuration file and updates the target combo box.

        This function allows the user to save a scrcpy version by selecting its path, assigning it a 
        custom name, and storing it in the configuration data. If the path and version name are valid, 
        the name is added to the specified combo box and saved in the configuration file. This functionality 
        is currently supported only on Windows. For unsupported operating systems, an alert is displayed.

        Parameters
        ----------
        - line_edit (`QLineEdit`): The QLineEdit widget containing the scrcpy folder path.
        - combo_box_target (`QComboBox`): The QComboBox widget where the version name will be added if valid.
        - data (`dict`): A dictionary containing configuration data, including saved versions.

        Raises
        ------
        - `TypeError`: If the scrcpy path is not a string.

        Notes
        -----
        - This function checks if the scrcpy folder exists and verifies its contents to ensure both 
        `scrcpy` and `adb` are properly installed.
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
        Deletes a scrcpy version from the configuration file and updates the combo box.

        This function removes the currently selected scrcpy version from the configuration data and updates 
        the associated combo box. If a version is selected and the user confirms the deletion, it is removed 
        from both the combo box and the saved configuration. The selected version is updated accordingly, 
        or reset if no other versions remain. This functionality is only supported on Windows; unsupported 
        operating systems will prompt an alert.

        Parameters
        ----------
        - combo_box (`QComboBox`): The QComboBox widget containing the list of saved scrcpy versions.
        - data (`dict`): A dictionary containing configuration data, including saved and selected versions.
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
        Configures the device resolution and starts the resolution adjustment process.

        This function retrieves the selected resolution from a combo box and applies it to the selected 
        device through the ADB SHELL. It validates the scrcpy path and checks the resolution, initiating 
        the process if all conditions are met. If no resolution or scrcpy version is selected, the user 
        is notified via an alert dialog.

        Parameters
        ----------
        - data (`dict`): A dictionary containing user data, including saved resolutions and selected scrcpy version.
        - combo_box (`QComboBox`): The combo box widget from which the desired resolution is selected.
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
        Adds a custom resolution to the configuration file and updates the combo box.

        This function allows the user to define a custom resolution by providing width and height values. 
        The resolution is validated to ensure it consists of positive integers less than 8 digits. If valid 
        and not already existing in the configuration, it is added to the combo box and saved to the 
        configuration file.

        Parameters
        ----------
        - combo_box_target (`QComboBox`): The combo box widget where the new resolution will be displayed and selectable.
        - data (`dict`): A dictionary containing the configuration data, including saved resolutions.
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
        Deletes a custom resolution from the combo box and the saved resolutions dictionary.

        This function removes the currently selected resolution from a combo box and deletes it 
        from the saved resolutions in the configuration file. The user is prompted to confirm 
        the deletion before proceeding. If no resolution is selected or the resolution is not 
        found in the saved resolutions, the user is notified via an alert dialog.

        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget containing the list of resolutions, from which the selected resolution will be deleted.
        - saved_resolution (`dict`): A dictionary containing saved custom resolutions, where the key is the resolution name (e.g., `"1920x1080"`) 
        and the value is the resolution size as a list [x, y] (e.g., `[1920, 1080]`).
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
        Saves a file path to the configuration file and updates the combo box.

        This function allows the user to save a file path by specifying a custom name. The file path is 
        validated to ensure it exists, and if valid, it is saved in the configuration data and added to 
        the specified combo box for easy selection in the future.

        Parameters
        ----------
        - line_edit (`QLineEdit`): The QLineEdit widget containing the file path entered by the user.
        - combo_box_target (`QComboBox`): The QComboBox widget where the custom name for the file path will be displayed.
        - data (`dict`): A dictionary containing configuration data, including saved file paths and the currently 
        selected path.
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
        Deletes a file path from the combo box and the configuration file.

        This function removes the currently selected file path from a combo box and deletes it from 
        the configuration data. The user is prompted to confirm the deletion. If no file path is selected 
        or the selected path is not found in the configuration data, an alert is displayed.

        Parameters
        ----------
        - combo_box (`QComboBox`): The QComboBox widget containing the list of saved file paths, from which the selected path 
        will be removed.
        - data (`dict`): A dictionary containing configuration data, including saved file paths and the currently 
        selected path.
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
        --------
        """
        webbrowser.open(r"https://github.com/ZkSnow")
    
    def reset_data(self, client: QWidget) -> None:
        """
        Resets the configuration data by overwriting the data file and closes the client widget.

        This function erases all the current data in the configuration file, effectively resetting the 
        application state. It prompts the user for confirmation before performing the reset, and if 
        confirmed, it writes the default data to the file and closes the client widget to apply the changes.

        Parameters
        ----------
        - client (`QWidget`): The client widget (main window) that will be closed after the data is reset.

        Notes
        -----
        - The function opens and overwrites the `UserData.json` file with default data (`USERDATA`).
        - After resetting the data, the client widget is closed to apply the changes.
        - The reset is irreversible, so it is important that the user explicitly confirms the action.
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
        Resets the ADB server by initiating a reset process on the selected scrcpy version.

        This function performs a reset of the ADB server, It first verifies that the scrcpy path is valid, 
        prompts the user for confirmation, and then starts a thread to execute the reset. During this process, 
        the state of the specified buttons is toggled to indicate that the reset is in progress.

        Parameters
        ----------
        - buttons (`list`): A list of buttons that will be toggled (enabled/disabled) during the reset process to prevent 
        concurrent actions. The list contains non-concurrent buttons which will be disabled while the reset 
        is ongoing and restored to their original state afterward.
        - data (`dict`): A dictionary containing user data, including the path to the selected scrcpy version.
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
        Opens a dialog for the user to select a directory to save video files.

        This function prompts the user with a file dialog to choose a directory on their system where 
        video files should be saved. Once the user selects a directory, the path is set in the specified 
        line edit widget, which can then be used to store or reference the selected save path.

        Parameters
        ----------
        - line_edit_target (`QLineEdit`): The QLineEdit widget where the selected directory path will be displayed.
        """
        Directory = QFileDialog.getExistingDirectory(None, "Select Save Directory")
        line_edit_target.setText(Directory)
            
    def path_mode(self, index: int, data: dict) -> None:
        """
        Updates the `Path_Mode_Radio` setting in the `File_Path_Config` dictionary based on the selected index.

        This function modifies the `Path_Mode_Radio` value in the configuration data to reflect the selected 
        mode, which is determined by the radio button's index. The radio button can represent two modes, 
        where index `0` represents the first mode and index `1` represents the second. The function then 
        saves the updated configuration to the data file.

        Parameters
        ----------
        - index (`int`): 
            The index of the selected radio button, where:
            - `0` corresponds to (`True, False`).
            - `1` corresponds to (`False, True`).
        - data (`dict`): The data dictionary that contains the configuration settings.
        """
        path_mode = [True, False] if index == 0 else [False, True]
        data["Path_Mode_Radio"] = path_mode
        update_data_file(
            path_mode,
            ["File_Path_Config", "Path_Mode_Radio"],
        )
    
    def version_selected(self, combo_box: QComboBox, line_edit_target: QLineEdit, data: dict) -> None:
        """
        Updates the selected version in the `Saved_Versions` and `Selected_Version` sections of the configuration.

        This function retrieves the currently selected version from the combo box, updates the `Selected_Version` 
        in the `data` dictionary, and sets the path in the specified line edit widget. It then saves the updated version 
        information in the configuration file under both `Selected_Version` and `Saved_Versions`.

        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget from which the currently selected version is retrieved.
        - line_edit_target (`QLineEdit`): The line edit widget where the path of the selected version is displayed.
        - data (`dict`): The dictionary containing configuration data.
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
        Updates the `Path_selected` in the `File_Path_Config` section of the configuration file.

        This function retrieves the currently selected path from the combo box, updates the `Path_selected` in the 
        `data` dictionary, and displays the path in the specified line edit widget. It then saves the updated path 
        information in the configuration file under the `Path_selected` section.

        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget from which the currently selected path is retrieved.
        - line_edit_target (`QLineEdit`): The line edit widget where the selected path is displayed.
        - data (`dict`): The dictionary containing configuration data.
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
        Updates the `index_combox` in the `Last_Session_Config` section of the configuration file.

        This function retrieves the currently selected index from the given combo box and updates the 
        `index_combox` in the `Last_Session_Config` dictionary, specifically updating the index for the 
        provided combo box number. The updated index is saved in the configuration file to persist 
        the user's last selection.

        Parameters
        ----------
        - combo_box_num (`int`): The index of the combo box in the `Last_Session_Config` section.
        - combo_box (`QComboBox`): The combo box widget from which the selected index is retrieved.
        """
        update_data_file(
            comobo_box.currentIndex(),
            ["Last_Session_Config", "ConfigTAB", "Index_Combox", combo_box_num],
        )