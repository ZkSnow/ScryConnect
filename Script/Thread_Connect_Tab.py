import subprocess
from contextlib import suppress

from platform import system

from PyQt5.Qt import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal

from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Utils import check_is_ip, toggle_button_state
from Script.Utilities.Auxiliary_Funcs import connection_errors
 
class ConnectTAB_Thread(QThread):
    """
    This class runs the specified `Connect` commands in a separate thread to prevent blocking the main UI thread.

    The `ConnectTAB_Thread` class is designed to handle background operations related to device connectivity 
    (such as connecting or disconnecting devices) without affecting the responsiveness of the UI. The class 
    uses PyQt's threading mechanisms and signals to communicate the results of the operations back to the main thread.

    Parameters
    ----------
    - command (`str`): The command to run in the thread, related to connecting or disconnecting devices.
    - path (`str`): The path to the scrcpy installation folder, where necessary executables (e.g., `scrcpy`, `adb`) are located.
    - *func_args (`tuple`): The arguments that will be passed to the function executed in the thread.

    Signals
    -------
    - `connect_output` (`pyqtSignal(list)`): Emitted with the result of the connection attempt.
    - `get_device_output` (`pyqtSignal(list)`): Emitted with the list of connected devices.
    - `disconnect_output` (`pyqtSignal(str)`): Emitted with the result of the disconnect command.
    - `wifi_connect_output` (`pyqtSignal(str)`): Emitted with the result of the Wi-Fi connection attempt.
    """
    connect_output = pyqtSignal(list)
    get_device_output = pyqtSignal(list)
    disconnect_output = pyqtSignal(str)
    wifi_connect_output = pyqtSignal(str)
    
    def __init__(self, command: str, path: str, *func_args: tuple):
        super().__init__()
        self.command = command.lower()
        self.path = "." if system() != "Windows" else path
        self.func_args = func_args
    
    def run(self):
        if self.command == "connect_device":
            self.connect_device()
        elif self.command == "wifi_connect_device": 
            self.wifi_connect_device()
        elif self.command == "get_connect_devices":
            self.get_connect_devices()
        elif self.command == "disconnect_device":
            self.disconnect_device()
        else:
            raise ValueError(f"the command '{self.command}' is not valid")
            
    def connect_device(self) -> list:
        """
        Establishes a connection to a device by running the `adb tcpip` and `adb connect` commands in a separate thread.

        This function triggers the `adb tcpip` command to set the device into TCP/IP mode and then attempts to connect 
        to the device using the `adb connect` command. Both operations are executed in sequence within a separate thread. 
        The results, including any errors and standard output, are captured and emitted to the caller.

        Emits
        ------
        - connect_output (`list`): A list containing the results of the `adb tcpip` and `adb connect` commands. 
        The list includes error messages (if any) and the standard output. The order is `[error, output]`.
        
        Parameters (self.func_args[n])
        ----------
        - port (`str`) `[0]`: The port number to use for the connection.
        - ip (`str`) `[1]`:  The IP address of the device to connect to.
        """
        out_tcp = subprocess.run(
            args=f"adb tcpip {self.func_args[1]}", #ip
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            cwd=self.path
        )
        out_connect = subprocess.run(
            args=f"adb connect {self.func_args[0]}", #port
            shell=True,
            stdout=subprocess.PIPE,
            cwd=self.path,
        )
        
        out_tcpip = out_tcp.stdout.decode("utf-8").lower().rstrip()
        err_tcpip = out_tcp.stderr.decode("utf-8").lower().rstrip()
        out_connect = out_connect.stdout.decode("utf-8").lower().rstrip()
        
        results = [err_tcpip, out_connect] if err_tcpip else [out_tcpip, out_connect]
        self.connect_output.emit(results)   
   
    def wifi_connect_device(self):
        """
        Connects to a device over Wi-Fi by pairing it using the `adb pair` command after enabling TCP/IP mode.

        This function first enables TCP/IP mode on the device by running the `adb tcpip` command. Then, it attempts to pair
        the device using the `adb pair` command with the provided IP address, port, and pairing code. The results, including
        any errors or success messages, are captured and emitted to the caller.

        Emits
        ------
        - wifi_connect_output (`str`): The result of the `adb pair` command. If an error occurs, the error message is emitted; 
        otherwise, the success message is emitted.
        
        Parameters (self.func_args[n])
        ----------
        - ip (`str`) `[0]`: The IP address of the device to connect to.
        - port (`str`) `[1]`: The port number to use for the connection.
        - code (`str`) `[2]`: The pairing code to use for the connection.
        """
        subprocess.run(
            args=f"adb tcpip 5555",
            shell=True,
            cwd=self.path,
        )
        device = subprocess.run(
            args=f"adb pair {self.func_args[0]}:{self.func_args[1]} {self.func_args[2]}",
            shell=True,
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        out = device.stdout.decode("utf-8").lower().rstrip()
        err = device.stderr.decode("utf-8").lower().rstrip()
        if err:
            self.wifi_connect_output.emit(err)
        else:
            self.wifi_connect_output.emit(out)
        
    def get_connect_devices(self) -> list:
        """
        Retrieves a list of connected devices by running the `adb devices` command in a separate thread.

        This function executes the `adb devices` command to get the list of devices currently connected via ADB. It processes
        the output to extract the device identifiers and filters for devices with valid IP addresses. The resulting list of 
        device identifiers is then emitted to the caller.

        Emits
        ------
        - get_devices_output (`list`): A list of connected device identifiers (IPs) obtained from the output of the `adb devices` command.
        """
        list_devices = subprocess.run(
            args="adb devices", 
            shell=True, 
            cwd=self.path,
            stdout=subprocess.PIPE, 
        ).stdout.decode("utf-8").splitlines()

        devices_list = [] 
        list_devices.remove("")
        for device in list_devices[1:]:
            if check_is_ip(device):
                devices_list.append(device.split("\t")[0])
        self.get_device_output.emit(devices_list)
    
    def disconnect_device(self) -> str:
        """
        Disconnects a device from ADB by running the `adb disconnect` command in a separate thread.

        This function attempts to disconnect a device from ADB using the `adb disconnect` command, providing the device 
        identifier as an argument. The output or error resulting from the command is captured and emitted to the caller.

        Emits
        ------
        - disconnect_output (`str`): The result of the `adb disconnect` command. This could be either an error message or 
        the success output.
        
        Parameters (self.func_args[n])
        ----------
        - device (`str`) `[0]`: The device identifier (usually `adb` device ID).
        """
        out = subprocess.run(
            args=f"adb disconnect {self.func_args[0]}", #device
            shell=True,
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        if error:= out.stderr.decode("utf-8").lower().rstrip():
            self.disconnect_output.emit(error)
        else:
            output = out.stdout.decode("utf-8").lower().rstrip()
            self.disconnect_output.emit(output)
    
    @pyqtSlot(list)
    def start_disconnect_ui(self, device_list: list) -> None:
        """
        Starts the UI for selecting a device to disconnect from ADB.

        This function activates the UI to allow the user to choose a device from the provided `device_list` for disconnection. 
        It also toggles the state of certain UI elements (such as buttons) based on the device list. If no devices are found, 
        an alert is displayed to notify the user.

        Parameters
        ----------
        - device_list (`list`): A list of devices available for disconnection. This list is passed to the device selection UI.
        - self.func_args[n]:
            - buttons (`list`) `[0]`: A list of buttons to toggle.
            - original_text (`str`) `[1]`: The text to set on the buttons.
            - DeviceSelectionUI (`class`) `[2]`: A class representing the device selection UI.
        """
        toggle_button_state(
            self.func_args[0], #buttons
            True,
            self.func_args[1], #original_text
        )
        
        if device_list:
            DeviceSelectionUI = self.func_args[2]
            DeviceSelectionUI(device_list, self.path, "Disconnect Device")
        else:
            create_alert(
                "Nothing Found",
                ("No device found, make sure " 
                "it is connected via Wi-Fi")
            )
     
    @pyqtSlot(list)
    def check_emits_connect(self, emits_outputs: list) -> None:
        """
        This function checks for `errors` in the `emits_outputs`.
        
        Parameters
        ----------
        - emits_outputs (`list`): list of error provided by `connect_device` function.
        """
        error_detect = connection_errors(emits_outputs[0], emits_outputs[1])
        if not error_detect and "connected to" in emits_outputs[1].lower():
            create_alert(
                "SUCCESS",
                "Successfully connected",
            )            

    @pyqtSlot(str)
    def check_emits_wifi_debug(self, emit_output: str) -> None:
        """
        This function checks for `errors` in the `emit_output`.
        
        Parameters
        ----------
        - emit_output (`str`): str of error provided by `wifi_connect_device` function.
        """
        error_detect = connection_errors("", emit_output)
        if not error_detect:
            create_alert(
                "SUCCESS",
                "Successfully connected",
            )

        
    @pyqtSlot(str)
    def check_emits_disconnect(self, emit_output: str) -> None:
        """
        This function checks for `errors` in the `emit_output`.
        
        Parameters
        ----------
        - emit_output (`str`): str of error provided by `disconnect_device` function.
        - self.func_args[n]:
            - device_board (`QGroupBox`) `[1]`: The QGroupBox of the corresponding device.
        """
        print(emit_output, "<----")
        if "no such device" in emit_output:
            create_alert(
                "Failed To Find Device",
                ("Cannot find the device, check if it" 
                "has been connected before and is valid")
            )
        elif "security exception" in emit_output:
            create_alert(
                "Permission refused",
                ("Go in developer options and make sure\n"
                "'USB debugging (Security setting)' is enabled"),
            )
        else:
            create_alert(
                "SUCCESS",
                "The selected device was successfully disconnected",
            )
        
        with suppress(RuntimeError):
            self.func_args[1].deleteLater() #device_board
              
    