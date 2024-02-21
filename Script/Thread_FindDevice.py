import subprocess
from platform import system

from PyQt5.Qt import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal
 
from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Utils import toggle_button_state
from Script.Utilities.Auxiliary_Funcs import connection_errors
 
class FindDeviceW_Thread(QThread):
    """
    This class is used to run the `FindDevice` commands in a `separate thread`.
    
    Parameters
    ----------
    - command (`str`): the command to run in the thread.
    - path (`str`): the path to the scrcpy folder.
    - *func_args (`tuple`): the arguments for the function.
    """
    # signals
    get_device_output = pyqtSignal(dict)
    output_connect = pyqtSignal(list)
    disconnect_output = pyqtSignal(str)
    
    def __init__(self, command: str, path: str, *func_args: tuple):
        super().__init__()
        self.command = command
        self.path = "." if system() != "Windows" else path
        self.func_args = func_args
            
    def run(self):
        if self.command == "get_devices_infos":
            self.get_devices_infos()
        elif self.command == "disconnect_device":
            self.disconnect_device()
        elif self.command == "connect_device":
            self.connect_device()
        else:
            raise ValueError(f"the command '{self.command}' is not valid")
            
    def get_devices_infos(self) -> dict:
        """
        This function runs `commands` to get the `list of devices` and their infos (`ip`, `model`).
        
        Emits
        -----
        - get_device_output (`dict`): dictionary of `devices infos`
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
            model_out = subprocess.run(
                args=f"adb -s {device} shell getprop ro.product.model", 
                shell=True, 
                stdout=subprocess.PIPE, 
                cwd=self.path,
            )
            
            ip = ip_out.stdout.decode("utf-8").lower().rstrip()
            model = model_out.stdout.decode("utf-8").lower().rstrip()
            if not ip_out.stderr.decode("utf-8").lower().rstrip():
                ip = ip.split("inet ")[1].split("/")[0]
                devices_infos[device_num] = [ip, model.title()]
        
        self.get_device_output.emit(devices_infos)     
                
    def connect_device(self) -> list:
        """
        This function runs the `adb tcpip` and `adb connect` in a `separate thread`.
        
        Emits
        -----
        - `connect_output` (`list`): the output of the `adb connect` command. [error, output]
        """
        self.old_text = toggle_button_state(
            self.func_args[3], #buttons
            False,
            disabled_text="..."
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
        - emits_devices (`dict`): dictionary of `devices infos` 
          provided by `get_devices_infos` function.
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