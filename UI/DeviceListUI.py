from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QWidget, QGroupBox, QVBoxLayout, QGridLayout

from Script.Utilities.Utils import connect_signal
from Script.ConnectTAB_Functions import DeviceList
import Script.Utilities.Create_Elements as Create

class DeviceListUI(QScrollArea):
    """
    This class represents the device list UI.
    
    Parameters
    ----------
    - userdata (`dict`): A dictionary containing the user data.
    - parent (`any`, `optional`): The parent widget. Defaults to None.

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
        self.content = QWidget()
        self.content.setObjectName("FindDevicescontent")
        self.setWidget(self.content)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)
    
    def create_device_board(self, device_name: str, device_ip: str) -> QGroupBox:
        self.device_box = QGroupBox()
        self.board_layout = QGridLayout()
        self.board_layout.setSpacing(2)
        self.device_box.setMinimumSize(411, 120)
        
        self.label_device_name = Create.Label(f"Name: {device_name}", self.device_box)
        self.label_ip = Create.Label(f"IP: {device_ip}", self.device_box)
        self.button_connect = Create.Button("Connect Device", self.device_box, (111, 41))      
        
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
        Add a new board to the device list using `create_device_board`.
        
        Parameters
        ----------
        - device_name (`str`): The name of the device.
        - device_ip (`str`): The IP address of the device.
        """
        self.content_layout.addWidget(
            self.create_device_board(
                device_name,
                device_ip,
            )
        )
        self.content.setLayout(self.content_layout)
    
