from posixpath import splitext
from shutil import move
from os import rename, listdir
from os.path import join
from sys import version 

from PyQt5.QtWidgets import QComboBox, QGridLayout

from Script.Utilities.Utils import add_widget_set
from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Static_Datas import (ERRORS_LIST, EXTRA_ARGS_LIST, 
                                           ARGS_LIST, LAYOUT_POSITIONS)

#get elements for start semi-auto mode
def get_sliders_start(sliders: list, active_checks: list, scrcpy_version: float) -> str:
    """
    Generate arg_line of the `sliders`.

    Parameters
    ----------
    - sliders (`List[QSlider]`): A list of QSlider objects.
    - active_checks list (`List[str]`): A list of active checks.
    - scrcpy_version (`float`): The scrcpy version.
    
    Returns:
    - str: arg_line of the `sliders`.
    """
    args_line = ""
    for index, slider in enumerate(sliders):
        args_line += f" --max-fps {slider.value()}" if index == 0 else ""
        args_line += f" -m {slider.value()}" if index == 1 else ""
        
        if index == 2:
            bitrate_cmd = "--video-bit-rate" if scrcpy_version >= 2.0 else "--bit-rate"
            args_line += f" {bitrate_cmd} {slider.value()}M"
        
        if "video buffer" in active_checks and index == 3:
            args_line += f" --display-buffer {slider.value()}"
        
        if "audio buffer" in active_checks and index == 4 and scrcpy_version >= 2.0:
            args_line += f" --audio-buffer {slider.value()}"

        if "time limit" in active_checks and index == 5 and scrcpy_version >= 2.1:
            args_line += f" --time-limit {slider.value()}"
            
        
    return args_line

def get_line_edit_start(line_edits: list, active_checks: list, record_combox: QComboBox, scrcpy_version: float) -> str:
    """
    Generate arg_line of the `lineEdits`.

    Parameters
    ----------
    - line_edits list (`List[QLineEdit]`): A list of QLineEdit objects.
    - active_checks list (`List[str]`): A list of active checks.
    - record_combox (`QComboBox`): A QComboBox object for the record file name.
    - scrcpy_version (`float`): The scrcpy version.
    
    Returns:
    - str: arg_line of the `lineEdits`.
    """
    args_line = ""
    for index, lineedit in enumerate(line_edits):
            if "crop" in active_checks and index == 1:
                args_line += f" --crop {lineedit.text()}"
                
            if "record" in active_checks and index == 0:
                file_name = lineedit.text() or "video"
                extension_file = record_combox.currentText()
                extension_file = "mp4" if extension_file in ["opus", "aac"] \
                    and scrcpy_version < 2.1 else extension_file
                
                if extension_file  in ["opus", "aac"] and scrcpy_version >= 2.1:
                    args_line += f" --audio-codec={extension_file}"
                
                args_line += f" --record {file_name}.{extension_file}"
                        
    return args_line
            
def get_combo_box_start(combo_boxs: list, scrcpy_version: float) -> str:
    """
    Generate arg_line of the `comboBoxs` selections.

    Parameters
    ----------
    - combo_boxs (`List[QComboBox]`): A list of QComboBox objects.

    Returns:
    - str: arg_line of the `comboboxs`.
    """
    args_line = ""
    combo_boxs_texts = [combo_box.currentText() for combo_box in combo_boxs[1:]]
    for dict_name in EXTRA_ARGS_LIST:
        version_dict = EXTRA_ARGS_LIST[dict_name]
        if dict_name == "all_version":
            args_line += "".join(version_dict[combo_text] for combo_text in combo_boxs_texts \
                if combo_text in version_dict.keys())
            
        elif dict_name == "deprecated_args":
            for limits in version_dict.keys():
                if scrcpy_version <= (limit_dict := version_dict[limits])["Version"]:
                    args_line = "".join(limit_dict[combo_text] for combo_text in combo_boxs_texts \
                        if combo_text in limit_dict.keys())
        
        elif scrcpy_version >= version_dict["Version"]:
            args_line += "".join(version_dict[combo_text] for combo_text in combo_boxs_texts \
                if combo_text in version_dict.keys())
                
    return args_line

def get_checkBox_start(active_checks: list, args_w_required_values: list, scrcpy_version: float) -> tuple:
    """
    Generate arg_line of the checkBox.

    Parameters
    ----------
    - active_checks (`list`): A list of active checks.
    - require_values (`list`): A list of values that are required.

    Returns
    -------
    - `tuple`: A tuple containing the arg_line and the hide_client value.
    """
    args_line = ""
    active_checks = [check for check in active_checks if check not in args_w_required_values]
    for dict_name in ARGS_LIST.keys():
        version_dict = ARGS_LIST[dict_name]
        if dict_name == "all_version":
            args_line += "".join(version_dict[active_check] for active_check in active_checks \
                if active_check in version_dict.keys())
        else:
            if scrcpy_version >= version_dict["Version"]:
                args_line += "".join(version_dict[active_check] for active_check in active_checks \
                    if active_check in version_dict.keys())

    hide_client = any("hide client" in check for check in active_checks)   
    return args_line, hide_client
    
#move saved video from --record (-r)
def move_record_file(record_file: str, path: str, target_path: str, custom_dir_enabled: bool) -> None:
    """
    This function moves the saved `video file` from the `--record` (`-r`) argument to the target path.
    
    Parameters
    ----------
    - record_file (`str`): The name of the saved video file.
    - path (`str`): The path where the saved video file is located.
    - target_path (`str`): The path where the saved video file will be moved.
    - custom_dir_enabled (`bool`): Whether the custom directory is enabled.
    """
    if record_file:
        if custom_dir_enabled:
            try:
                files = [file.lower() for file in listdir(target_path)]
                old_path = join(path, record_file)
                index = 0
                while True:
                    name_extension = splitext(record_file.lower())
                    new_file_name = f"{name_extension[0]}_{index}{name_extension[1]}"
                    if new_file_name not in files:
                        rename(old_path, join(path, new_file_name))
                        old_path = join(path, new_file_name) 
                        break
                    else:
                        index += 1
                    
                move(old_path, target_path)

            except (FileNotFoundError, TypeError):
                create_alert(
                    "Directory Not Found",
                    ("The target path was not found, make sure it is correct\n"
                    "the file was left in the initial folder"),
                )
            else:
                create_alert(
                    "SUCCESSFUL",
                    ("The file has been saved to the selected " 
                    "destination folder successfully!"),
                )
        else:
            create_alert(
                "SUCCESSFUL",
                "The saved file was left in the Scrcpy version directory",
            )

#Errors for start_scrcpy
def arguments_errors(err_out: list) -> bool:
    """
    This function checks if there are any `argument errors` and creates an alert if there are any.
    
    Parameters
    ----------
    - err_out (`list`): A list of errors.
    
    Returns
    -------
    - `bool`: `True` if there are no errors, `False` otherwise.
    """
    error_detect = True
    if any(error in err_out for error in ERRORS_LIST["args_unexpected"]):
        create_alert(
            "Arguments Unexpected",
            ("You provided an invalid arg, check that the arg used is\n" 
            "compatible with the version of scrcpy used, and try again"),
        )
        
    elif any(error in err_out for error in ERRORS_LIST["value_error"]):
        create_alert(
            "Values Error",
            ("Not all values for the required arguments were " 
            "provided or invalid values were provided\n"
            "\t\t Check the commands (like --crop) and try again.")
        )
    
    elif "nothing to do" in err_out:
        create_alert(
            "Values Error",
            ("Nothing is being used <Video | Audio | OTG> "
            "in other words nothing to do\ncheck everything "
            "is correct and try again"),
        )
        
    elif "no format specified" in err_out:
        create_alert(
            "Nothing To Do",
            ("The format chosen for '--record' is not valid or "
            "has not been set\nchoose a valid one (.mp4 | .mkv) "
            "and try again"),
            )
    elif "only work in otg mode" in err_out:
        create_alert(
            "OTG Arg",
            ("to use arg (--hid-keyboard | '--hid-mouse')\n" 
            "you need to use the argument (--otg)"),
        )
    elif "audio container does not support video stream" in err_out:
        create_alert(
            "Audio Container",
            ("The selected audio container does not support the video stream\n"
            "use --no-video and try again"),
        )
        
    elif "camera options are only available with --video-source=camera" in err_out:
        create_alert(
            "Camera Options",
            "Camera options are only available with --video-source=camera",
        )
    
    elif "could not specify both --camera-size and -m/--max-size" in err_out:
        create_alert(
            "Camera Size",
            "Cannot specify --camera-size and -m/--max-size at the same time.",
        )
    
    elif "could not specify both --camera-id and --camera-facing" in err_out:
        create_alert(
            "Camera ID",
            "Cannot specify --camera-id and --camera-facing at the same time.",
        )
    elif "otg mode (--otg) is not supported on this platform" in err_out:
        create_alert(
            "Not Supported",
            ("The otg mode (--otg) is not supported on this platform, this version only allows it on Linux"
            "try updating the version of Scrcpy "),
        )
    elif "otg mode (--otg) is disabled" in err_out:
        create_alert(
            "Otg Mode Disabled",
            "OTG mode (--otg) has been disabled, to fix this problem try updating the version of scrcpy" 
        )
    else:
        error_detect = False
    
    print(err_out)
    return error_detect
    
def device_errors(err_out: list) -> bool:
    """
    This function checks if there are any `device errors` and creates an alert if there are any.
    
    Parameters
    ----------
    - err_out (`list`): The list of error messages.
    
    Returns
    -------
    - `bool`: `True` if there are no errors, `False` otherwise.
    """
    error_detect = True
    if any(error in err_out for error in ERRORS_LIST["device_not_found"]):
        create_alert(
            "Nothing Detected",
            ("No device was detected connect a device (Wi-Fi | USB)\n" 
            "and try again"),
        )
    elif "not find any usb device" in err_out:
        create_alert(
            "USB Device",
            ("You need to connect the device via USB to use OTG " 
            "via Wi-Fi will not work"),
        )
    elif "state=offline" in err_out:
        create_alert(
            "Offline Device",
            ("The selected device is offline try, disconnecting and connecting it "
            "and try again"),
        )
    elif "Encoding Error" in err_out:
        create_alert(
            "Encoding Error",
            ("An encoding error occurred, check that the arguments " 
            "and their values are correct\ncheck that the device "
            "is correctly configured and try again")
        )
    elif "0xfffffff4" in err_out:
        create_alert(
            "Encoding Error",
            ("An 'Encoding' error was detected try changing the video-rate (--video-rate)\n"
            "or the maximum size (-m | --max-size) and try again."),
        ) 
    elif "connection reset by peersab" in err_out:
        create_alert(
            "Connection Reset",
            ("The adb connection has been restarted by Peersab\n" 
            "make sure everything is set up correctly."),
        )
    elif "turn screen off if control is disabled" in err_out:
        create_alert(
            "No Control",
            "Cannot use turn screen off without device control.",
        )
 
    else:
        error_detect = False
    
    return error_detect

def args_combination_errors(err_out: list) -> bool:
    """
    This function checks if there are any args `combination errors` and creates an alert if there are any.
    
    Parameters
    ----------
    - err_out (str): The output of the adb command.
    
    Returns
    -------
    - `bool`: `True` if there are no errors, `False` otherwise.
    """
    error_detect = True
    if "--prefer-text is incompatible with --raw-key-events" in err_out:
        create_alert(
            "Incompatible Args",
            ("The args '--prefer-text' and '--raw-key-events' are not compatible\n"
            "remove one of them and try again."),
        )
    elif "not request to show touches if control is disabled" in err_out:
        create_alert(
            "Incompatible Args",
            ("The args '--show-touches' and '--no-control' are not compatible\n" 
            "remove one of them and try again"),
        )
    elif "not request to stay awake if control is disabled" in err_out:
        create_alert(
            "Incompatible Args",
            ("The args '--stay-awake' and '--no-control' are not compatible\n" 
            "remove one of them and try again"),
        )
    else:
        error_detect = False
    
    return error_detect

#Errors for connection
def connection_errors(emit_tcpip: str, emit_connect: str) -> bool:
    """
    This function checks if there are any `connection errors` and creates an alert if there are any.
    
    Parameters
    ----------
    - emit_tcpip (str): The output of the tcpip command.
    - emit_connect (str): The output of the connect command.
    
    Returns
    -------
    - `bool`: `True` if there are no errors, `False` otherwise.
    """
    error_detect = True
    if "already connected to" in emit_connect:
        create_alert(
            "Already Connected",
            "This IP is already connected",
        )
    elif "no devices/emulators found" in emit_tcpip:
        create_alert(
            "Device Not Found",
            "No device found, check if it is properly connected (USB)",
        )
    elif "invalid port" in emit_tcpip:
        create_alert(
            "Invalid Port",
            "Invalid PORT, make sure the PORT you entered is valid",
        )
    elif "(11001)" in emit_connect:
        create_alert(
            "Not Recognized",
            ("The IP and Port was not recognized check the Port Ip\n" 
            "are correct and try again (11001)"),
        )
    elif "(10060)" in emit_connect:
        create_alert(
            "No Response",
            ("Did not get a response from the connected device to the host\n"
            "check the IP and try again (10060)"),
        )
    elif "(10061)" in emit_connect:
        create_alert(
            "Connection Refused",
            ("The connection was refused by the destination device, "
            "check if it is not already connected to some host\n"
            "\t\tand make sure that the IP and Port are valid (10061)"),
        )
    elif "bad port number" in emit_connect:
        create_alert(
            "Bad Port",
            "One poorly chosen door, please choose another",
        )
    else:
        error_detect = False
    
    return error_detect
        
def assemble_grid_layout(tab_name: str, locate: str, *elements: tuple) -> QGridLayout:
    """
    This function is used to `assemble` the grid layout for the tab. It takes the tab name, 
    location, and elements and returns a `QGridLayout` with the appropriate `positions`.
    
    Parameters
    ----------
    - tab_name (`str`): The name of the tab, either 'connect_tab', 'start_tab' or 'config_tab'.
    - locate (`str`): The location of the elements, either 'upper', 'middle', or 'lower'.
    - elements (`tuple`): The elements to be added to the grid layout.
    
    Returns
    -------
    - `QGridLayout`: A `QGridLayout` with the appropriate `positions`.
    
    Raises
    ------
    - `ValueError`: If the tab name is not valid.
    - `ValueError`: If the location is not valid.
    - `ValueError`: If the number of elements does not match the number of positions.
    - `KeyError`: If the keys are not valid for the chosen location.
    """
    tab_name = tab_name.lower().rstrip().lstrip()
    if tab_name not in ["connect_tab", "start_tab", "config_tab"]:
        raise ValueError("The tab name is not valid. Please use "
                         "'connect_tab', 'start_tab', or 'config_tab'.")
    
    locate =  locate.lower().rstrip().lstrip()
    if locate not in ["upper", "middle", "lower"]:
        raise ValueError("The location is not valid. Please use " 
                         "'upper', 'middle', or 'lower'.")
    try:
        positions = LAYOUT_POSITIONS[tab_name][locate]
    except KeyError:
        raise KeyError("Check that the keys are valid and that the "
                        "chosen location is valid for the tab.")
    else:
        if len(positions) != len(elements):
            raise ValueError("The number of elements does not match the number of positions. "
                             f"pos: {len(positions)} elms: {len(elements)}")
    
        return add_widget_set(list(elements), positions)

#takes the data needed for the UI to work correctly
def get_datas_for_ui(data, data_for: str) -> tuple:
    """
    This function takes the data needed for the `UI` to work correctly.
    
    Parameters
    ----------
    - data (`dict`): A dictionary containing the data.
    - data_for (`str`): The type of data to be retrieved. Must be one of 'connect', 'start', or 'config'.
    
    Returns
    -------
    - `tuple`: A tuple containing the datas.
    
    Raises
    ------
    - `ValueError`: If the data type is not valid.
    - `ValueError`: If the data is not a dictionary.
    """
    if not isinstance(data_for, str):
        raise ValueError("'data_for' must be a string")
    
    if not isinstance(data, dict):
        raise ValueError("'data' must be a dictionary")
    
    data_for = data_for.lower()
    if data_for == "connect":
        ips = data["Connect"]["Custom_Ip_Saved"].keys()
        last_ip_index = data["Last_Session_Config"]["ConnectTAB"]["Ip_Index"]
        last_texts = data["Last_Session_Config"]["ConnectTAB"]["LineEdit_Texts"]
        auto_port = data["Connect"]["Port_Auto"]
        
        return ips, last_ip_index, last_texts, auto_port
        
    elif data_for == "start":
        config_templates = data["Custom_Config_Set"].keys()
        last_checks = data["Last_Session_Config"]["StartTAB"]["Check_Boxes"]
        index_combo = data["Last_Session_Config"]["StartTAB"]["Indexs_Combox"]
        last_texts = data["Last_Session_Config"]["StartTAB"]["LineEdit_Texts"]
        slider_values = data["Last_Session_Config"]["StartTAB"]["Slider_Value"]
        
        return config_templates, last_checks, index_combo, last_texts, slider_values
        
    elif data_for == "config":
        selected_version = data["Versions"]["Selected_Version"]["Path"]
        versions = data["Versions"]["Saved_Versions"]
        resolution = data["Resolutions"]["Saved_Resolution"]
        path_mode = data["File_Path_Config"]["Path_Mode_Radio"]
        last_path_file = data["File_Path_Config"]["Path_selected"]
        directory_name = data["File_Path_Config"]["Saved_Path_Files"].keys()
        combox_index = data["Last_Session_Config"]["ConfigTAB"]["Index_Combox"]
        
        return selected_version, versions, resolution, path_mode,\
               last_path_file, directory_name, combox_index
    else:
        raise ValueError("Please choose a value from these: ['connect', 'start', 'config']")
        
