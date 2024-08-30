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
    This class represents the device selection UI.
    
    Parameters
    ----------
    - devices (`list`): A list of devices.
    - path (`str`): The path to the selected version.
    - ui_type (`str`): The type of UI to display.
    - *args: Additional arguments.
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
        device_board = QGroupBox()
        device_board.setFixedSize(221, 35)
        device_board.setObjectName("DeviceBoxNative")
        
        button_locate = (153, 0) if self.large_device_list else (166, 0)
        device_text = f"{device_name[:17]}..." if len(device_name) > 20 else device_name
        
        label_device_name = Create.Label(device_text, device_board, (10, 8))
        label_device_name.move(5, 7)
        select_button = Create.Button("Select", device_board, (55, 35), "SelectDeviceButton")
        select_button.move(button_locate[0], 0)
        self.buttons.append(select_button)
        
        if self.ui_type == "Device Resolution":
            self.connect_select_button(select_button, device_name)
        elif self.ui_type == "Disconnect Device":
            self.connect_select_button(select_button, device_name, device_board)
        elif self.ui_type == "Start Device":
            self.connect_select_button(select_button, device_name, self.device_last_index)
        else:
            self.connect_select_button(select_button, device_name, self.device_last_index)
        self.device_last_index+=1
        
        return device_board
    
    def connect_select_button(self, button, *def_arg) -> None:
        """
        This function connects the correct function for each type of situation.
        
        Parameters
        ----------
        
        - button (`QPushButton`): The button to connect.
        - *def_arg (`list`): The arguments to pass to the function.
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
        This function starts thread that will charge the resolution of the chosen device.
        
        Parameters
        ----------
        - device_name (`str`): device name.
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
        This function starts thread that will disconnect the `scrcpy` of the chosen device.
        
        Parameters
        ----------
        - device_name (`str`): device name.
        - device_board (`QGroupBox`): is the QGroupBox of the corresponding device.
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
        This function starts thread that will start the `scrcpy` of the chosen device.
        
        Parameters
        ----------
        - device_name (`str`): name of the device.
        - device_index (`int`): index of the device.
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
        This function stops all instances of scrcpy using a `psutil` function called `process_iter`.
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
        This function will start the Thread that will open the `shell` of the chosen device.
        
        Parameters
        ----------
        
        - device_name (`str`): name of the device.
        - device_index (`int`): index of the device.
        
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
