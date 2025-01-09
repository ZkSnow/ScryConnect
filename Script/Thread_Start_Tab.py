import subprocess
from platform import system

from PyQt5.Qt import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal

from Script.Utilities.Create_Alerts import create_alert 
from Script.Utilities.Utils import toggle_button_state, get_file_name
from Script.Utilities.Auxiliary_Funcs import (
    device_errors,
    args_combination_errors,
    arguments_errors,
    move_record_file
)
class StartTAB_Thread(QThread):
    """
    This class is used to run the `start` commands in a separate thread.

    It allows executing commands related to starting processes or handling tasks in the background, 
    without blocking the main UI thread. The results of the operations can be emitted via custom signals.

    Parameters
    ----------
    - command (`str`): The command to be executed in the thread. Typically, it represents a specific action to perform.
    - path (`str`): The path to the `scrcpy` folder. On non-Windows systems, it defaults to the current directory.
    - *func_args (`tuple`): Additional arguments to be passed to the function executed in the thread.

    Signals
    -------
    - `start_scrcpy_output` (`pyqtSignal(str)`): Emitted with a string containing the output of the `start` process.
    - `get_devices_output` (`pyqtSignal(list)`): Emitted with a list of detected devices or related outputs.
    """
    # signals
    start_scrcpy_output = pyqtSignal(str)
    get_devices_output = pyqtSignal(list)
    
    def __init__(self, command: str, path: str, *func_args: tuple):
        super().__init__()
        self.command = command.lower()
        self.path = "." if system() != "Windows" else path
        self.func_args = list(func_args)

    def run(self):
        methods_dict = {
            "start_scrcpy": self.start_scrcpy,
            "get_connect_devices": self.get_connect_devices,
            "open_shell": self.open_shell,
        }
        
        try:
            method = methods_dict[self.command]
            method()
        except KeyError:
            raise ValueError(f"the command '{self.command}' is not valid.")
        
    def start_scrcpy(self) -> str:
        """
        Runs the `scrcpy` command in a separate thread.

        This function executes the scrcpy command line with the provided arguments in the background. 
        It uses a subprocess to handle the execution and captures any error messages that occur during the process.

        Emits
        -----
        - `start_scrcpy_output` (`str`): An error message emitted if the scrcpy process encounters an issue.
        """
        arg_line = self.func_args[1]
        arg_line, file_name = get_file_name(self.func_args[1], self.path)
        
        scrcpy_err = subprocess.run(
            args=arg_line, #arg_line
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.path,
        ).stderr.decode("utf-8").rstrip().lower()
        if file_name:
            self.func_args[2] = file_name
    
        toggle_button_state(
            self.func_args[4], #button
            True,
            charge_text=False,
        )

        self.start_scrcpy_output.emit(str(scrcpy_err))
    
    def get_connect_devices(self) -> list:
        """
        Retrieves the list of connected devices using the `adb devices` command.

        This function executes the `adb devices` command in a separate thread to fetch a list of connected devices.
        It processes the command output to extract the device identifiers and emits the resulting list.

        Emits
        -----
        - `get_devices_output` (`list`): A list containing the identifiers of connected devices.
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
        
        self.get_devices_output.emit(devices_list)
    
    def open_shell(self) -> None:
        """
        Opens an ADB shell session in a separate thread.

        This function launches an `adb shell` command for the specified device in an appropriate terminal emulator 
        based on the operating system.

        Behavior
        --------
        - On Windows: Executes the command in `cmd.exe` using `start cmd.exe /k`.
        - On Linux: Detects the terminal emulator and runs the command in it.
        """
        if system() == "Windows":
            cmd = f"start cmd.exe /k adb -s {self.func_args[0]} shell"
        else: #Linux
            terminal = subprocess.run(
                args=f"ls /usr/bin | grep terminal",
                shell=True,
                stdout=subprocess.PIPE,
                cwd=self.path,
            ).stdout.decode("utf-8").rstrip()
            terminal = terminal.split()[0]
            cmd = f"{terminal} -- bash -c 'adb -s {self.func_args[0]} shell; exec bash'"
            
        subprocess.run(
            args=cmd,
            shell=True,
            stderr=subprocess.PIPE,
            cwd=self.path,
        )
        toggle_button_state(
            self.func_args[1], #button
            True,
        )
    
    @pyqtSlot(list)
    def start_shell_ui(self, device_list: list) -> None:
        """
        Displays a UI for selecting a device to open the `ADB shell`.

        This function initializes the device selection user interface to allow the user to choose a device 
        from the provided list for opening an ADB shell session.

        Parameters
        ----------
        - device_list (`list`): A list of connected devices available for selection.
        """

        DeviceSelectionUI = self.func_args[0]
        if device_list:
            DeviceSelectionUI(device_list, self.path, "Open Shell")
        else:
            create_alert(
                "Nothing Found",
                "No device found, make sure it is connected via Wi-Fi or USB"
            )
    
    @pyqtSlot(list)
    def start_scrcpy_ui(self, device_list: list) -> None:
        """
        Displays a UI for selecting a device to start `scrcpy`.

        This function initializes the device selection user interface, allowing the user to choose a device 
        from the provided list for starting a `scrcpy` session.

        Parameters
        ----------
        - device_list (`list`): A list of connected devices available for selection.
        """
        client = self.func_args[4]
        DeviceSelectionUI = self.func_args[5]
        if device_list:
            DeviceSelectionUI(
                device_list,
                self.path,
                "Start Device",
                self.func_args[0], #target_file_path
                self.func_args[1], #arg_line
                self.func_args[2], #record_file
                self.func_args[3], #custom_dir_enabled
            )
        else:
            create_alert(
                "Nothing Found",
                "No device found, make sure it is connected via Wi-Fi or USB"
            )
        if client:
            client.show()

    @pyqtSlot(str)
    def check_output_start_scrcpy(self, err_out: str) -> None:
        """
        This function checks for `errors` in the `err_out`
        using the `args_errors`, `device_errors` and `args_combination_errors` functions.
        
        Parameters
        ----------
        - err_out (`str`): str of error provided by `start_scrcpy` function.
        """
        arg_error = arguments_errors(err_out)
        device_error = device_errors(err_out)      
        args_combo_error = args_combination_errors(err_out)  

        detect_error_list = [args_combo_error, device_error, arg_error]
        if (record_file := self.func_args[2]) and not any(detect_error_list):
            move_record_file(
                record_file,
                self.path,
                self.func_args[0], #target_file_path
                self.func_args[3], #custom_dir_enabled
            )
        
            
        
