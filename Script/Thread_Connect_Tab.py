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
    This class is used to run the `Connect` commands in a `separate thread`.
    
    Parameters
    ----------
    - command (`str`): the command to run in the thread.
    - path (`str`): the path to the scrcpy folder.
    - *func_args (`tuple`): the arguments for the function.
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
        This function runs the `adb tcpip` and `adb connect` in a `separate thread`.
        
        Emits
        -----
        - connect_output (`list`) --> results of `adb tcpip` and `adb connect`. [error, output]
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
        This function runs the `adb devices` in a `separate thread` to get the list of `devices`.
        
        Emits
        -----
        - get_devices_output (`list`) --> list of `devices`
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
        This function runs the `adb disconnect` in a `separate thread`.
        
        Emits
        ------
        - disconnect_output (`str`): the output of the disconnect command.
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
        """This function runs the UI for choosing the `device` to start the `disconnect`."""
        
        toggle_button_state(
            self.func_args[0], #buttons
            True,
            self.func_args[1], #old_text
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
    def check_emits_wifi_debug(self, wifi_output: str) -> None:
        error_detect = connection_errors("", wifi_output) #fazer os button off e on
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
              
    