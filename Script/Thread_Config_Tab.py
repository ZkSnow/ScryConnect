from curses.ascii import isdigit
import subprocess
from platform import system

from PyQt5.Qt import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal

from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Utils import toggle_button_state, update_data_file

running_on_windows = system() == "Windows"
class ConfigTAB_Thread(QThread):
    """
    This class is used to run the `start` commands in a `separate thread`.
    
    Parameters
    ----------
    - command (`str`): the command to run in the thread.
    - path (`str`): the path to the scrcpy folder.
    - *func_args (`tuple`): the arguments for the function.
    """
    
    charge_resolution_output = pyqtSignal(str)
    get_device_output = pyqtSignal(list)
    reset_server_output = pyqtSignal(list)
    
    def __init__(self, command_name: str, path: str, *func_args: tuple) -> None:
        super().__init__(None)
        self.command_name = command_name.lower()
        self.path = path if running_on_windows == "Windows" else path
        self.func_args = list(func_args)
    
    def run(self):
        if self.command_name == "charge_device_resolution":
            self.charge_device_resolution()
        elif self.command_name == "get_devices":
            self.get_connect_devices()
        elif self.command_name == "reset_adb_server":
            self.reset_adb_server()
        elif self.command_name == "get_scrcpy_version_and_save":
            self.get_scrcpy_version_and_save()
        else:
            raise ValueError(f"the command '{self.command_name}' is not valid")

    def get_connect_devices(self) -> list:
        """
        This function runs the `adb devices` in a `separate thread` to get the list of `devices`.
        
        Emits
        -----
        - `get_device_output` (`list`) --> list of `devices`.
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
            devices_list.append(device.split("\t")[0])

        self.get_device_output.emit(devices_list)

    def charge_device_resolution(self) -> str:
        """
        This function runs the `adb shell wm size` in a `separate thread` 
        to charge the `device` resolution.
        
        Emits
        -----
        - `charge_resolution_output` (`str`): the output of the `adb shell wm size` command.
        """
        device = self.func_args[0]    
        resolution = self.func_args[1]
        arg_line = f"adb -s {device} shell wm size {resolution}" if resolution \
        else f"adb -s {device} shell wm size reset" 
        
        size_out = subprocess.run(
            args=arg_line,
            shell=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=self.path,
        )       
        err = size_out.stderr.decode("utf-8").lower().rstrip()
        out = size_out.stdout.decode("utf-8").lower().rstrip()
        
        if err:
            self.charge_resolution_output.emit(err)
        else:
            self.charge_resolution_output.emit(out)
            
    def reset_adb_server(self) -> list:
        """
        This function runs the `adb kill-server` and `adb start-server` in a `separate thread` 
        to reset the `adb` server.
        
        Emits
        -----
        - `reset_server_output` (`list`): list of `errors` and `warnings` provided by the 
                                `reset_server` function.
        """
        end = subprocess.run(
            args="adb kill-server",
            shell=True,
            stderr=subprocess.PIPE,
            cwd=self.path,
        )
        start = subprocess.run(
            args="adb start-server",
            shell=True,
            stderr=subprocess.PIPE,
            cwd=self.path,
        )
        
        end_err = end.stderr.decode("latin1").rstrip().lower()
        start_err = start.stderr.decode("latin1").rstrip().lower()
        
        self.reset_server_output.emit([start_err, end_err])
    
    def get_scrcpy_version_and_save(self):
        """
        This function runs the `scrcpy -v` in a `separate thread` to get the version of `scrcpy`.
        """
        scrcpy_version = subprocess.run(
            args="scrcpy -v",
            shell=True,
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode("utf-8").lower().rstrip().lstrip().split()
        
        if not scrcpy_version and not running_on_windows:
            create_alert(
                "Error",
                "Error getting scrcpy version.",
            )
            self.func_args[2].close() #client
        
        else:
            find_version_point = False
            version = ""
            for char in scrcpy_version[1]:
                if char == "." and find_version_point is False:
                    find_version_point = True
                    version += char
                elif char != "." and isdigit(char):
                    version += char
            
            scrcpy_version = float(version)        
            
            scrcpy_info = {
                "Path": self.path,
                "Version": scrcpy_version,
            }
            version_name = self.func_args[0]
            data = self.func_args[1]
            data["Selected_Version"] = scrcpy_info
            
            update_data_file(
                scrcpy_info,
                ["Versions", "Selected_Version"],
            )
            
            if running_on_windows:
                data["Saved_Versions"][version_name] = scrcpy_info
                update_data_file(
                    scrcpy_info,
                    ["Versions", "Saved_Versions", version_name],
                )
        
    @pyqtSlot(str)
    def check_emit_res(self, emit_output: str) -> None:
        """
        This function checks for `errors` in the `emits_ouputs`.
        
        Parameters
        ----------
        - emit_output (`str`): str of error provided by `charge_device_resolution` function.
        """
        if 'not found' in emit_output:
            create_alert(
                "Device Not Found",
                "No device found, check if it is properly connected (USB or Wi-Fi)",
            )
        elif "security exception" in emit_output:
            create_alert(
                "Permission refused",
                ("Go in developer options and make sure 'USB debugging "
                "(Security setting)' is enabled"),
            )
        elif "not implemented: display" in emit_output:
            create_alert(
                "Not Supported Resolution",
                ("The selected resolution is not supported by your device\n"
                 "Try a different resolution (your device will likely reboot)"),
            )
        else:
            create_alert(
                "SUCCESS",
                "The Resolution was successfully modified!",
            )
    
    @pyqtSlot(list)
    def check_emit_reset(self, emits_ouputs: list) -> None:
        """
        This function checks for `errors` in the `emits_ouputs`.
        
        Parameters
        ----------
        - emits_ouputs (`list`): list of errors provided by `reset_adb_server` function.
        """
        if "started successfully" in (start_emit := emits_ouputs[0]):
            create_alert(
                "Server ADB",
                "The ADB server has been successfully reset!",
            )
        print(start_emit, "<< start")
        print(emits_ouputs[1], "<< end")

        toggle_button_state(
            self.func_args[0], #buttons
            True,
            self.func_args[1], #original_text
        )
    
    @pyqtSlot(list)
    def start_resolution_ui(self, device_list: list) -> None:
        """
        This functions runs UI for choosing the `device` to change the `resolution` of the `device`.
        
        Parameters
        ----------
        - device_list (`list`): list of `devices`.
        """
        if device_list:
            DeviceSelectionUI = self.func_args[0]
            if resolution:= self.func_args[1]:
                DeviceSelectionUI(device_list, self.path, "Device Resolution", resolution)
            else:
                DeviceSelectionUI(device_list, self.path, "Device Resolution", None)
        else:
            create_alert(
                "Nothing Found",
                ("No device found, make sure " 
                "it is connected via Wi-Fi or USB")
            )

    