from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QTabWidget

from UI.DeviceListUI import DeviceListUI
from Script.ConnectTAB_Functions import ConnectTAB, DeviceList
from Script.Utilities.Utils import connect_signal
from Script.Utilities import Create_Elements as Create
from Script.Utilities.Auxiliary_Funcs import assemble_grid_layout, get_datas_for_ui

class ConnectTab(QWidget):
    """
    Represents the connection tab UI in the application.

    This class is responsible for creating and managing the user interface (UI) elements 
    within the "Connect" tab. It provides functionality for setting up the configuration data, 
    handling user inputs, and interacting with other components of the application such as 
    buttons and the main window. The `ConnectTab` is added to a `QTabWidget` to make it a part 
    of the main application's tab-based interface.

    Parameters
    ----------
    - userdata (`dict`): The dictionary containing user-specific data, which is used 
    to populate the connection fields.
    - nconc_btns (`list`): A list of buttons that are non-concurrent, i.e., buttons that 
    should not be pressed simultaneously, which are toggled during various actions.
    - tabs (`QTabWidget`): The `QTabWidget` that holds all the tabs in the application, to which 
    this connection tab will be added.
    """
    def __init__(self, userdata: dict, nconc_btns: list, tabs: QTabWidget):
        super().__init__()
        self.userdata = userdata
        self.non_concurrent_buttons = nconc_btns
        
        self.create_elements()
        self.assemble_elements()
        self.connect_functions_elements()
        tabs.addTab(self, "Connect")

    def create_elements(self):
        """
        Creates and initializes all the UI elements for the `Connect Tab`.

        This method is responsible for setting up the widgets and controls that will be displayed 
        in the "Connect" tab. These include labels, combo boxes, line edits, and buttons, which 
        allow the user to configure various aspects of the application. The method also retrieves 
        necessary data for populating these elements from the `userdata` dictionary.
        """
        ips, last_ip_index, last_texts, auto_port = get_datas_for_ui(self.userdata, "connect")
        
        self.label_manual_connect = Create.Label("Manual Connection", self)
        self.label_auto_connect = Create.Label("Auto Connection", self)
        
        self.combox_saved_ips = Create.Combox(ips, self, index=last_ip_index)
        self.combox_saved_ips.setFocusPolicy(Qt.NoFocus)
        
        self.text_ip = Create.LineEdit("Custom IP Address...", initial_text=last_texts[0], input_filter="^[0-9A-Fa-f:.]+$")
        self.text_port = Create.LineEdit("Port...", initial_text=last_texts[1], input_filter="^[0-9]*$")
        self.text_port_auto = Create.LineEdit("Port...", self, (201, 20), auto_port, "^[0-9]*$")
        
        self.button_connect = Create.Button("Connect", self, (50, 24))
        self.button_save_custom = Create.Button("Save", self, (50, 24))
        self.button_delete_custom = Create.Button("Delete", self, (50, 24))
        self.button_connect_textline = Create.Button("Connect Text Line", self, (50, 24))
        self.button_disconnect = Create.Button("Disconnect", self, (50, 24))
        self.button_wifi_debug = Create.Button("Wifi Debug", self, (50, 24))
        self.button_detect_devices = Create.Button("Detect Devices", self, (200, 24))
        
        self.DeviceL = DeviceListUI(self.userdata)
        
    def assemble_elements(self):
        """
        Assembles all the UI elements into a grid layout for the `Connect Tab`.

        This method arranges and organizes the previously created UI elements into a layout 
        structure. It splits the UI into an upper and lower section, each containing related 
        widgets. The elements are then added to the layout using grid-based positioning. 
        Additionally, spacers are inserted at specific positions to improve the overall layout 
        structure.
        """
        upper_layout = assemble_grid_layout(
            "connect_tab",
            "upper",
            self.label_manual_connect,
            self.combox_saved_ips,
            self.text_ip,
            self.button_connect,
            self.text_port,
            self.button_save_custom,
            self.button_delete_custom,
            self.button_connect_textline,
            self.button_disconnect,
            self.button_wifi_debug,
            self.label_auto_connect,
            self.button_detect_devices,
        )
        lower_layout = assemble_grid_layout(
            "connect_tab",
            "lower",
            self.DeviceL,
            self.text_port_auto,
        )
        
        upper_content = QWidget()
        lower_content = QWidget()
        main_layout  = QGridLayout()
        
        main_layout.addWidget(upper_content, 0, 0, Qt.AlignTop)
        main_layout.addWidget(lower_content, 1, 0)
        
        upper_content.setLayout(upper_layout)
        lower_content.setLayout(lower_layout)
        self.setLayout(main_layout)
        
    def connect_functions_elements(self):
        """
        Connects the UI elements to their respective functions in the `ConnectTAB`.

        This method establishes the necessary signal-slot connections for the UI elements in the 
        `ConnectTAB` to ensure user interactions trigger the appropriate actions. Signals (such as 
        `textChanged` and `clicked`) are connected to the corresponding functions that handle these 
        events.

        The method also extends the `non_concurrent_buttons` list with specific buttons that should 
        be handled separately in the layout.

        Notes
        -----
        - This method relies on the `connect_signal` utility function to connect the UI elements' 
        signals to the appropriate functions.
        """
        self.non_concurrent_buttons.extend(
            [
            self.button_connect, 
            self.button_disconnect,
            self.button_wifi_debug,
            self.button_connect_textline,
            self.button_detect_devices,
            ]
        )     
        connect_tab_instance = ConnectTAB()
        for index, line_edit in enumerate([self.text_ip, self.text_port]):
            connect_signal(
                line_edit,
                "textChanged",
                connect_tab_instance.last_text_infos,
                line_edit,
                index,
            )
        
        connect_signal(
            self.combox_saved_ips,
            "currentIndexChanged",
            connect_tab_instance.last_ip_selected, 
            self.combox_saved_ips,
        )
        
        connect_signal(
            self.button_connect,
            "clicked",
            connect_tab_instance.connect_to_saved,
            self.non_concurrent_buttons,
            self.combox_saved_ips,
            self.userdata,
        )
        
        connect_signal(
            self.button_connect_textline,
            "clicked",
            connect_tab_instance.connect_to_line_edit,
            self.non_concurrent_buttons,
            [self.text_ip, self.text_port],
            self.userdata,
        )
        
        connect_signal(
            self.button_wifi_debug,
            "clicked",
            connect_tab_instance.connect_wifi_debug,
            self.non_concurrent_buttons,
            [self.text_ip, self.text_port],
            self.userdata,
        )
        
        connect_signal(
            self.button_save_custom,
            "clicked",
            connect_tab_instance.save_custom_connection,
            self.combox_saved_ips,
            [self.text_ip, self.text_port],
            self.userdata["Connect"]["Custom_Ip_Saved"]
            )
        
        connect_signal(
            self.button_delete_custom,
            "clicked",
            connect_tab_instance.delete_custom_connection,
            self.combox_saved_ips,
            self.userdata["Connect"]["Custom_Ip_Saved"],
        )
        
        connect_signal(
            self.button_disconnect,
            "clicked",
            connect_tab_instance.disconnect_device,
            self.non_concurrent_buttons,
            self.userdata,
        )

        find_devices_instance = DeviceList()
        connect_signal(
            self.button_detect_devices,
            "clicked",
            find_devices_instance.detect_devices,
            self.non_concurrent_buttons,
            self.DeviceL,
            self.userdata["Versions"],
        )
        
        connect_signal(
            self.text_port_auto,
            "textChanged", 
            find_devices_instance.save_ui_port,
            self.text_port_auto,
            self.userdata["Connect"],
        )
