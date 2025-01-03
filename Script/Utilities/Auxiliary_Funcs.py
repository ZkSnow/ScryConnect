from posixpath import splitext
from shutil import move
from os import rename, listdir
from os.path import join

from PyQt5.QtWidgets import QComboBox, QGridLayout

from Script.Utilities.Utils import add_widget_set
from Script.Utilities.Create_Alerts import create_alert
from Script.Utilities.Static_Datas import (ERRORS_LIST, EXTRA_ARGS_LIST, 
                                           ARGS_LIST, LAYOUT_POSITIONS)

#get elements for start semi-auto mode
def get_sliders_start(sliders: list, active_checks: list, scrcpy_version: float) -> str:
    """
    Generates the argument line for configuring `sliders` based on their values and associated conditions.

    This function builds a command-line argument string (`arg_line`) for the `sliders`, which can be 
    used in the context of configuring settings for a `scrcpy` application. The function takes the 
    values of the sliders and optionally includes different settings based on the version of `scrcpy` 
    and the active checks.

    Parameters
    ----------
    - sliders (`List[QSlider]`): A list of `QSlider` objects representing various configuration options.
    - active_checks (`List[str]`): A list of active checks, which are conditions that influence the 
      command-line arguments (e.g., "video buffer", "audio buffer", "time limit").
    - scrcpy_version (`float`): The version of `scrcpy` being used. The argument format may vary depending 
      on the version (e.g., bitrate or video buffer options).

    Returns
    -------
    - `str`: The generated command-line argument string (`arg_line`) based on the slider values and active checks.
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
    Generates the argument line for configuring `lineEdits` based on their values and associated conditions.

    This function builds a command-line argument string (`arg_line`) for the `lineEdits`, which can be 
    used in the context of configuring settings for a `scrcpy` application. The function checks the values 
    of the `lineEdits` and optionally includes different settings based on the active checks and the version of 
    `scrcpy`.

    Parameters
    ----------
    - line_edits (`List[QLineEdit]`): A list of `QLineEdit` objects representing various configuration options.
    - active_checks (`List[str]`): A list of active checks that influence the command-line arguments (e.g., "record", "crop").
    - record_combox (`QComboBox`): A `QComboBox` object used to select the recording file format (e.g., "mp4", "opus", "aac").
    - scrcpy_version (`float`): The version of `scrcpy` being used. The argument format may vary depending on the version (e.g., audio codec options, recording format).

    Returns
    -------
    - `str`: The generated command-line argument string (`arg_line`) based on the `lineEdits` and active checks.
"""
    args_line = ""
    for index, lineedit in enumerate(line_edits):
        if "record" in active_checks and index == 0:
            extension_file = record_combox.currentText()
            extension_file = "mp4" if extension_file in ["opus", "aac"] \
                and scrcpy_version < 2.1 else extension_file

            if extension_file  in ["opus", "aac"] and scrcpy_version >= 2.1:
                args_line += f" --audio-codec={extension_file}"
            args_line += f" --record {lineedit.text() or 'video'}.{extension_file}"
        
        if "mouse binding" in active_checks and index == 1 and scrcpy_version >= 2.5:
            args_line += f" --mouse-bind={lineedit.text()}"
            
        if "crop" in active_checks and index == 2:
            args_line += f" --crop {lineedit.text()}"

    return args_line

def get_combo_box_start(combo_boxs: list, scrcpy_version: float) -> str:
    """
    Generates the argument line for the selections in the `comboBoxs`.

    This function constructs a command-line argument string (`arg_line`) based on the selected values in the 
    provided `QComboBox` objects. It uses predefined arguments stored in `EXTRA_ARGS_LIST` to adjust the command 
    according to the selected options and the version of `scrcpy`.

    Parameters
    ----------
    - combo_boxs (`List[QComboBox]`): A list of `QComboBox` objects representing different configuration options.
    - scrcpy_version (`float`): The version of `scrcpy`. The argument format may vary depending on the version.

    Returns
    -------
    - `str`: The generated command-line argument string (`arg_line`) based on the selections in the `comboBoxs`.

    Notes
    -----
    - The function collects the selected texts from all `QComboBox` objects, except for the first one.
    - The selected values are then matched against predefined arguments stored in `EXTRA_ARGS_LIST`.
    - The `EXTRA_ARGS_LIST` is assumed to contain version-specific argument mappings, which may vary depending on the `scrcpy_version` and the selected values from the combo boxes.
    - If `scrcpy_version` is lower than certain specified limits, deprecated or older arguments may be included.
    - The function combines multiple selections in the last two combo boxes into a single key for argument construction.
    - The generated argument line will include different settings for specific `scrcpy_version` values.
    """
    args_line = ""
    combo_boxs_texts = [combo_box.currentText() for combo_box in combo_boxs[1:]]
    key_mouse = " ".join(combo_boxs_texts[-2:])

    for dict_name in EXTRA_ARGS_LIST:
        version_dict = EXTRA_ARGS_LIST[dict_name]
        if dict_name == "all_version":
            args_line += "".join(
                version_dict.get(combo_text, "") for combo_text in combo_boxs_texts
            )
            args_line += "".join(
                version_dict.get(key_mouse, "")
            )
        elif dict_name == "deprecated_args":
            for limits in version_dict.keys():
                if scrcpy_version <= (limit_dict := version_dict[limits])["Version"]:
                    args_line = "".join(
                        limit_dict.get(combo_text, "") for combo_text in combo_boxs_texts 
                    )
        elif scrcpy_version >= version_dict["Version"]:
            args_line += "".join(
                version_dict.get(combo_text, "") for combo_text in combo_boxs_texts
            )
    return args_line

def get_checkBox_start(active_checks: list, args_w_required_values: list, scrcpy_version: float) -> tuple:
    """
    Generates the argument line for the selected checkboxes.

    This function constructs a command-line argument string (`arg_line`) based on the active checks in the 
    provided list. It checks the selected options against predefined arguments stored in `ARGS_LIST` and 
    adjusts the generated arguments according to the version of `scrcpy`.

    Parameters
    ----------
    - active_checks (`list`): A list of active checks (strings) representing the options selected by the user.
    - args_w_required_values (`list`): A list of argument names that require additional values. These will be excluded from `active_checks`.
    - scrcpy_version (`float`): The version of `scrcpy`. The argument format may vary depending on the version.

    Returns
    -------
    - `tuple`: A tuple containing:
      - `arg_line` (`str`): The generated command-line argument string based on the active checkboxes.
      - `hide_client` (`bool`): A flag indicating whether the "hide client" option is selected.

    Notes
    -----
    - The function filters out `active_checks` that match entries in `args_w_required_values`, ensuring only the options
    that don't require additional values are included.
    - The function uses the predefined `ARGS_LIST` to generate the argument string. The `ARGS_LIST` is assumed to contain 
    version-specific argument mappings for different `scrcpy_version` values.
    - If `scrcpy_version` is greater than or equal to the version specified in `ARGS_LIST`, the corresponding arguments 
    are included in the `arg_line`.
    - The function also checks if the "hide client" option is selected, and returns a `True` or `False` value for that.
    """
    args_line = ""
    active_checks = [check for check in active_checks if check not in args_w_required_values]
    for dict_name in ARGS_LIST.keys():
        version_dict = ARGS_LIST[dict_name]
        if dict_name == "all_version":
            args_line += "".join(
                version_dict.get(active_check, "") for active_check in active_checks
            )
        else:
            if scrcpy_version >= version_dict["Version"]:
                args_line += "".join(
                    version_dict.get(active_check, "") for active_check in active_checks
                )
    return args_line, "hide client" in active_checks 
    
#move saved video from --record (-r)
def move_record_file(record_file: str, path: str, target_path: str, custom_dir_enabled: bool) -> None:
    """
    Moves a saved video file to the target directory.

    This function moves a recorded video file (created using the `--record` argument) from its original path 
    to a target destination. If a custom directory is enabled, the file is renamed to avoid conflicts 
    with existing files in the target directory.

    Parameters
    ----------
    - record_file (`str`): The name of the saved video file (e.g., "video.mp4").
    - path (`str`): The current path where the video file is located (before moving).
    - target_path (`str`): The target path where the video file should be moved.
    - custom_dir_enabled (`bool`): A flag indicating whether a custom directory is enabled for saving the file. 
    If `True`, the file is renamed if a file with the same name exists in the target directory.
    
    Raises
    ------
    - `FileNotFoundError`: If the target directory is not found.
    - `TypeError`: If there is an issue with the file or path provided.

    Notes
    -----
    - If `custom_dir_enabled` is `True`, the function checks the target directory for existing files with the same name. 
    If a conflict is detected, it renames the file by appending an index (e.g., `video_1.mp4`) until it finds a unique name.
    - If `custom_dir_enabled` is `False`, the file is moved without renaming, and a success alert is shown.
    - If any error occurs during the process (such as a missing target directory), an alert is shown to the user.
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
                    "the file was left in the scrcpy folder"),
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
    Checks for argument errors and creates alerts for specific error conditions.

    This function examines the provided list of errors (`err_out`) and checks for specific conditions 
    related to argument errors. Depending on the type of error, it will show an appropriate alert 
    message to the user. The function handles various types of errors, including unexpected arguments, 
    value errors, and issues related to specific scrcpy options.

    Parameters
    ----------
    - err_out (`list`): A list of error messages or strings returned from a command execution. 
    This list is checked against predefined sets of known errors to identify any issues.

    Returns
    -------
    - `bool`: Returns `True` if no errors are found (meaning the arguments are valid). 
    Returns `False` if any recognized error is detected and an alert is triggered.
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
            ("Camera options are only available with --video-source=camera"
            "\n(This can also be caused by the '--crop' argument)")
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
    elif "invalid mouse bindings" in err_out:
        create_alert(
            "Mouse Bindings",
            ("Mouse bindings are invalid, mouse binding can have a maximum of 4 characters"
            "\nand using any of these characters: '+', '-', 'b', 'h', 's', 'n'.")           
        )
    elif "could not retrieve device information" in err_out:
        create_alert(
            "Args Error",
            "Could not retrieve device information, try changing the arguments",
        )
    elif "--no-mouse-over is specific to --mouse=sdk" in err_out:
        create_alert(
            "No Mouse Over",
            "The --no-mouse-over option is specific to --mouse=sdk",
        )
    elif "--no-key-repeat is specific to --keyboard=sdk" in err_out:
        create_alert(
            "No Key Repeat",
            "The --no-key-repeat option is specific to --keyboard=sdk",
        )
    elif "--prefer-text is specific to --keyboard=sdk" in err_out:
        create_alert(
            "Prefer Text",
            "The --prefer-text option is specific to --keyboard=sdk",
        )
    elif "--raw-key-events is specific to --keyboard=sdk" in err_out:
        create_alert(
            "Raw Key Events",
            "The --raw-key-events option is specific to --keyboard=sdk",
        )
    else: 
        error_detect = False
    print(err_out)
    return error_detect
    
def device_errors(err_out: list) -> bool:
    """
    Checks for device errors and creates alerts for specific error conditions.

    This function checks the provided list of error messages (`err_out`) for specific errors 
    related to device connectivity and configuration issues. If any recognized error is found, 
    it triggers an alert to inform the user about the problem. The function handles errors such as 
    device not being detected, connection issues, encoding errors, and more.

    Parameters
    ----------
    - err_out (`list`): A list of error messages returned from a command execution or device operation. 
    This list is checked against known device-related error conditions to determine if any specific errors have occurred.

    Returns
    -------
    - `bool`: Returns `True` if no errors are found (indicating that the device is functioning correctly). 
    Returns `False` if any recognized device-related error is found, triggering an alert to the user.
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
    elif "unauthorized" in err_out:
        create_alert(
            "Unauthorized",
            ("The device has not yet authorized this computer\n"
             "to establish an adb connection."),
        )
    elif "no matching camera found" in err_out:
        create_alert(
            "No Camera Was Found",
            "Make sure the camera is properly connected.",
        )
    else: 
        error_detect = False
    print(err_out)
    return error_detect

def args_combination_errors(err_out: list) -> bool:
    """
    Checks for argument combination errors and creates alerts for specific incompatible arguments.

    This function checks the provided output (`err_out`) of an adb command for known argument 
    combination errors, specifically when two or more arguments are incompatible with each other. 
    If such errors are found, it triggers an alert to inform the user about the conflicting arguments. 
    The function helps ensure that incompatible argument combinations are not used simultaneously.

    Parameters
    ----------
    - err_out (`str`): The output string from the adb command or scrcpy operation, containing error messages.

    Returns
    -------
    - `bool`: Returns `True` if no errors are detected (indicating that all argument combinations are valid). 
    Returns `False` if any incompatible argument combinations are found, triggering an alert to the user.
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
            ("The args '--show-touches' and '--no-control' (or camera) are not compatible\n" 
            "remove one of them and try again"),
        )
    elif "not request to stay awake if control is disabled" in err_out:
        create_alert(
            "Incompatible Args",
            ("The args '--stay-awake' and '--no-control' (or camera) are not compatible\n" 
            "remove one of them and try again"),
        )
    else: 
        error_detect = False
    print(err_out)
    return error_detect

#Errors for connection
def connection_errors(emit_tcpip: str = "", emit_connect: str = "") -> bool:
    """
    Checks for connection errors and creates alerts based on specific issues.

    This function checks the provided output (`emit_tcpip` and `emit_connect`) for known connection errors.
    If any connection-related issues are detected, it triggers an alert to inform the user about the problem.
    The function is designed to help identify issues related to establishing a connection with a device or server.

    Parameters
    ----------
    - emit_tcpip (`str`): The output of the `tcpip` command, which can indicate connection errors related to IP or port issues.
    - emit_connect (`str`): The output of the `connect` command, which can indicate connection issues such as already connected devices, timeouts, or refusals.

    Returns
    -------
    - `bool`: Returns `True` if no connection errors are detected, allowing the process to proceed.
    Returns `False` if any connection errors are found, triggering an alert to the user.
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
    elif "server connection failed" in emit_connect:
        create_alert(
            "Connection Failed",
            ("The connection was refused by the destination device,\n"
             "or the device is offline")
        )
    elif "protocol fault" in emit_connect:
        create_alert(
            "Protocol Fault",
            "The protocol faulted, make sure the IP/PORT is valid",
        )
    else:
        error_detect = False
    print(f"connect: {emit_connect}\n tcpip: {emit_tcpip}")
    return error_detect
        
def assemble_grid_layout(tab_name: str, locate: str, *elements: tuple) -> QGridLayout:
    """
    Assembles a QGridLayout for the specified tab and location with the provided elements.

    This function is used to construct a grid layout for a tab in the user interface. Based on the tab name
    ('connect_tab', 'start_tab', 'config_tab') and the location ('upper', 'middle', 'lower'), it arranges
    the provided elements in the appropriate grid positions. The elements are placed according to predefined
    positions for each tab and location.

    Parameters
    ----------
    - tab_name (`str`): The name of the tab where the layout will be applied. It can be one of the following:
      - `'connect_tab'`: A tab related to device connection.
      - `'start_tab'`: A tab for starting operations.
      - `'config_tab'`: A tab for configuring settings.

    - locate (`str`): The location where the elements will be placed within the grid. It can be one of the following:
      - `'upper'`: The upper section of the layout.
      - `'middle'`: The middle section of the layout.
      - `'lower'`: The lower section of the layout.

    - elements (`tuple`): A variable number of elements (widgets or other UI components) to be added to the grid layout.

    Returns
    -------
    - `QGridLayout`: A `QGridLayout` instance with the elements positioned according to the tab and location.

    Raises
    ------
    - `ValueError`: If the `tab_name` is not one of the predefined valid values (`'connect_tab'`, `'start_tab'`, `'config_tab'`).
    - `ValueError`: If the `locate` parameter is not one of the valid location values (`'upper'`, `'middle'`, `'lower'`).
    - `ValueError`: If the number of elements provided does not match the number of positions available for the given `tab_name` and `locate`.
    - `KeyError`: If the specified `tab_name` and `locate` combination does not have valid predefined positions.

    Notes
    -----
    - This function uses predefined position mappings for each tab and location. The number of elements passed
    must match the number of positions in the corresponding grid layout.
    - The grid layout will automatically adjust based on the tab and location, placing the elements in the right
    spots on the user interface.
    """
    tab_name = tab_name.lower().rstrip().lstrip()
    if tab_name not in ["connect_tab", "start_tab", "config_tab"]:
        raise ValueError(
            "The tab name is not valid. Please use "
            "'connect_tab', 'start_tab', or 'config_tab'."
        )
    
    locate =  locate.lower().rstrip().lstrip()
    if locate not in ["upper", "middle", "lower"]:
        raise ValueError(
            "The location is not valid. Please use " 
            "'upper', 'middle', or 'lower'."
        )
    try:
        positions = LAYOUT_POSITIONS[tab_name][locate]
    except KeyError:
        raise KeyError(
            "Check that the keys are valid and that the "
            "chosen location is valid for the tab."
        )
    else:
        if len(positions) != len(elements):
            raise ValueError(
                "The number of elements does not match the number of positions. "
                f"pos: {len(positions)} elms: {len(elements)}"
            )
        return add_widget_set(list(elements), positions)

#takes the data needed for the UI to work correctly
def get_datas_for_ui(data: dict, data_for: str) -> tuple:
    """
    Retrieves the necessary data for the user interface (UI) based on the specified category.

    This function extracts specific data from the provided dictionary based on the category 
    specified in the `data_for` argument. The data is used to populate the user interface for 
    different sections (connect, start, or config). 

    Parameters
    ----------
    - data (`dict`): A dictionary containing various configurations and session data. 
    It should include keys like 'Connect', 'Last_Session_Config', 'Custom_Config_Set', 
    'Versions', 'Resolutions', 'File_Path_Config', and others based on the UI sections.

    - data_for (`str`): The category of data to retrieve. It must be one of the following:
    - `'connect'`: Retrieves data related to the connection tab.
    - `'start'`: Retrieves data related to the start tab.
    - `'config'`: Retrieves data related to the config tab.

    Returns
    -------
    - `tuple`: A tuple containing the relevant data for the specified category.
    
    Raises
    ------
    - `ValueError`: If the `data_for` is not one of the allowed values (`'connect'`, `'start'`, or `'config'`).
    - `ValueError`: If the `data` parameter is not a dictionary.
    - `KeyError`: If the keys expected in the dictionary (`'Connect'`, `'Last_Session_Config'`, etc.) do not exist in the provided data.
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
        raise ValueError(
            "Please choose a value from these: ['connect', 'start', 'config']"
        )
