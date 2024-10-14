from functools import partial
from platform import system

from PyQt5.QtWidgets import QComboBox, QLineEdit, QScrollArea

from UI.DeviceSelection import DeviceSelectionUI 
from Script.Thread_Connect_Tab import ConnectTAB_Thread 
from Script.Thread_FindDevice import FindDeviceW_Thread 
from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Utils import (
    toggle_button_state,
    verify_scrcpy_path,
    update_data_file,
)

running_on_windows = system() == "Windows"
class ConnectTAB():
    """This class contains all the functions for the `ConnectTAB`."""
    def __init__(self):
        self.terminal = None
     
    def connect_device(self, connect_infos: list, buttons: list, path: str) -> None:
        """
        This function connects to the selected device using the `ip`/`port` in a `thread`.
        
        Parameters
        ----------
        - connect_infos (`list`): The list containing the `ip`/`port` to connect to the device.
        - buttons (`list`): The list of non-concurrent buttons to toggle.
        - path (`str`): The path to the scrcpy folder.
        """
        create_alert(
            "ALERT",
            ("Make sure your device is properly " \
            "configured and connected via USB"),
        )
        original_texts = toggle_button_state(
            buttons, 
            False,
        )
        self.terminal = ConnectTAB_Thread(
            "connect_device",
            path, 
            connect_infos[0], #ip
            connect_infos[1], #port
        )
        self.terminal.start()
        self.terminal.finished.connect(
            partial(
                toggle_button_state,
                buttons,
                True,
                original_texts,
            )
        )
    
    def connect_to_saved(self, buttons: list, combo_box: QComboBox, data: dict) -> None:
        """
        This function prepares the `ip`/`port` to connect to the selected device using the combo box.
        
        Parameters
        ----------
        - buttons (`list`): The list of non-concurrent buttons.
        - combo_box (`QComboBox`): The combo box containing the list of saved configurations.
        - data (`dict`): The dictionary containing the saved configurations.
        """
        if path := data["Versions"]["Selected_Version"]["Path"] or not running_on_windows:
            if verify_scrcpy_path(path):
                if ip := combo_box.currentText():
                    self.connect_device(data["Connect"]["Custom_Ip_Saved"][ip], buttons, path)
                    self.terminal.connect_output.connect(self.terminal.check_emits_connect)
                else:
                    create_alert(
                        "Nothing Selected",
                        "No IP has been selected",
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
        
    def connect_to_line_edit(self, buttons: list, line_edits: list, data: dict) -> None:
        """
        This function prepares the `ip`/`port` to connect to the selected device using the line edits.
        
        Parameters
        ----------
        - buttons (`list`): The list of non-concurrent buttons.
        - line_edits (`list`): The list of line edits `ip`/`port`.
        - data (`dict`): The data of the config file.
        """
        if path := data["Versions"]["Selected_Version"]["Path"] or not running_on_windows:
            if verify_scrcpy_path(path):
                connect_infos = [obj.text().rstrip().lstrip() for obj in line_edits]
                if all(connect_infos):
                    self.connect_device(connect_infos, buttons, path)
                    self.terminal.connect_output.connect(self.terminal.check_emits_connect)
                else:
                    create_alert(
                        "Fill All",
                        ("Make sure all fields are filled out " 
                         "before you start the connection"),
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
    
    def save_custom_connection(self, combo_box_target: QComboBox, list_edits: list, data: dict) -> None:
        """
        This function saves a `custom connection` in `data`.
        
        Parameters
        ----------
        - combo_box_target (`QComboBox`): The combo box widget to get the combo box from.
        - list_edits (`list`): The list containing the sources of the `ip`/`port`.
        - data (`dict`): The dictionary to store the custom connections.
        """
        list_edits = [obj.text().rstrip().lstrip() for obj in list_edits]   
        if all(list_edits) and list_edits[0] not in data.keys():
            connection_name = f"{list_edits[0]}:{list_edits[1]}"
            combo_box_target.addItem(connection_name)
            combo_box_target.setCurrentIndex(combo_box_target.count() - 1)
            
            data[connection_name] = list_edits   
            update_data_file(
                list_edits,
                ["Connect", "Custom_Ip_Saved", connection_name],
            )
        else:
            create_alert(
                "IP Error",
                "The PORT or IP entered is invalid or already exists",
            )
        
    def delete_custom_connection(self, combo_box: QComboBox, data: dict) -> None:
        """
        This function deletes a `custom connection` saved in `data`.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget to get the combo box from.
        - data (`dict`): The dictionary containing the custom connections.
        """
        if (current_ip := combo_box.currentText().rstrip().lstrip()) in data:
            if create_alert(
                "Are You Sure?",
                f"You are about to delete the '{current_ip}' ip, do you want to continue?",
                "confirm",
            ):
                combo_box.removeItem(combo_box.findText(current_ip))
                del data[current_ip]
                update_data_file(
                    None,
                    ["Connect", "Custom_Ip_Saved", current_ip],
                    delete_value=True,
                )
        else: 
            create_alert(
                "Nothing Selected",
                "No ip Selected",
            )   

    def disconnect_device(self, buttons: list, data: dict) -> None:
        """
        This function `disconnects` the device with `DisconnectUI`.
        
        Parameters
        ----------
        - buttons (`list`): A list of non-concurrent buttons to toggle.
        - data (`dict`): The dictionary containing the userdata.
        """

        if path := data["Versions"]["Selected_Version"]["Path"] or not running_on_windows:
            if verify_scrcpy_path(path):
                original_text = toggle_button_state(
                    buttons, 
                    False
                )
                self.terminal = ConnectTAB_Thread(
                    "get_connect_devices",
                    path,
                    buttons,
                    original_text,
                    DeviceSelectionUI,
                )
                self.terminal.start()
                self.terminal.get_device_output.connect(
                    partial(
                        self.terminal.start_disconnect_ui,
                    )
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
             
    def last_ip_selected(self, combo_box: QComboBox) -> None:
        """
        This function updates the `ip_index` in `Last_Session_Config`.
        
        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget to get the index from.
        """
        update_data_file(
            combo_box.currentIndex(),
            ["Last_Session_Config", "ConnectTAB", "Ip_Index"],
        )

    def last_text_infos(self, line_edit: QLineEdit, index: int) -> None:
        """
        This function updates the `LineEdit_Texts` in `Last_Session_Config`.
        
        Parameters
        ----------
        - line_edit (`QLineEdit`): The line edit widget to get the text from.
        - index (`int`): The index of the text in `LineEdit_Texts`.
        """
        update_data_file(
            line_edit.text(),
            ["Last_Session_Config", "ConnectTAB", "LineEdit_Texts", index],
        )

class DeviceList():
    """This class contains all the functions for the `DeviceListUI`"""
    def __init__(self):
        self.terminal = None
    
    def detect_devices(self, buttons: list, DeviceListUi: QScrollArea, data: dict) -> None:
        """
        This function can be used to `detect` compatible devices using a `thread`.
        
        Parameters
        ----------
        - buttons (`list`): list of non-concurrent buttons to toggle.
        - DeviceListUi (`QScrollArea`): ui representing the device list.
        - data (`dict`): data of the config file.
        """
        if path := data["Selected_Version"]["Path"] or not running_on_windows:
            if verify_scrcpy_path(path):
                original_texts = toggle_button_state(
                    buttons,
                    False,
                )
                self.terminal = FindDeviceW_Thread(
                    "get_devices_infos",
                    path,
                    buttons,
                    original_texts,
                    DeviceListUi,
                )
                self.terminal.start()
                self.terminal.get_device_output.connect(
                    partial(
                        self.terminal.add_devices,
                    )
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
      
    def connect_device(
        self,
        device_ip: str,
        connect_list: list,
        buttons: list,
        data: dict
    ) -> None:
        """
        This function can be used to `connect` to a device using a `thread`.
        
        Parameters
        ----------
        - device_ip (`str`): device ip.
        - connect_list (`list`): list of connected devices.
        - buttons (`list`): list of non-concurrent buttons to toggle.
        - data (`dict`): data of the config file.
        """
        device_port = data["Connect"]["Port_Auto"]
        if (device_port := device_port.rstrip().lstrip() if device_port else None):
            path = data["Versions"]["Selected_Version"]["Path"]
            if verify_scrcpy_path(path) or not running_on_windows:
                self.terminal = FindDeviceW_Thread(
                    "connect_device",
                    path,
                    device_port,
                    device_ip,
                    connect_list,
                    buttons,
                )
                self.terminal.start()
                self.terminal.output_connect.connect(
                    self.terminal.check_emits_connect,
                )
            else:
                create_alert(
                    "Error in finding scrcpy",
                    ("the scrcpy/adb was not found in the version folder, " 
                    "check the folder and try again"),
                )
        else:
            create_alert(
                "Port Not Specified",
                "PORT has not been set, please set it and try again",
            )
    
    def save_ui_port(self, line_port: QLineEdit, data: dict):
        """
        This function is used to save the ui port
        
        Parameters
        ----------
        - line_port (`QLineEdit`): the line edit of the port.
        - data (`dict`): the data of the connect tab.
        """
        data["Port_Auto"] = line_port.text()
        update_data_file(
            line_port.text(),
            ["Connect", "Port_Auto"],
        )
