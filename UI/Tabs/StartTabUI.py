from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSlider,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QMainWindow,
    QTabWidget
)

from Script.StartTAB_Functions import StartTAB
from Script.Utilities import Create_Elements as Create
from Script.Utilities.Utils import connect_signal
from Script.Utilities.Auxiliary_Funcs import assemble_grid_layout, get_datas_for_ui

class StartTab(QWidget):
    """
    This class is used to create the UI for the Start Tab.
    
    Parameters
    ----------
    - userdata (`dict`): The UserData, where all values will be saved for later access.
    - nconc_btns (`list`): List with all non concurrent buttons {`QPushButton`}.
    - client (`QMainWindow`): The main window of the application.
    - tabs (`QTabWidget`): The tab widget that contains all the tabs.
    """
    def __init__(self, userdata: dict, nconc_btns: list, client: QMainWindow, tabs: QTabWidget):
        super().__init__()
        self.userdata = userdata
        self.non_concurrent_buttons = nconc_btns
        self.client = client
        
        self.create_elements()
        self.assemble_elements()
        self.connect_functions_elements()
        tabs.addTab(self, "Start")
    
    def create_elements(self):
        """
        This function `creates` all the elements of the `Start Tab`.
        """
        config_templates, last_checks, index_combo, last_texts,\
        slider_values = get_datas_for_ui(self.userdata, "start")
        
        orientations = [
            "OFF",
            "Initial Orientation",
            "Vertical Orientation",
            "Upside Down",
            "Horizontal Left",
            "Horizontal Right",
        ]
        otg_type = [
            "OFF",
            "SDK",
            "AoA",
            "uHid",
        ]
        otg_mode = [
            "Mouse",
            "Keyboard",
            "Mouse + Keyboard",
        ]
        file_types = [
            "mp4",
            "mkv",
            "aac",
            "opus",
        ]
        video_sources = [
            "Screen",
            "Back Camera",
            "Front Camera",
            "External Camera",
        ]
        audio_sources = [
            "Device Sound",
            "Microphone",
        ]
        
        self.label_save_config = Create.Label("Save Config", self)
        self.label_custom_start = Create.Label("Custom Start", self)
        self.label_FPS = Create.Label("FPS", self)
        self.label_max_size = Create.Label("Max-Size", self)
        self.label_video_bit = Create.Label("Video-Bit", self)
        self.label_video_buffer = Create.Label("Video-Buffer", self)
        self.label_audio_buffer = Create.Label("Audio-Buffer", self)
        self.label_record = Create.Label("Record File", self)
        self.label_crop_config = Create.Label("Crop Config", self)
        self.label_lock_orientation = Create.Label("Lock Orientation", self)
        self.label_video_source = Create.Label("Video Source", self)
        self.label_audio_source = Create.Label("Audio Source", self)
        self.label_time_limit = Create.Label("Record Time Limit", self)
        self.label_keyboard_mouse = Create.Label("Keyboard & Mouse", self)

        self.combox_presets = Create.Combox(config_templates, self, (145, 22), index_combo[0])
        self.combox_record_file_type = Create.Combox(file_types, self, (51, 22), index_combo[1])
        self.combox_orientation_config = Create.Combox(orientations, self, (191, 22), index_combo[2])
        self.combox_video_source = Create.Combox(video_sources, self, (191, 22), index_combo[3])
        self.combox_audio_source = Create.Combox(audio_sources, self, (191, 22), index_combo[4])
        self.combox_OTG_type = Create.Combox(otg_type, self, (191, 22), index_combo[5])
        self.combox_OTG_mode = Create.Combox(otg_mode, self, (191, 22), index_combo[6])
        
        self.text_custom_start = Create.LineEdit("Custom Config... *JUST ARGS*", self, (301, 20), last_texts[0])
        self.text_record_file_name = Create.LineEdit("File Name...", self, (111, 20), last_texts[1], r"\S+")
        self.text_crop_config = Create.LineEdit("width:height:x:y", self, (192, 20), last_texts[2], "^[0-9:]*$")
        
        self.line_FPS = Create.LineEdit("FPS", self, (80, 20), slider_values[0], "[0-9]*$", "ValuesLines")
        self.line_max_size = Create.LineEdit("MAX-SIZE", self, (80, 20), slider_values[1], "[0-9]*$", "ValuesLines")
        self.line_video_bit = Create.LineEdit("VIDEO-BIT", self, (80, 20), slider_values[2], "[0-9]*$", "ValuesLines")
        self.line_video_buffer = Create.LineEdit("VIDEO-BUFFER", self, (80, 20), slider_values[3], "[0-9]*$", "ValuesLines")
        self.line_audio_buffer = Create.LineEdit("AUDIO-BUFFER", self, (80, 20), slider_values[4], "[0-9]*$", "ValuesLines")
        self.line_time_limit = Create.LineEdit("TIME-LIMIT (s)", self, (80, 20), slider_values[5], "[0-9]*$", "ValuesLines")
        
        self.slider_FPS = Create.Slider(self, 5, 65535, 5, slider_values[0], (151, 21))
        self.slider_max_size = Create.Slider(self, 500, 65535, 100, slider_values[1], (151, 21))
        self.slider_video_bit = Create.Slider(self, 1, 2147, 5, slider_values[2], (151, 21))
        self.slider_video_buffer = Create.Slider(self, 0, 10000, 10, slider_values[3], (151, 21))
        self.slider_audio_buffer = Create.Slider(self, 0, 10000, 10, slider_values[4], (151, 21))
        self.slider_time_limit = Create.Slider(self, 0, 1000, 30, slider_values[5], (151, 21))

        self.button_load = Create.Button("Load", self, (145, 23))
        self.button_start_custom = Create.Button("Start Custom", self, (301, 23))
        self.button_delete = Create.Button("Delete", self, (71, 23))
        self.button_save = Create.Button("Save", self, (71, 23))
        self.button_start = Create.Button("Start", self, (510, 27))
        self.button_default_config = Create.Button("\U0001F504", self, (20, 20), "Default_Config_Button")
        self.button_shell_button = Create.Button("\U0001F4BB", self, (20, 20), "Shell_Button")
        self.button_default_config.setMaximumSize(20, 20)
        self.button_shell_button.setMaximumSize(20, 20)
        
        self.check_record = Create.CheckBox("Record", self, (61, 18), last_checks[0])
        self.check_time_limit = Create.CheckBox("Time Limit", self, (91,  18), last_checks[1])
        self.check_prefer_text = Create.CheckBox("Prefer Text", self, (81, 20), last_checks[2])
        self.check_no_k_repeat = Create.CheckBox("No K Repeat", self, (91, 20), last_checks[3])
        self.check_raw_k_events = Create.CheckBox("Raw K Events", self, (101, 20), last_checks[4])
        self.check_fwd_all_clicks = Create.CheckBox("Fwd All Clicks", self, (91, 20), last_checks[5])
        self.check_no_playback = Create.CheckBox("No Playback", self, (101, 18), last_checks[6])
        self.check_video_buffer = Create.CheckBox("Video Buffer", self, (91,  18), last_checks[7])
        self.check_audio_buffer = Create.CheckBox("Audio Buffer", self, (91,  18), last_checks[8])
        self.check_no_audio = Create.CheckBox("No Audio", self, (91,  18), last_checks[9])
        self.check_no_video = Create.CheckBox("No Video", self, (91,  18), last_checks[10])
        self.check_crop = Create.CheckBox("Crop", self, (51, 20), last_checks[11])
        self.check_ctrl_shortcut = Create.CheckBox("Ctrl sct", self, (111, 18), last_checks[12])
        self.check_show_touches = Create.CheckBox("Show Touches", self, (101, 18), last_checks[13])
        self.check_hide_client = Create.CheckBox("Hide Client", self, (81, 18), last_checks[14])
        self.check_no_control = Create.CheckBox("No Control", self, (81, 18), last_checks[15])
        self.check_fullscreen = Create.CheckBox("Fullscreen", self, (71, 18), last_checks[16])
        self.check_alt_ctrl_shortcut = Create.CheckBox("Alt-Ctrl sct", self, (111, 18), last_checks[17])
        self.check_always_on_top = Create.CheckBox("Always on Top", self, (101, 18), last_checks[18])
        self.check_stay_awake = Create.CheckBox("Stay Awake", self, (81, 18), last_checks[19])
        self.check_screen_off = Create.CheckBox("Screen Off", self, (81, 18), last_checks[20])
        self.check_borderless = Create.CheckBox("Borderless", self, (71, 18), last_checks[21])
        
    def assemble_elements(self):
        """
        This function `assembles` all the elements into a `grid layout`.
        """
        upper_layout = assemble_grid_layout(
            "start_tab",
            "upper",
            self.label_save_config,
            self.button_default_config,
            self.label_custom_start,
            self.combox_presets,
            self.button_load,
            self.button_delete,
            self.button_save,
            self.button_shell_button,
            self.text_custom_start,
            self.button_start_custom,
        )
        middle_layout = assemble_grid_layout(
            "start_tab",
            "middle",
            self.line_FPS,
            self.label_FPS,
            self.slider_FPS,
            self.line_max_size,
            self.label_max_size,
            self.slider_max_size,
            self.line_video_bit,
            self.label_video_bit,
            self.slider_video_bit,
            self.line_video_buffer,
            self.label_video_buffer,
            self.slider_video_buffer,
            self.line_audio_buffer,
            self.label_audio_buffer,
            self.slider_audio_buffer,
            self.check_record,
            self.label_record,
            self.text_record_file_name,
            self.combox_record_file_type,
            self.label_crop_config,
            self.text_crop_config,
            self.label_lock_orientation,
            self.combox_orientation_config,
            self.label_video_source,
            self.combox_video_source,
            self.label_audio_source,
            self.combox_audio_source,
            self.label_keyboard_mouse,
            self.combox_OTG_type,
            self.combox_OTG_mode,
            self.label_time_limit,
            self.line_time_limit,
            self.slider_time_limit,
            self.check_time_limit,
        )
        lower_layout = assemble_grid_layout(
            "start_tab",
            "lower",
            self.check_prefer_text,
            self.check_no_k_repeat,
            self.check_raw_k_events,
            self.check_fwd_all_clicks,
            self.check_no_playback,
            self.check_video_buffer,
            self.check_audio_buffer,
            self.check_no_audio,
            self.check_no_video,
            self.check_crop,
            self.check_ctrl_shortcut,
            self.check_show_touches,
            self.check_hide_client,
            self.check_no_control,
            self.check_fullscreen,
            self.check_alt_ctrl_shortcut,
            self.check_always_on_top,
            self.check_stay_awake,
            self.check_screen_off,
            self.check_borderless,
            self.button_start,
        )
        
        middle_content = QWidget()
        lower_content = QWidget()
        main_layout = QVBoxLayout()
        
        middle_layout.setColumnStretch(1, 2)
        middle_layout.setColumnStretch(4, 2)
        middle_layout.setHorizontalSpacing(5)
        middle_layout.setAlignment(Qt.AlignTop)
        
        upper_content = QWidget()
        upper_content.setLayout(upper_layout)
        middle_content.setLayout(middle_layout)
        lower_content.setLayout(lower_layout)
        
        main_layout.addWidget(upper_content)
        main_layout.addWidget(middle_content)
        main_layout.addWidget(lower_content)
        
        self.setLayout(main_layout)
        
    def connect_functions_elements(self):
        """
        This function `connects` the functions to the `elements`.
        """
        self.non_concurrent_buttons.extend(
            [   
            self.button_start, 
            self.button_start_custom
            ]
        )     
        line_edit_value = [
            self.line_FPS,
            self.line_max_size,
            self.line_video_bit,
            self.line_video_buffer,
            self.line_audio_buffer,
            self.line_time_limit,
        ]
        sliders = self.findChildren(QSlider) 
        check_boxs = self.findChildren(QCheckBox) 
        combo_boxs = self.findChildren(QComboBox)
        line_edits = self.findChildren(QLineEdit) 
        line_edits = list(filter(lambda x: x not in line_edit_value, line_edits))
        
        start_tab_instance = StartTAB()
        for index, value_edit in enumerate(line_edit_value):            
            connect_signal(
                value_edit,
                "textChanged",
                start_tab_instance.value_edit_charge_event,
                value_edit,
                sliders[index],
            )
        
        for index, check_box in enumerate(check_boxs):
            connect_signal(
                check_box,
                "stateChanged",
                start_tab_instance.last_check_selected,
                index,
                self.userdata["Last_Session_Config"]["StartTAB"],
            )
        
        for index, combo_box in enumerate(combo_boxs):
            connect_signal(
                combo_box,
                "currentIndexChanged",
                start_tab_instance.last_index,
                combo_box,
                index,
            )
        
        for index, line_edit in enumerate(line_edits):
            connect_signal(
                line_edit,
                "textChanged",
                start_tab_instance.last_texts,
                line_edit,
                index,
            )
         
        for index, slider in enumerate(sliders):
            connect_signal(
                slider,
                "valueChanged",
                start_tab_instance.slider_charge_event,
                slider,
                line_edit_value[index],
                index,
                self.userdata["Last_Session_Config"]["StartTAB"]
            )
       
        connect_signal(
            self.button_default_config,
            "clicked",
            start_tab_instance.back_to_default_config,
            check_boxs,
            line_edits,
            combo_boxs,
            sliders,
        )
        
        connect_signal(
            self.button_load,
            "clicked",
            start_tab_instance.load_saved_config,
            self.combox_presets,
            check_boxs,
            line_edits,
            combo_boxs,
            sliders,
            self.userdata["Custom_Config_Set"],
        )
        
        connect_signal(
            self.button_delete,
            "clicked",
            start_tab_instance.delete_saved_config,
            self.combox_presets,
            self.userdata["Custom_Config_Set"],
        )

        connect_signal(
            self.button_save,
            "clicked",
            start_tab_instance.save_custom_config,
            self.combox_presets,
            check_boxs,
            line_edits,
            combo_boxs,
            sliders,
            self.userdata["Custom_Config_Set"],
        )
        
        connect_signal(
            self.button_start_custom,
            "clicked",
            start_tab_instance.line_arg_start_scrcpy,
            self.text_custom_start,
            self.userdata,
        )
        
        connect_signal(
            self.button_shell_button,
            "clicked",
            start_tab_instance.open_shell,
            self.userdata,
        )
        
        connect_signal(
            self.button_start,
            "clicked",
            start_tab_instance.ui_start_scrcpy,
            sliders,
            check_boxs,
            combo_boxs[1:],
            line_edits[1:],
            self.userdata,
            self.client,
        )

        
