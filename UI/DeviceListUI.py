from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QScrollArea,
    QWidget,
    QGroupBox,
    QVBoxLayout,
    QGridLayout
)
from Script.Utilities.Utils import connect_signal
from Script.ConnectTAB_Functions import DeviceList
import Script.Utilities.Create_Elements as Create

class DeviceListUI(QScrollArea):
    """
    Represents the device list user interface (UI-ConnectTab).

    This class creates a scrollable UI component to display and manage the list 
    of connected devices.

    Parameters
    ----------
    - userdata (`dict`): A dictionary containing the user data, including the 
    selected scrcpy version path and device information.
    - parent (`any`, optional): The parent widget of this UI. Defaults to `None`.
    """
    def __init__(self, userdata: dict, parent = None):
        super().__init__()
        self.path = userdata["Versions"]["Selected_Version"]["Path"]
        self.userdata = userdata
        self.detected_devices = []
        self.parent = parent
        self.find_devices_widget_instance = DeviceList()
        self.terminal = None
        self.setWidgetResizable(True)
        
        self.start_ui()
    
    def start_ui(self):
        """
        Initializes the user interface for the device list UI.

        This method sets up the main layout and widget for the device list UI, 
        ensuring that the content is scrollable and aligned to the top.
        """
        self.content = QWidget()
        self.content.setObjectName("FindDevicescontent")
        self.setWidget(self.content)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)
    
    def create_device_board(self, device_name: str, device_ip: str) -> QGroupBox:
        """
        Creates a device board UI component for a given device.

        This method generates a `QGroupBox` containing device details and a button 
        to connect to the specified device. The layout organizes the device name, 
        IP address, and connect button.

        Parameters
        ----------
        - device_name (`str`): The name of the device to display on the board.
        - device_ip (`str`): The IP address of the device to display on the board.

        Returns
        -------
        - `QGroupBox`: A group box widget containing the device details and the 
        connect button.
        """
        self.device_box = QGroupBox()
        self.board_layout = QGridLayout()
        self.board_layout.setSpacing(2)
        self.device_box.setMinimumSize(411, 120)
        
        self.label_device_name = Create.Label(f"Name: {device_name}")
        self.label_ip = Create.Label(f"IP: {device_ip}")
        self.button_connect = Create.Button("Connect Device", (111, 41))      
        
        self.board_layout.addWidget(self.label_device_name, 0, 0, Qt.AlignCenter)
        self.board_layout.addWidget(self.label_ip, 1, 0, Qt.AlignCenter)
        self.board_layout.addWidget(self.button_connect, 2, 0, Qt.AlignTop)
        
        self.device_box.setLayout(self.board_layout)
        
        connect_signal(
            self.button_connect,
            "clicked",
            self.find_devices_widget_instance.connect_device,
            device_ip,
            self.detected_devices,
            self.button_connect,
            self.userdata, 
        )
        return self.device_box 
    
    def add_board(self, device_name: str, device_ip: str) -> None:
        """
        Adds a new device board to the device list UI.

        This method utilizes `create_device_board` to generate a new board for 
        the specified device and appends it to the main content layout.

        Parameters
        ----------
        - device_name (`str`): The name of the device to add.
        - device_ip (`str`): The IP address of the device to add.
        """
        self.content_layout.addWidget(
            self.create_device_board(
                device_name,
                device_ip,
            )
        )
        self.content.setLayout(self.content_layout)
    
