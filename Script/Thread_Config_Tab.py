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
    This class runs the specified command in a separate thread to prevent blocking the main UI thread.

    The `ConfigTAB_Thread` class is designed to handle background operations, such as executing commands 
    related to the `scrcpy`, while allowing the UI to remain responsive. The class uses PyQt's threading 
    mechanisms and signals to communicate the results of the operations back to the main thread.

    Parameters
    ----------
    - command_name (`str`): The name of the command to run in the thread, related to scrcpy operations.
    - path (`str`): The path to the scrcpy installation folder, where necessary executables (e.g., `scrcpy`, `adb`) are located.
    - *func_args (`tuple`): The arguments that will be passed to the function that is executed in the thread.

    Signals
    -------
    - `charge_resolution_output` (`pyqtSignal(str)`): Emitted when resolution data is updated.
    - `get_device_output` (`pyqtSignal(list)`): Emitted with the list of devices found by the command.
    - `reset_server_output` (`pyqtSignal(list)`): Emitted to reset the server after executing the command.
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
        Runs the `adb devices` command in a separate thread to retrieve the list of connected devices.

        This function uses `subprocess` to execute the `adb devices` command and parse the output into a 
        list of connected devices. The list of devices is then emitted to the main UI thread through the 
        `get_device_output` signal.

        Emits
        -----
        - `get_device_output` (`list`): A list of devices currently connected via ADB.
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
        Runs the `adb shell wm size` command in a separate thread to update the resolution of the connected device.

        This function allows the user to set or reset the resolution of a device by invoking the `adb shell wm size` 
        command. It handles both setting a specific resolution and resetting to the default resolution. The result 
        (success or error message) is emitted back to the main thread through the `charge_resolution_output` signal.

        Emits
        -----
        - `charge_resolution_output` (`str`): The output of the `adb shell wm size` command, either the updated resolution 
        or an error message if something goes wrong.

        Parameters (self.func_args[n])
        ----------
        - device (`str`) `[0]`: The device identifier (usually `adb` device ID).
        - resolution (`str`) `[1]`: The desired resolution to be set for the device, or an empty string to reset.
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
        Resets the ADB server by running `adb kill-server` followed by `adb start-server` in a separate thread.

        This function is used to restart the ADB server, which may be necessary when encountering issues with device 
        connections. The process involves stopping the ADB server and then starting it again. Any error or warning messages 
        generated during this process are emitted back to the main thread through the `reset_server_output` signal.

        Emits
        -----
        - `reset_server_output` (`list`): A list containing any errors or warnings that occurred during the execution 
        of the `adb kill-server` and `adb start-server` commands.
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
        This function retrieves the version of scrcpy by executing the `scrcpy -v` command in a separate thread.

        It runs the scrcpy command to fetch its version, processes the output, and extracts the version number. The version 
        is then stored in the provided data dictionary and updated in the configuration file. If there is an error retrieving 
        the version, an alert is shown and the client window is closed if applicable.

        Emits
        -----
        - This function does not emit any signals but updates the configuration data.

        Parameters (self.func_args[n])
        ----------
        - version_name (`str`) `[0]`: The name of the version.
        - data (`dict`) `[1]`: A dictionary where the selected scrcpy version information is stored.
        - client (`QDialog`) `[2]`: The client window.
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
        
    @pyqtSlot(list)
    def start_resolution_ui(self, device_list: list) -> None:
        """
        Starts the UI for selecting a device to change its resolution.

        This function displays the UI that allows the user to choose a device from the provided `device_list` and set its 
        resolution. The function checks if a resolution is provided and passes it to the UI. If no devices are found, 
        an alert is shown to inform the user.

        Parameters
        ----------
        - device_list (`list`): A list of devices available for resolution adjustment. This list is passed to the device 
        selection UI.
        - self.func_args[n]:
            - path (`str`) `[0]`: Path to the scrcpy folder, used by the UI for device interaction.
            - resolution (`str`) `[1]`: The desired resolution to set for the selected device. If not provided, resolution 
            will be left as `None`.
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
        - self.func_args[n]:
            - buttons (`list`) `[0]`: list of buttons to toggle.
            - original_text (`str`) `[1]`: original text of the button.
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