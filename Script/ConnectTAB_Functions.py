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
        Connects to the selected device using the specified `ip` and `port` in a separate thread.

        This function initiates a connection to a target device by using its `ip` and `port`. The connection 
        process is handled asynchronously in a thread to avoid blocking the main application. Before starting, 
        it displays an alert to ensure the user has properly configured the device. Additionally, it disables 
        specified buttons during the connection process and re-enables them once the operation completes.

        Parameters
        ----------
        - connect_infos (`list`): A list containing the connection details, where:
          - `connect_infos[0]` (str): The device's IP address.
          - `connect_infos[1]` (str): The port number used for the connection.
        - buttons (`list`): A list of button widgets (`QPushButton`) that should be toggled to avoid 
        concurrent actions during the connection process.
        - path (`str`): The file path to the scrcpy folder, which is required to execute the connection logic.
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
        Connects to a saved device configuration selected from the combo box.

        This function retrieves the saved IP and port configuration of a device from the combo box and attempts 
        to establish a connection using the specified `scrcpy` version. It ensures that the selected `scrcpy` path 
        is valid and that the required binaries are present. Appropriate alerts are displayed in case of missing 
        configurations or errors.

        Parameters
        ----------
        - buttons (`list`): A list of button widgets (`QPushButton`) to toggle during the connection process.
        - combo_box (`QComboBox`): The combo box widget containing the saved device configurations.
        - data (`dict`): A dictionary with the application’s configuration data, including:
          - `Versions` (`dict`): Contains information about available `scrcpy` versions, including the selected one.
          - `Connect` (`dict`): Stores the saved device IPs and ports.
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
        
    def connect_to_line_edit(self, buttons: list, line_edits: list, data: dict, return_connect_infos: bool = False) -> None | list:
        """
        Connects to a device using IP and port specified in line edit widgets.

        This function retrieves the `ip` and `port` values entered in the provided line edits and attempts 
        to establish a connection using the specified `scrcpy` version. If `return_connect_infos` is set to `True`, 
        it returns the processed connection information (`ip` and `port`) instead of initiating the connection. 
        Appropriate alerts are displayed for missing inputs or errors.

        Parameters
        ----------
        - buttons (`list`): A list of button widgets (`QPushButton`) to toggle during the connection process.
        - line_edits (`list`): A list of `QLineEdit` widgets where users input the `ip` and `port`.
          - `line_edits[0]` (str): The device's IP address.
          - `line_edits[1]` (str): The port number used for the connection.
        - data (`dict`): A dictionary with the application’s configuration data, including:
          - `Versions` (`dict`): Contains information about available `scrcpy` versions, including the selected one.
        - return_connect_infos (`bool`, optional): If `True`, the function returns the processed `ip` and `port` 
        without initiating the connection. Defaults to `False`.

        Returns
        -------
        - `list`: A list containing the `ip` and `port` if `return_connect_infos` is `True`. Otherwise, `None`.
        """
        if path := data["Versions"]["Selected_Version"]["Path"] or not running_on_windows:
            if verify_scrcpy_path(path):
                connect_infos = [obj.text().rstrip().lstrip() for obj in line_edits]
                if all(connect_infos):
                    if return_connect_infos:
                        return connect_infos
                    else:
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
            
    def connect_wifi_debug(self, non_concurrent_buttons: list, line_edits: list, data: dict) -> None:
        """
        Connects a device using Wi-Fi debugging with a pairing code.

        This function establishes a Wi-Fi debugging connection by retrieving the IP and port from the specified 
        line edits, prompting the user for a pairing code, and validating the inputs. If all inputs are valid, 
        the connection process is initiated asynchronously in a separate thread. The UI buttons are disabled 
        during the connection process to prevent concurrent actions.

        Parameters
        ----------
        - non_concurrent_buttons (`list`): A list of button widgets (`QPushButton`) to toggle during the connection process.
        - line_edits (`list`): A list of `QLineEdit` widgets where users input the `ip` and `port`.
          - `line_edits[0]` (str): The device's IP address.
          - `line_edits[1]` (str): The port number used for the connection.
        - data (`dict`): A dictionary containing the application’s configuration data, including:
          - `Versions` (`dict`): Contains information about available `scrcpy` versions, including the selected one.

        Notes
        -----
        - The function first calls `connect_to_line_edit` to validate and retrieve the `ip` and `port` from the 
        line edits. If the fields are invalid or empty, appropriate alerts are displayed.
        """
        connect_infos = self.connect_to_line_edit(non_concurrent_buttons, line_edits, data, True)
        path = data["Versions"]["Selected_Version"]["Path"]
        accept_confirm = create_alert(
            "Check The Filled Fields",
            "Check if the IP and Port match Wifi Debug before proceeding",
            "confirm",
        )
        if accept_confirm:
            while True:
                pair_code, accept_input = create_alert(
                    "Pair Code",
                    "Enter your Wi-Fi Debug pairing code and place it in the field below.",
                    "input",
                )
                if not pair_code and accept_input:
                    create_alert(
                        "Pair Code Error",
                        "Pair code cannot be empty",
                    )
                else:
                    break
            if accept_input:
                original_text = toggle_button_state(
                    non_concurrent_buttons,
                    False
                )
                self.terminal = ConnectTAB_Thread(
                    "wifi_connect_device",
                    path,
                    connect_infos[0],
                    connect_infos[1],
                    pair_code,
                )
                self.terminal.start()
                self.terminal.wifi_connect_output.connect(
                    self.terminal.check_emits_wifi_debug
                )
                self.terminal.finished.connect(
                    partial(
                        toggle_button_state,
                        non_concurrent_buttons,
                        True,
                        original_text,
                    )
                )                      
    
    def save_custom_connection(self, combo_box_target: QComboBox, list_edits: list, data: dict) -> None:
        """
        Saves a custom IP connection to the configuration data.

        This function allows the user to save a new custom IP connection by providing the `ip` and `port` 
        via a list of input fields. If the `ip` and `port` are valid and the connection does not already exist, 
        the connection is added to the specified combo box and saved in the configuration data. 
        This ensures that the user's custom connections are stored for future sessions.

        Parameters
        ----------
        - combo_box_target (`QComboBox`): The combo box widget where the new connection will be added.
        - list_edits (`list`): A list of line edits containing the `ip` and `port` values to save.
        - data (`dict`): The dictionary that holds the custom IP connections. The key is a string in the format 
        `ip:port` and the value is a list containing the `ip` and `port`.
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
        Deletes a custom IP connection saved in the configuration.

        This function allows the user to delete a previously saved custom IP connection. The function checks 
        whether the currently selected IP in the `combo_box` exists in the saved connections. If the IP exists, 
        the user is prompted to confirm the deletion. Upon confirmation, the IP is removed from the combo box, 
        deleted from the configuration data, and the changes are saved back to the configuration file.

        Parameters
        ----------
        - combo_box (`QComboBox`): The combo box widget from which the selected custom IP is retrieved.
        - data (`dict`): A dictionary containing the saved custom IP connections. The key is the IP address, 
        and the value is the connection data.
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
        Disconnects the currently connected device using the `DisconnectUI`.

        This function initiates the disconnection process by calling the `ConnectTAB_Thread` to retrieve the 
        connected device information. It disables the provided buttons during the disconnection process to 
        prevent concurrent actions. Once the device information is retrieved, the `DisconnectUI` is displayed 
        for the user to proceed with the disconnection.

        Parameters
        ----------
        - buttons (`list`): A list of button widgets (`QPushButton`) to toggle during the disconnection process.
        - data (`dict`): A dictionary containing the application’s configuration data, including:
          - `Versions` (`dict`): Contains information about the `scrcpy` version, including the selected one.
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
        Updates the last selected IP index in the session configuration.

        This function retrieves the current index of a selected item from a `QComboBox` widget and updates 
        the `Ip_Index` field within the `Last_Session_Config` section of the configuration file. 
        This ensures that the user's last selected IP is remembered for future sessions.

        Parameters
        ----------
        - combo_box (`QComboBox`): The `QComboBox` widget from which the currently selected index is retrieved.
        """
        update_data_file(
            combo_box.currentIndex(),
            ["Last_Session_Config", "ConnectTAB", "Ip_Index"],
        )

    def last_text_infos(self, line_edit: QLineEdit, index: int) -> None:
        """
        Updates the last session configuration with the text from a line edit widget.

        This function retrieves the text from a specified `QLineEdit` widget and updates the corresponding entry 
        in the `LineEdit_Texts` list within the `Last_Session_Config` section of the configuration file. 
        It ensures that the most recent user input is saved for future sessions.

        Parameters
        ----------
        - line_edit (`QLineEdit`): The `QLineEdit` widget from which the text is retrieved.
        - index (`int`): The index in the `LineEdit_Texts` list where the retrieved text will be stored.
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
        Detects compatible devices using a background thread.

        This function initiates the process of detecting compatible devices by calling a background thread to 
        gather device information. It first verifies that the `scrcpy` installation is valid. If the installation 
        is valid, the devices are detected and listed in the `DeviceListUi`. The function ensures that buttons 
        are disabled during the process to avoid concurrent actions.

        Parameters
        ----------
        - buttons (`list`): A list of non-concurrent buttons (`QPushButton`) to toggle during the detection process.
        - DeviceListUi (`QScrollArea`): The user interface component where the detected devices will be displayed.
        - data (`dict`): A dictionary containing the configuration data, which includes information about the 
        selected version of `scrcpy`.
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
        Connects to a device using a background thread.

        This function attempts to establish a connection to a device using its `IP` and a specified `PORT`. It
        leverages a background thread (`FindDeviceW_Thread`) to manage the connection process, ensuring that
        the main UI remains responsive. If the `PORT` and `scrcpy` path are valid, the connection will be initiated.
        If either the `PORT` is missing or the `scrcpy` installation is not found, an appropriate alert is shown to 
        the user.

        Parameters
        ----------
        - device_ip (`str`): The IP address of the device to connect to.
        - connect_list (`list`): A list of currently connected devices. This can be used to track or update device 
        connection status.
        - buttons (`list`): A list of non-concurrent buttons (`QPushButton`) to toggle during the connection process.
        - data (`dict`): The configuration data, including the `PORT` to use and the path to the selected `scrcpy` version.
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
        Saves the port value entered in the UI.

        This function saves the port value entered in the `line_port` field into the `data` dictionary, 
        specifically under the key `Port_Auto`. It then updates the configuration file with the new port value.
        The port is expected to be a string, and it is stored to ensure the next time the application is run, 
        the same port value is retained.

        Parameters
        ----------
        - line_port (`QLineEdit`): The `QLineEdit` widget where the user inputs the port value.
        - data (`dict`): The dictionary containing the connection configuration data, where the port value will 
        be saved.
        """
        data["Port_Auto"] = line_port.text()
        update_data_file(
            line_port.text(),
            ["Connect", "Port_Auto"],
        )