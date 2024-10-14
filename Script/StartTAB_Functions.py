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
        This function is used to load a saved configuration 
        and update the GUI elements with the corresponding values.
        
        Parameters
        ----------
        - combo_box_source (`QComboBox`): The combo box containing the list of saved configurations.
        - checks (`list`): A list of check boxes.
        - line_edits (`list`): A list of line edits.
        - combo_boxs (`list`): A list of combo boxes.
        - sliders (`list`): A list of sliders.
        - data (`dict`): A dictionary containing the saved data.
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
        This function is used to save a custom start configuration.
        
        Parameters
        ----------
        - combo_box_target (`QComboBox`): The combo box containing the list of saved configurations.
        - checks (`list`): A list of check boxes.
        - line_edits (`list`): A list of line edit widgets.
        - combo_boxs (`list`): A list of combo box widgets.
        - sliders (`list`): A list of slider widgets.
        - data (`dict`): A dictionary containing the saved data.
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
        This function is used to delete a saved start configuration.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box containing the list of saved configurations.
        - data (`dict`): A dictionary containing the saved data.
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
        This function is used to run scrcpy with the specified arguments.
        If there is no ui_arg_line, it will use manual_arg_line (custom line for editing args).
        
        Parameters
        ----------
        - data (`dict`): A dictionary containing the saved data.
        - manual_arg_line (`str`): The manual arguments line.
        - ui_arg_line (`str`): The ui arguments line.
        - client (`QMainWindow`, `optional`): The client window.
        """
             
        arg_line = manual_arg_line.text().lower() if manual_arg_line else ui_arg_line
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
        This function is used to run scrcpy custom line args (line edit).
        
        Parameters
        ----------
        - line_edit (`QLineEdit`): The line edit widget to get the arg line from.
        - Data (`dict`): A dictionary containing the saved configuration data.
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
        This function is used to execute scrcpy with the arguments specified by ui.
        
        Parameters
        ----------
        - Sliders (`list`): A list of slider widgets.
        - Check_Boxes (`list`): A list of check box widgets.
        - Combo_Boxs (`list`): A list of combo box widgets.
        - Line_Edits (`list`): A list of line edit widgets.
        - Data (`dict`): A dictionary containing the saved configuration data.
        - Client (`QMainWindow`, `optional`): The client object. Defaults to None.
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
            "SDK"
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
        data: dict,
    ) -> None:
        """
        This function updates the `data file` with the value of the `slider` and the `line edit`.  
        The line edit values used are those representing the slider values.
        
        Parameters
        ----------
        - slider (`QSlider`): The slider widget to get the value from.
        - line_edit_value (`QLineEdit`): The line edit widget to update with the new value.
        - index (`int`): The index of the slider in the `data file`.
        - data (`dict`): The data dictionary to update.
        """      
        new_value = slider.value()
        line_edit_value.setText(str(new_value))
        update_data_file(
            new_value,
            ["Last_Session_Config", "StartTAB", "Slider_Value", index],
        )

    def value_edit_charge_event(self, line_edit: QLineEdit, target_slider: QSlider) -> None:
        """
        This function updates the `data file` with the value of the `line edit`
        The line edits values used are those representing the slider values.
        
        Parameters
        ----------
        - line_edit (`QLineEdit`): The line edit widget to get the value from.
        - target_slider (`QSlider`): The slider widget to update with the new value.
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
        This function updates the `data file` with the index of the `combo box`.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget to get the index from.
        - index (`int`): The index of the combo box in the `data file`.
        """
        update_data_file(
            combo_box.currentIndex(),
            ["Last_Session_Config", "StartTAB", "Indexs_Combox", index],
        )
    
    def last_texts(self, line_edit: QLineEdit, index: int) -> None:
        """
        This function updates the `data file` with the text of the `line edit`.
        
        Parameters
        ----------
        - line_edit (`QLineEdit`): The line edit widget to get the text from.
        - index (`int`): The index of the line edit in the `data file`.
        """
        update_data_file(
            line_edit.text(),
            ["Last_Session_Config", "StartTAB", "LineEdit_Texts", index],
        )
        
    def last_check_selected(self, index: int, data: dict) -> None:
        """
        This function updates the `data file` with the selected state of the `check box`.
        
        Parameters
        ----------
        - Index (`int`): The index of the check box in the `data file`.
        - Data (`dict`): The dictionary containing the data.
        """
        last_check_value = data["Check_Boxes"][index] = not data["Check_Boxes"][index]
        update_data_file(
            last_check_value,
            ["Last_Session_Config", "StartTAB", "Check_Boxes", index],
        )
    
    def back_to_default_config(self, checks, line_edits, combo_boxs, sliders) -> None:
        """
        This function loads the default config in the UI.
        
        Parameters
        ----------
        - checks (`list`): The list of check boxes.
        - line_edits (`list`): The list of line edits.
        - combo_boxs (`list`): The list of combo boxes.
        - sliders (`list`): The list of sliders.
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
        This function opens a new terminal window with the `adb shell` command.
        
        Parameters
        ----------
        - data (`dict`): A dictionary containing the saved data.
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
