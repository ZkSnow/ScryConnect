from functools import partial
from psutil import process_iter
from os.path import join

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt  
from PyQt5.QtWidgets import (
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QGroupBox,
    QDialog,
)

from Theme.icon_scrcpy import * 
import Script.Utilities.Create_Elements as Create
from Script.Utilities.Utils import connect_signal
from Script.Utilities.Utils import toggle_button_state
from Script.Thread_Connect_Tab import ConnectTAB_Thread
from Script.Thread_Start_Tab import StartTAB_Thread
from Script.Thread_Config_Tab import ConfigTAB_Thread
from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Utils import get_current_alert_theme


class DeviceSelectionUI(QDialog):
    """
    Represents the device selection user interface (UI).

    This class provides a dialog window for selecting a device from a given list. 
    It supports different UI types and handles scenarios with a large number of devices.

    Parameters
    ----------
    - devices (`list`): A list of devices available for selection.
    - path (`str`): The file path to the selected scrcpy version or related resources.
    - ui_type (`str`): The type of UI to display, determining the behavior or style 
    of the selection interface.
    - *args: Additional arguments for UI types.
    """
    def __init__(self, devices: list, path: str, ui_type: str, *args):
        super().__init__()
        self.terminal = None
        self.devices = devices
        self.path = path
        self.ui_type = ui_type
        self.args = args
        self.device_last_index = 0
        self.buttons = []
        self.large_device_list = len(self.devices) > 7
        self.setWindowTitle("Device Select")
        self.setFixedWidth(256)
        self.setWindowIcon(QIcon(join(":", "icon.ico")))
        self.start_ui()
    
    def start_ui(self):
        """
        Initializes and configures the device selection UI.

        This method sets up the UI components based on the selected `ui_type`
        and the list of available devices. It dynamically creates device boards 
        and organizes them in a scrollable area. Depending on the `ui_type`, 
        additional functionality like a "Stop ALL Devices" button may be included.

        Parameters
        ----------
        - ui_type (`str`): The type of UI to display, which determines the behavior 
        and layout of the dialog.
        - devices (`list`): The list of devices to be displayed in the UI.

        Raises
        ------
        - `ValueError`: If `ui_type` is not a valid string or does not match one 
        of the predefined options.
        """
        if not isinstance(self.ui_type, str):
            raise ValueError("Invalid UI type, must be a string")
                
        self.ui_type = self.ui_type.lower().title().rstrip().lstrip()
        if self.ui_type not in ["Disconnect Device", "Start Device", "Device Resolution", "Open Shell"]:
            raise ValueError(
                "Invalid UI type, must be one of the following: "
                "'Disconnect Device', 'Start Device', 'Device Resolution', 'Open Shell'"
            )
        
        self.setWindowTitle(self.ui_type)
        self.layout_content = QVBoxLayout()
        self.layout_content.setAlignment(Qt.AlignTop)
        
        for device_name in self.devices:
            self.layout_content.addWidget(
                self.create_device_board(
                    str(device_name)
                    )
                )
            
        self.scroll = QScrollArea()
        self.content = QWidget(self.scroll)
        self.content.setLayout(self.layout_content)
        self.scroll.setWidget(self.content)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel(self.ui_type), 1, 0, 1, 2)
        self.layout.addWidget(self.scroll, 2, 0, 1, 2)
        if self.ui_type == "Start Device":
            self.stopall_button = Create.Button("Stop ALL Devices")
            self.stopall_button.clicked.connect(self.stop_scrcpys)
            self.layout.addWidget(self.stopall_button, 3, 0, 1, 2)
            
        self.setLayout(self.layout)
        self.setStyleSheet(get_current_alert_theme())
        self.exec()
    
    def create_device_board(self, device_name: str) -> QGroupBox:
        """
        Creates a device board for displaying device information and a selection button.

        This method generates a `QGroupBox` containing a label with the device name 
        and a button to select the device. The layout and behavior vary depending 
        on the `ui_type`.

        Parameters
        ----------
        - device_name (`str`): The name of the device to display on the board.

        Returns
        -------
        - `QGroupBox`: A group box widget containing the device name and a selection button.

        Behavior Based on UI Type
        --------------------------
        - `Device Resolution`: Connects the select button to a handler for setting device resolution.
        - `Disconnect Device`: Connects the select button to a handler for disconnecting the device.
        - `Start Device`: Connects the select button to a handler for starting the device.
        - `Open Shell`: Connects the select button to a general handler with the device index.
        """
        device_board = QGroupBox()
        device_board.setFixedSize(221, 35)
        device_board.setObjectName("DeviceBoxNative")
        
        button_locate = (153, 0) if self.large_device_list else (166, 0)
        device_text = f"{device_name[:17]}..." if len(device_name) > 20 else device_name
        
        label_device_name = Create.Label(device_text, (10, 8), parent=device_board)
        label_device_name.move(5, 7)
        select_button = Create.Button("Select", (55, 35), "SelectDeviceButton", parent=device_board)
        select_button.move(button_locate[0], 0)
        self.buttons.append(select_button)
        
        if self.ui_type == "Device Resolution":
            self.connect_select_button(select_button, device_name)
        elif self.ui_type == "Disconnect Device":
            self.connect_select_button(select_button, device_name, device_board)
        elif self.ui_type == "Start Device":
            self.connect_select_button(select_button, device_name, self.device_last_index)
        else: # Open Shell
            self.connect_select_button(select_button, device_name, self.device_last_index)
        self.device_last_index+=1
        
        return device_board
    
    def connect_select_button(self, button, *def_arg) -> None:
        """
        Connects the appropriate function to the select button based on the `ui_type`.

        This method determines the action to perform when the select button is clicked 
        by checking the `ui_type` and connecting the button to the corresponding handler.

        Parameters
        ----------
        - button (`QPushButton`): The button to connect the function to.
        - *def_arg (`list`): The arguments to pass to the function when the button is clicked.
        """
        if self.ui_type == "Device Resolution":
            connect_signal(
                button,
                "clicked",
                self.charge_device_res,
                def_arg[0],
            )
            
        elif self.ui_type == "Disconnect Device":
            connect_signal(
                button,
                "clicked",
                self.disconnect,
                def_arg[0],
                def_arg[1],
            )
        elif self.ui_type == "Start Device": 
            connect_signal(
                button,
                "clicked",
                self.start_device,
                def_arg[0],
                def_arg[1],
            )
        else:
            connect_signal(
                button,
                "clicked",
                self.open_device_shell,
                def_arg[0],
                def_arg[1],
            )

    def charge_device_res(self, device_name: str) -> None:
        """
        Starts a thread to change the resolution of the chosen device.

        This method initiates a background thread to either change the resolution of 
        the specified device or revert it to the native resolution, depending on the 
        `args` passed during initialization. It also displays an alert to confirm the 
        action before proceeding.

        Parameters
        ----------
        - device_name (`str`): The name of the device for which the resolution will be changed.
        """
        if resolution := self.args[0]:
            alert_msg = ("You are about to change the phone's resolution " 
                         "via ADB, make sure the height and width are valid!")
        else:
            alert_msg = ("You are about to go back to the native resolution "
                        "of that device, are you sure?")
        if create_alert(
            "Are You Sure?",
            alert_msg,
            "confirm",
        ):
            self.terminal = ConfigTAB_Thread(
                "charge_device_resolution",
                self.path,
                device_name,
                resolution,
            )
            self.terminal.start()
            self.terminal.charge_resolution_output.connect(
                partial(
                    self.terminal.check_emit_res,
                )
            )
    
    def disconnect(self, device_name: str, device_board: QGroupBox) -> None:
        """
        Starts a thread to disconnect the `scrcpy` session for the chosen device.

        This method initiates a background thread to disconnect the specified device from 
        the `scrcpy` session. Before proceeding, a confirmation alert is shown to the user.

        Parameters
        ----------
        - device_name (`str`): The name of the device to disconnect.
        - device_board (`QGroupBox`): The `QGroupBox` widget representing the device's UI element.
        """
        if create_alert(
            "Are you sure?",
            "You are about to disconnect a device",
            "confirm",
        ):
            self.terminal = ConnectTAB_Thread(
                "disconnect_device",
                self.path,
                device_name,
                device_board,
            )
            self.terminal.start()
            self.terminal.disconnect_output.connect(
                self.terminal.check_emits_disconnect,
            )
            
    def start_device(self, device_name: str, device_index: int) -> None:
        """
        Starts a thread to initiate the `scrcpy` session for the chosen device.

        This method triggers a background thread to start a `scrcpy` session for the specified device, 
        using the arguments passed during initialization. Before starting, it disables the select button 
        for the device to prevent multiple actions.

        Parameters
        ----------
        - device_name (`str`): The name of the device to start the `scrcpy` session for.
        - device_index (`int`): The index of the device in the list of available devices.
        """
        toggle_button_state(
            self.buttons[device_index],
            False,
            charge_text=False,
        )

        target_file_path = self.args[0]
        arg_line = f"scrcpy -s {device_name} {self.args[1]}"
        record_file = self.args[2]
        custom_dir_enabled = self.args[3]
        self.terminal = StartTAB_Thread(
            "start_scrcpy",
            self.path,
            target_file_path,
            arg_line,
            record_file,
            custom_dir_enabled,
            self.buttons[device_index],
        )
        self.terminal.start()
        self.terminal.start_scrcpy_output.connect(
            self.terminal.check_output_start_scrcpy,
        )

    def stop_scrcpys(self):
        """
        Stops all instances of `scrcpy` by terminating processes using `psutil`.

        This method scans all running processes and stops any instances of `scrcpy` by identifying 
        processes with names `scrcpy.exe` (on Windows) or `scrcpy` (on other systems). Before terminating 
        the processes, a confirmation alert is shown to warn the user that recordings will not be saved 
        and may become corrupted.
        """
        if create_alert(
            "Are you sure?",
            ("You are about to stop all instances of scrcpy\n"
            "recordings will not be saved (corrupted)"),
            "confirm",
        ):
            for process in process_iter(["name"]):
                if process.info["name"].lower() in ["scrcpy.exe", "scrcpy"]:
                    process.terminate()
                    toggle_button_state(
                        self.buttons,
                        True,
                        charge_text=False,
                    )
    
    def open_device_shell(self, device_name: str, device_index: int)  -> None:
        """
        Starts a thread to open the shell of the chosen device.

        This method triggers a background thread that opens the device's shell interface, allowing 
        interaction with the device via command line. Before starting, it disables the corresponding 
        button to prevent multiple actions.

        Parameters
        ----------
        - device_name (`str`): The name of the device to open the shell for.
        - device_index (`int`): The index of the device in the list of available devices.
        """
        toggle_button_state(
            self.buttons[device_index],
            False,
            charge_text=False,
        )
        
        self.terminal = StartTAB_Thread(
            "open_shell",
            self.path,
            device_name,
            self.buttons[device_index],
        )
        self.terminal.start()
