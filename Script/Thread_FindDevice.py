import subprocess
from platform import system

from PyQt5.Qt import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal
 
from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Utils import toggle_button_state
from Script.Utilities.Auxiliary_Funcs import connection_errors
 
class FindDeviceW_Thread(QThread):
    """
    This class is used to run the `FindDevice` commands in a separate thread.

    It allows executing commands related to device discovery and handling in the background, 
    without blocking the main UI thread. The output of the command can be emitted via custom signals.

    Parameters
    ----------
    - command (`str`): The command to run in the thread, typically related to device discovery or management.
    - path (`str`): The path to the `scrcpy` folder. On non-Windows systems, the path is set to the current directory.
    - *func_args (`tuple`): Additional arguments to be passed to the function that the thread is running.

    Signals
    -------
    - `get_device_output` (`pyqtSignal(dict)`): Emitted with a dictionary containing the output of the device discovery process.
    - `output_connect` (`pyqtSignal(list)`): Emitted with a list of outputs to be processed further.
    - `disconnect_output` (`pyqtSignal(str)`): Emitted with a message indicating the result of the disconnection attempt.
    """
    # signals
    get_device_output = pyqtSignal(dict)
    output_connect = pyqtSignal(list)
    
    def __init__(self, command: str, path: str, *func_args: tuple):
        super().__init__()
        self.command = command
        self.path = "." if system() != "Windows" else path
        self.func_args = func_args
            
    def run(self):
        methods_dict = {
            "get_devices_infos": self.get_devices_infos,
            "connect_device": self.connect_device,
        }
        
        try:
            method = methods_dict[self.command]
            method()
        except KeyError:
            raise ValueError(f"the command '{self.command}' is not valid.")
            
    def get_devices_infos(self) -> dict:
        """
        Runs commands to retrieve the list of connected devices and their information (IP address, model, and brand).

        This function uses `adb` commands to gather information about each connected device. It retrieves the device 
        serial numbers, their IP addresses, and the device brand and model. The information is then compiled into a dictionary 
        and emitted via a signal.

        Returns
        -------
        - `dict`: A dictionary where each key is a device index (device number), and the value is a list containing:
            - IP address (`str`): The IP address of the device.
            - Model and brand (`str`): The model and brand of the device in the format "Brand (Model)".

        Emits
        ------
        - `get_device_output` (`pyqtSignal(dict)`): Emitted with a dictionary containing device information.
        """
        #get device serials ↓
        lists_serials = subprocess.run(
            args="adb devices",
            shell=True,
            stdout=subprocess.PIPE,
            cwd=self.path
        ).stdout.decode("utf-8").splitlines()
        
        devices_serials = []
        for serial in lists_serials[1:-1]:
            devices_serials.append(serial.split("\t")[0])
        
        #get devices infos ↓
        devices_infos = {} 
        for device_num, device in enumerate(devices_serials):
            ip_out = subprocess.run(
                args=f"adb -s {device} shell ip addr show wlan0", 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                cwd=self.path,
            )
            
            brand = subprocess.run(
                args=f"adb -s {device} shell getprop ro.product.brand",
                shell=True, 
                stdout=subprocess.PIPE, 
                cwd=self.path,
            ).stdout.decode("utf-8").title().rstrip()
            
            model = subprocess.run(
                args=f"adb -s {device} shell getprop ro.product.model", 
                shell=True, 
                stdout=subprocess.PIPE, 
                cwd=self.path,
            ).stdout.decode("utf-8").title().rstrip()
            
            if not ip_out.stderr.decode("utf-8").lower().rstrip():
                ip = ip_out.stdout.decode("utf-8").lower().rstrip()
                ip = ip.split("inet ")[1].split("/")[0]
                devices_infos[device_num] = [ip, f"{brand} ({model})"]
        
        self.get_device_output.emit(devices_infos)     
                
    def connect_device(self) -> list:
        """
        Runs the `adb tcpip` and `adb connect` commands in a separate thread to establish a TCP/IP connection to a device.

        This function initiates a connection to a device over TCP/IP by first using `adb tcpip <device_port>` to enable 
        TCP/IP mode, followed by `adb connect <device_ip>` to establish the connection. The results of these commands 
        are then captured and emitted.

        Emits
        ------
        - `connect_output` (`pyqtSignal(list)`): A list containing two elements:
            - The first element is either an error message (if any occurred) from the `adb tcpip` command or its output.
            - The second element is the output message from the `adb connect` command.
        """
        self.old_text = toggle_button_state(
            self.func_args[3], #buttons
            False,
        )
        
        out_tcp = subprocess.run(
            args=f"adb tcpip {self.func_args[0]}", #device_port
            shell=True,  
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            cwd=self.path
        )
        out_connect = subprocess.run(
            args=f"adb connect {self.func_args[1]}", #device_ip
            shell=True,
            stdout=subprocess.PIPE,
            cwd=self.path
        )
        
        out_tcpip = out_tcp.stdout.decode("utf-8").lower().rstrip()
        err_tcpip = out_tcp.stderr.decode("utf-8").lower().rstrip()
        out_connect = out_connect.stdout.decode("utf-8").lower().rstrip()
        
        results = [err_tcpip, out_connect] if err_tcpip else [out_tcpip, out_connect]
        self.output_connect.emit(results)         

    @pyqtSlot(dict)
    def add_devices(self, emits_devices: dict) -> None:
        """
        This function adds the `emits_devices` to the `DeviceListUi` using device infos.
        
        Parameters
        ----------
        - emits_devices (`dict`): dictionary of `devices infos` provided by `get_devices_infos` function.
        """
        if emits_devices:
            for device in emits_devices.values():
                device_ip = device[0]
                device_name = device[1]
                DeviceListUi = self.func_args[2]
                if device_ip not in DeviceListUi.detected_devices:
                    DeviceListUi.add_board(device_name, device_ip)
                    DeviceListUi.detected_devices.append(device_ip)
                
            create_alert(
                "Devices Detected",
                "Compatible devices have been detected.",
            )
        else:
            create_alert(
                "Nothing Detected",
                ("No devices were detected make sure your\n" 
                "device is properly connected (USB)"),
            )
        toggle_button_state(
            self.func_args[0], #buttons
            True, 
            self.func_args[1], #old_texts
        )
    
    @pyqtSlot(list)
    def check_emits_connect(self, emits_outputs: list) -> None:
        """
        This function checks for `errors` in the `emits_outputs` using `connection_errors` function.
        
        Parameters
        ----------
        - emits_outputs (`list`): list of errors provided by `connect_device` function.
        """
        error_detect = connection_errors(emits_outputs[0], emits_outputs[1])
        if not error_detect and "connected to" in emits_outputs[1].lower():
            create_alert(
                "SUCCESS",
                "Successfully connected",
            )

        toggle_button_state(
            self.func_args[3], #buttons
            True,
            self.old_text,
        )