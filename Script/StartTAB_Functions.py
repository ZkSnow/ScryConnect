from platform import system

from PyQt5.QtWidgets import QLineEdit, QComboBox, QSlider, QMainWindow

from Script.Thread_Start_Tab import StartTAB_Thread
from UI.DeviceSelection import DeviceSelectionUI 
from Script.Utilities.Static_Datas import USERDATA
from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Utils import (
    verify_scrcpy_path,
    valid_maxsize_value,
    get_file_name,
    update_data_file,
)
from Script.Utilities.Auxiliary_Funcs import (
    get_sliders_start,
    get_line_edit_start,
    get_combo_box_start,
    get_checkBox_start,
)
running_on_windows = system() == "Windows"
class StartTAB():
    """This class is used to handle the start tab functions"""
    def __init__(self):
        self.terminal = None
        
    def load_saved_config(
        self, 
        combo_box_source: QComboBox, 
        checks: list, 
        line_edits: list, 
        combo_boxs: list, 
        sliders: list, 
        data: dict,
    ) -> None:
        """
        Loads a saved configuration and updates the associated GUI elements.

        This function retrieves a saved configuration from the provided data dictionary based on the 
        currently selected configuration name in the source combo box. It updates the sliders, line edits, 
        combo boxes, and checkboxes in the GUI with the saved values. If no configuration is selected, 
        an alert is displayed.

        Parameters
        ----------
        - combo_box_source (`QComboBox`): The combo box containing the list of saved configurations.
        - checks (`list`): A list of QCheckBox widgets to be updated with the saved configuration state.
        - line_edits (`list`): A list of QLineEdit widgets to be updated with the saved text values.
        - combo_boxs (`list`): A list of QComboBox widgets to be updated with the saved index values.
        - sliders (`list`): A list of QSlider widgets to be updated with the saved slider positions.
        - data (`dict`): A dictionary containing the saved configuration data.
        """
        config_name = combo_box_source.currentText() if combo_box_source else "StartTAB"
        if config_name:
            for index, slider in enumerate(sliders):
                new_value = data[config_name]["Slider_Value"][index]
                slider.setValue(new_value)
                    
            for index, line_edit in enumerate(line_edits):
                new_text = data[config_name]["LineEdit_Texts"][index]
                line_edit.setText(new_text)
            
            for index, combo_box in enumerate(combo_boxs):
                new_index = data[config_name]["Indexs_Combox"][index]
                new_index = new_index - 1 if index == 0 else new_index
                combo_box.setCurrentIndex(new_index)       
                     
            for index, check in enumerate(checks):
                new_value = data[config_name]["Check_Boxes"][index]
                check.setChecked(new_value)
        else:
            create_alert(
                "None Selected",
                "No Config has been selected"
            )
                      
    def save_custom_config(
        self, 
        combo_box_target: QComboBox, 
        checks: list, 
        line_edits: list, 
        combo_boxs: list, 
        sliders: list, 
        data: dict,
    ) -> None:        
        """
        Saves a custom start configuration and updates the configuration data.

        This function allows the user to save the current state of GUI elements (sliders, line edits, 
        combo boxes, and checkboxes) as a named configuration. The configuration is stored in the 
        provided data dictionary, added to the target combo box, and saved to a data file. If the 
        provided name is invalid or already exists, an alert is displayed.

        Parameters
        ----------
        - combo_box_target (`QComboBox`): The combo box where the new configuration name will be added.
        - checks (`list`): A list of QCheckBox widgets to save the current checked states.
        - line_edits (`list`): A list of QLineEdit widgets to save the current text values.
        - combo_boxs (`list`): A list of QComboBox widgets to save the current selected indices.
        - sliders (`list`): A list of QSlider widgets to save the current slider positions.
        - data (`dict`): A dictionary where the new configuration will be stored.
        """
        config_name, accept_input = create_alert(
            "Type a Name", 
            "Type the name for this config ↓", 
            "input",
        )
        config_name = config_name.rstrip().lower().title().lstrip()
        if accept_input:
            if config_name and config_name not in data.keys():
                lines_texts, slider_values, index_comboxs, check_boxes = [], [], [], []
                for line_edit in line_edits:
                    lines_texts.append(line_edit.text())

                for slider in sliders:
                    slider_values.append(slider.value())

                for combo_box in combo_boxs:
                    index = max(combo_box.currentIndex(), 0)
                    index_comboxs.append(index)

                for check in checks:
                    check_boxes.append(check.isChecked())

                config_data = {
                    "LineEdit_Texts": lines_texts,
                    "Slider_Value": slider_values,
                    "Indexs_Combox": index_comboxs,
                    "Check_Boxes": check_boxes,
                }
                data[config_name] = config_data
                combo_box_target.addItem(config_name)
                combo_box_target.setCurrentIndex(combo_box_target.count()-1)
                index_comboxs[0] = len(data.keys())
                update_data_file(
                    config_data,
                    ["Custom_Config_Set", config_name],
                )
            else:
                create_alert(
                    "Name Error",
                    "The name entered is invalid or already exists",
                )

    def delete_saved_config(self, combo_box: QComboBox, data: dict) -> None: 
        """
        Deletes a saved start configuration from the configuration data.

        This function removes a selected configuration from the combo box and the associated 
        data dictionary. The deletion is confirmed with the user before proceeding. If no 
        configuration is selected, an alert is displayed.

        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box containing the list of saved configurations.
        - data (`dict`): A dictionary storing the saved configurations.
        """

        if config_name := combo_box.currentText():
            if create_alert(
                "Are you sure?",
                f"you're about to delete the '{config_name}' setting, are you sure?",
                "confirm",
            ):
                combo_box.removeItem(combo_box.findText(config_name))
                del data[config_name]
                update_data_file(
                    None,
                    ["Custom_Config_Set", config_name],
                    delete_value=True,
                )
        else:
            create_alert(
                "None Selected",
                "No Config has been selected",
            )       
   
    def run_scrcpy(
        self,
        data: dict,
        manual_arg_line: str = "",
        ui_arg_line: str = "",
        client: QMainWindow = None,
    ) -> None:
        """
        Runs scrcpy with the specified arguments and configuration.

        This function starts scrcpy using either manually provided arguments or UI-generated arguments. 
        It validates the arguments, ensures the required scrcpy path exists, and manages the execution 
        through a separate thread. Alerts are displayed for any validation or path-related errors.

        Parameters
        ----------
        - data (`dict`): A dictionary containing saved configurations, including the selected scrcpy version and paths.
        - manual_arg_line (`str`): A string containing manually entered arguments for scrcpy. Takes precedence over `ui_arg_line`.
        - ui_arg_line (`str`): A string containing arguments generated by the UI.
        - client (`QMainWindow`, optional): The main client window, which can be hidden during scrcpy execution.

        Raises
        ------
        - `ValueError`: If the `-m` or `--max-size` argument has a value below 500, causing potential errors.
        - `FileNotFoundError`: If the scrcpy or adb executables are missing in the selected version folder.
        """
        arg_line = manual_arg_line.text() if manual_arg_line else ui_arg_line
        if valid_maxsize_value(arg_line):
            if path := data["Versions"]["Selected_Version"]["Path"] or not running_on_windows:
                if verify_scrcpy_path(path):
                    self.terminal = StartTAB_Thread(
                        "get_connect_devices", 
                        path,
                        data["File_Path_Config"]["Path_selected"],
                        arg_line,
                        get_file_name(arg_line)[1],
                        data["File_Path_Config"]["Path_Mode_Radio"][0] == True,
                        client,
                        DeviceSelectionUI,
                    )
                    self.terminal.start()
                    self.terminal.get_devices_output.connect(
                        self.terminal.start_scrcpy_ui,
                    )
                    if client:
                        client.hide()
                    
                else:
                    create_alert(
                        "Error in finding scrcpy",
                        ("the scrcpy/adb was not found in the version folder, " 
                        "check the folder and try again"),
                    )
            else: 
                create_alert(
                    "Nothing Selected",
                    ("No version has been selected -> "
                    "<a href='https://github.com/Genymobile/scrcpy/releases'>Scrcpy Releases</a> or "
                    "<a href='https://github.com/Genymobile/scrcpy/blob/master/doc/linux.md#latest-version'>Scrcpy for Linux</a>"),
                )
        else:    
            create_alert(
                "Invalid Value",
                ("The arg '-m' or '--max-size' values are below 500, "
                "this can\ngenerate errors please fix the value and try again")
            )
        
    def line_arg_start_scrcpy(self, line_edit: QLineEdit, data: dict) -> None:
        """
        Runs scrcpy with custom arguments entered in a line edit widget.

        This function retrieves the argument line from the provided `QLineEdit` widget and passes it 
        to the `run_scrcpy` function to execute scrcpy with the specified custom arguments.

        Parameters
        ----------
        - line_edit (`QLineEdit`): The QLineEdit widget containing the custom argument line.
        - data (`dict`): A dictionary containing saved configuration data, used to retrieve version paths and other settings.
        """
        self.run_scrcpy(data, manual_arg_line=line_edit)
    
    def ui_start_scrcpy(
        self,
        sliders: list,
        check_boxes: list,
        combo_boxs: list,
        line_edits: list,
        data: dict,
        client: QMainWindow = None,
    ) -> None:
        """
        Executes scrcpy with the arguments specified by the UI elements.

        This function constructs a command line from various UI elements, including sliders, checkboxes, 
        combo boxes, and line edits. It then passes the constructed arguments to the `run_scrcpy` function 
        to start scrcpy with the specified configuration. If the selected scrcpy version is below 2.0, 
        an alert is displayed indicating that some features may not work.

        Parameters
        ----------
        - sliders (`list`): A list of QSlider widgets containing values for scrcpy options.
        - check_boxes (`list`): A list of QCheckBox widgets specifying additional arguments for scrcpy.
        - combo_boxs (`list`): A list of QComboBox widgets containing choices for scrcpy options.
        - line_edits (`list`): A list of QLineEdit widgets for custom arguments.
        - data (`dict`): A dictionary containing saved configuration data, including the selected scrcpy version.
        - client (`QMainWindow`, optional): The main client window, which can be hidden during scrcpy execution.
        """

        #Get all args ↓ ------------------
        args_w_required_values = [
            "display buffer",
            "crop",
            "record",
            "video buffer",
            "audio buffer",
            "time limit",
            "Mouse",
            "Keyboard",
            "Mouse + Keyboard",
            "AoA",
            "uHid",
            "SDK",
            "Mouse Binding",
            "Virtual Display",
            "Screen Off TO",
        ] 
        
        command_line = ""
        active_checks = [box.text().lower() for box in check_boxes if box.isChecked()]
        scrcpy_version = data["Versions"]["Selected_Version"]["Version"]
        scrcpy_version = float(scrcpy_version) if scrcpy_version else 0.0
        command_line += get_sliders_start(sliders, active_checks, scrcpy_version) 
        command_line += get_line_edit_start(line_edits, active_checks, combo_boxs[0], scrcpy_version)
        command_line += get_combo_box_start(combo_boxs, scrcpy_version)
        args_line, hide_client = get_checkBox_start(active_checks, args_w_required_values, scrcpy_version)
        command_line += args_line
        
        if scrcpy_version < 2.0:
            create_alert(
                "Scrcpy Version Alert",
                "Scrcpy version is below 2.0, some features will not work. "
            )
        
        print(command_line)
        self.run_scrcpy(
            data=data, 
            ui_arg_line=command_line, 
            client=client if hide_client else None
        )
   
    def slider_charge_event(
        self, 
        slider: QSlider, 
        line_edit_value: QLineEdit, 
        index: int, 
    ) -> None:
        """
        Updates the data file with the current value of a slider and its corresponding line edit.

        This function retrieves the current value from the provided `QSlider` widget, updates the 
        associated `QLineEdit` widget with the new value, and stores the value in the data file for 
        persistence. The index specifies the position of the slider in the data file structure.

        Parameters
        ----------
        - slider (`QSlider`): The QSlider widget from which the value is retrieved.
        - line_edit_value (`QLineEdit`): The QLineEdit widget to update with the slider's value.
        - index (`int`): The index of the slider in the data file, used to store the value.
        """
        new_value = slider.value()
        line_edit_value.setText(str(new_value))
        update_data_file(
            new_value,
            ["Last_Session_Config", "StartTAB", "Slider_Value", index],
        )

    def value_edit_charge_event(self, line_edit: QLineEdit, target_slider: QSlider) -> None:
        """
        Updates a slider based on the value entered in a line edit widget.

        This function retrieves the value from the provided `QLineEdit` widget, converts it to an integer, 
        and updates the associated `QSlider` widget with the new value. The value is clamped to the slider's 
        minimum and maximum range before being set.

        Parameters
        ----------
        - line_edit (`QLineEdit`): The QLineEdit widget from which the value is retrieved.
        - target_slider (`QSlider`): The QSlider widget to update with the new value.
        """
        min_value = target_slider.minimum()
        max_value = target_slider.maximum()
        try:
            new_value = int(line_edit.text())
        except ValueError:
            new_value = min_value

        new_value = max(new_value, min_value)
        new_value = min(new_value, max_value)
        target_slider.setValue(new_value)
    
    def last_index(self, combo_box: QComboBox, index: int) -> None:
        """
        Updates the data file with the current index of a combo box.

        This function retrieves the current index from the provided `QComboBox` widget and stores it 
        in the data file at the specified index position. This allows the selected combo box option to 
        persist across sessions.

        Parameters
        ----------
        - combo_box (`QComboBox`): The QComboBox widget from which the current index is retrieved.
        - index (`int`): The index of the combo box in the data file, used to store the value.
        """
        update_data_file(
            combo_box.currentIndex(),
            ["Last_Session_Config", "StartTAB", "Indexs_Combox", index],
        )
    
    def last_texts(self, line_edit: QLineEdit, index: int) -> None:
        """
        Updates the data file with the text from a line edit widget.

        This function retrieves the current text from the provided `QLineEdit` widget and stores it 
        in the data file at the specified index position. This allows the entered text to persist across sessions.

        Parameters
        ----------
        - line_edit (`QLineEdit`): The QLineEdit widget from which the text is retrieved.
        - index (`int`): The index of the line edit in the data file, used to store the value.
        """
        update_data_file(
            line_edit.text(),
            ["Last_Session_Config", "StartTAB", "LineEdit_Texts", index],
        )
        
    def last_check_selected(self, index: int, data: dict) -> None:
        """
        Updates the data file with the selected state of a checkbox.

        This function toggles the state of the checkbox at the specified index and stores the new state 
        in the data file. The state is stored as a boolean value, representing whether the checkbox is 
        checked or unchecked.

        Parameters
        ----------
        - index (`int`): The index of the checkbox in the data file, used to store the state.
        - data (`dict`): The dictionary containing the saved configuration data, including checkbox states.
        """
        last_check_value = data["Check_Boxes"][index] = not data["Check_Boxes"][index]
        update_data_file(
            last_check_value,
            ["Last_Session_Config", "StartTAB", "Check_Boxes", index],
        )
    
    def back_to_default_config(
        self, 
        checks: list, 
        line_edits: list, 
        combo_boxs: list, 
        sliders: list
    ) -> None:
        """
        Loads the default configuration into the UI elements.

        This function resets the UI elements (checkboxes, line edits, combo boxes, and sliders) 
        to their default values by loading the default configuration data from the saved configuration.

        Parameters
        ----------
        - checks (`list`): A list of QCheckBox widgets to be updated with the default configuration values.
        - line_edits (`list`): A list of QLineEdit widgets to be updated with the default configuration texts.
        - combo_boxs (`list`): A list of QComboBox widgets to be updated with the default selection.
        - sliders (`list`): A list of QSlider widgets to be updated with the default values.

        Notes
        -----
        - The function uses the `load_saved_config` method to load the default configuration data from the 
        `USERDATA["Last_Session_Config"]`.
        """
        self.load_saved_config(
            None,
            checks,
            line_edits,
            combo_boxs,
            sliders,
            USERDATA["Last_Session_Config"],
        )
        
    def open_shell(self, data):
        """
        Opens a new terminal window to run the `adb shell` command.

        This function attempts to open a new terminal window that connects to the device using `adb shell` 
        by first verifying the `scrcpy` installation path. If the path is valid and the device is connected,
        it opens the terminal for interaction.

        Parameters
        ----------
        - data (`dict`): A dictionary containing the saved configuration data, including the selected scrcpy version.
        """
        if path := data["Versions"]["Selected_Version"]["Path"] or not running_on_windows:
            if verify_scrcpy_path(path):
                self.terminal = StartTAB_Thread(
                    "get_connect_devices",
                    path,
                    DeviceSelectionUI,
                )
                self.terminal.start()
                self.terminal.get_devices_output.connect(
                    self.terminal.start_shell_ui,
                )
            else:
                create_alert(
                    "Error in finding scrcpy",
                    ("the scrcpy/adb was not found in the version folder, " 
                    "check the folder and try again"),
                )
        else:
            create_alert(
                "Nothing Selected",
                ("No version has been selected -> "
                "<a href='https://github.com/Genymobile/scrcpy/releases'>Scrcpy Releases</a> or "
                "<a href='https://github.com/Genymobile/scrcpy/blob/master/doc/linux.md#latest-version'>Scrcpy for Linux</a>"),
            )
