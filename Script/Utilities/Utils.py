from posixpath import splitext
from functools import partial
from os import listdir
from os.path import join
from re import findall
from json import load, dump
from platform import system
from typing import Callable

from PyQt5.QtWidgets import QGridLayout
from Theme.Style_UI import black_theme_Alerts, white_theme_Alerts
from Script.Utilities.Static_Datas import PATH_DATA_DIR

running_on_windows = system() == "Windows"
def open_or_save_data_json(json_url: str, open_mode: str, data_to_save: dict = None) -> dict:
    """
    This function either opens or saves a `JSON` file based on the specified `open_mode`.

    Parameters
    ----------
    - json_url (`str`): The URL or path of the `JSON` file to open or save.
    - open_mode (`str`): The mode to open the `JSON` file. Should be either 'r' for reading or 'w' for writing.
    - data_to_save (`dict`, optional): The data to save in the `JSON` file if `open_mode` is 'w'. Defaults to `None`.

    Returns
    -------
    - `dict`: The data loaded from the `JSON` file if `open_mode` is 'r'.
    - `None`: If `open_mode` is 'w' (when data is written and nothing is returned).

    Raises
    ------
    - `ValueError`: If either `open_mode` or `json_url` is not a string.
    - `ValueError`: If `open_mode` is not 'r' or 'w'.
    """
    if not isinstance(open_mode , str) and not isinstance(json_url , str):
        raise ValueError("'open_mode' and 'json_url' has to be a string.")
    
    if open_mode.lower() not in ["r", "w"]:
        raise ValueError(f"'{open_mode}' is not a valid mode, use 'r' or 'w'")
    
    with open(json_url, open_mode.lower()) as json_data:
        if open_mode == "r":
            return load(json_data)
        else:
            dump(data_to_save, json_data)

def connect_signal(element: any, conn_type: str, method: Callable, *args: tuple) -> None:
    """
    This function connects a signal of a specified `conn_type` to a `method` using `getattr` 
    and `functools.partial`, passing additional arguments to the method when the signal is emitted.
    
    Parameters
    ----------
    - element (`any`): The object or element that emits the signal (e.g., a widget or UI element).
    - conn_type (`str`): The name of the signal to connect (e.g., 'clicked', 'textChanged').
    - method (`Callable`): The method to be called when the signal is emitted.
    - *args (`tuple`): The arguments to be passed to the method when the signal is triggered.
    
    Raises
    ------
    - `ValueError`: If `conn_type` is not a valid connection type (not in the list of predefined signals).
    """
    valid_conn_types = [
        "clicked",
        "currentIndexChanged",
        "textChanged",
        "stateChanged",
        "valueChanged",
        "activated",
    ]
    if conn_type not in valid_conn_types:
        raise ValueError(
            f"Invalid connection type: '{conn_type}'. Valid types: '{valid_conn_types}'"
        )
    getattr(element, conn_type).connect(partial(method, *args))
        
def toggle_button_state(
    buttons: list, 
    toggle_to: bool, 
    old_texts: list = None,
    charge_text: bool = True,
    disabled_text = "LOADING...",
) -> list:
    """
    This function toggles the state of a list of buttons by enabling or disabling them 
    and optionally changing their text to indicate a loading state.

    Parameters
    ----------
    - buttons (`list`): A list of button objects.
    - toggle_to (`bool`): True to enable the buttons, False to disable them.
    - old_texts (`list`, optional): A list of original texts to revert to when enabling the buttons. Defaults to None.
    - charge_text (`bool`, optional): If True, the text of the buttons will be set to `disabled_text` when disabling. Defaults to True.
    - disabled_text (`str`, optional): The text to display on the buttons when they are disabled. Defaults to "LOADING...".
    
    Returns
    -------
    - `list`: A list of the original texts of the buttons if `toggle_to` is `False` (when buttons are disabled).
    - `None`: If `toggle_to` is `True` (when buttons are enabled).

    Notes
    -----
    - If `old_texts` is provided, the original texts will be restored when the buttons are enabled.
    - The length of `old_texts` should match the number of buttons in the `buttons` list.
    """
    buttons = buttons if isinstance(buttons, list) else [buttons]
    if toggle_to:
        for index, elems in enumerate(buttons):
            elems.setEnabled(True)
            if old_texts and charge_text:
                elems.setText(old_texts[index])
    else:
        current_texts = []
        for elems in buttons:
            text = elems.text()
            elems.setDisabled(True)
            if charge_text:
                current_texts.append(text)
                elems.setText(disabled_text)
    
        return current_texts

def verify_scrcpy_path(path: str) -> bool:
    """
    This function verifies if the `scrcpy` and `adb` executables are located in the same directory.
    The function checks for their presence in the specified `path`.

    Parameters
    ----------
    - path (`str`): The directory path where the `scrcpy` and `adb` executables are located.

    Returns
    -------
    - `bool`: 
      - On Windows, returns `True` if both `scrcpy.exe` and `adb.exe` are found in the same directory.
      - On Linux, always returns `True` (since scrcpy and adb may be installed differently).

    Raises
    ------
    - `FileNotFoundError`: If the provided `path` does not exist.
    - `NotADirectoryError`: If the provided `path` is not a directory.
    """
    try:
        path = path["Path"] if isinstance(path, dict) else path
        files = [file.lower().rstrip() for file in listdir(path)]
        verify = "scrcpy.exe" in files and "adb.exe" in files 
    except (FileNotFoundError, NotADirectoryError):
        verify = False
   
    return verify if running_on_windows else True
 
def check_is_ip(ip: str) -> bool:
    """
    This function checks if the given string is a valid IPv4 or IPv6 address.

    Parameters
    ----------
    - ip (`str`): The string to be checked, which should represent an IP address.

    Returns
    -------
    - `bool`: True if the string is a valid IPv4 or IPv6 address, False otherwise.

    Notes
    -----
    - The function uses regular expressions to validate the IP format. 
    It checks for the general structure of IPv4 (x.x.x.x) and IPv6 (x:x:x:x:x:x:x:x) addresses.
    """
    ipv4 = findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", ip)
    ipv6 = findall(r"\b(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}\b", ip)
    
    return bool(ipv4 or ipv6)

def get_file_name(arg_line: str, path: str = "") -> str:
    """
    This function returns the modified command string and the `file name` extracted 
    from the `command string`.
    
    Parameters
    ----------
    - arg_line (`str`): The command string to extract the `file name` from.
    - path (`str`, optional): The directory path to check for filename existence (default is "").
    
    Returns
    -------
    - (`str`, `str`): A tuple where the first element is the modified command string (with 
    the new file name if necessary) and the second element is the extracted `file name`.
    """
    file_name = findall(r"-(?:r|-record)\s+(\S+)", arg_line)
    file_name = file_name[0] if file_name else ""

    if path and file_name in listdir(path):
        index = 0
        while True:
            name_extension = splitext(file_name.lower())
            new_file_name = f"{name_extension[0]}_{index}{name_extension[1]}"
            if new_file_name not in listdir(path):
                break
            else:
                index += 1

        new_arg_line = arg_line.replace(file_name, new_file_name)
        return new_arg_line, new_file_name.lower()
    
    return arg_line, file_name.lower()

def valid_maxsize_value(cmd: str) -> bool:
    """
    This function checks if the `max-size` value is valid. It verifies that the value is an integer 
    and that it is greater than or equal to 500. If the `max-size` parameter is not present, 
    the function returns `True` by default.

    Parameters
    ----------
    - cmd (`str`): The command string to check, which should contain the `max-size` parameter.

    Returns
    -------
    - `bool`: 
      - True if the `max-size` value is either not present, or if the value is valid (an integer and >= 500).
      - False if the `max-size` value is an integer but less than 500.
    """
    max_size = findall(r"-(?:m|--max-size)\s+(\S+)", cmd)
    max_size = max_size[0] if max_size else ""
    max_size = int(max_size) if max_size.isdigit() else ""
    
    return max_size >= 500 if max_size else True

def update_data_file(value: any, keys: list, delete_value: bool = False) -> None:
    """
    This function updates a nested key-value pair in a data file (JSON) based on the provided `keys`.
    If `delete_value` is True, it deletes the key instead of updating the value.
    
    Parameters
    ----------
    - value (`any`): The new value to be set for the final key in the nested structure.
    - keys (`list`): A list of keys representing the path to the nested key to be updated or deleted.
    - delete_value (`bool`, optional): If True, the key will be deleted from the nested structure.
    Defaults to False, meaning the key will be updated with the provided `value`.   
     
    Notes
    -----
    - This function is useful for updating or deleting nested data in a JSON file where each key is represented 
    as a list of keys in the `keys` parameter.
    - If `delete_value` is set to `True`, the function removes the specified key from the nested structure.
    """
    path = join(PATH_DATA_DIR, "UserData.json")
    data = open_or_save_data_json(path, "r")
    sub_dict = data
    for index, key in enumerate(keys):
        index += 1
        if index < len(keys):
            sub_dict = data[key] if index == 1 else sub_dict[key]
        else: 
            if delete_value:
                del sub_dict[key]
            else:
                sub_dict[key] = value
    
    open_or_save_data_json(path, "w", data)           
               
def get_current_alert_theme() -> dict:
    """
    This function returns the current alert theme based on the user's selected theme.
    The selected theme is retrieved from the `UserData.json` file, and depending on the theme value,
    it returns either the `black_theme_Alerts` or `white_theme_Alerts`.

    Returns
    -------
    - `dict`: The alert theme corresponding to the user's selected theme. 
      - `black_theme_Alerts` if the selected theme is dark (represented by 0).
      - `white_theme_Alerts` if the selected theme is light (represented by 1).
    """
    select_theme = open_or_save_data_json(
        join(PATH_DATA_DIR, "UserData.json"), "r"
    )["Theme_Active"]
    return black_theme_Alerts if select_theme == 0 else white_theme_Alerts   

def add_widget_set(widgets: list, positions: list[tuple]) -> QGridLayout:
    """
    This function creates a `QGridLayout` and adds the given `widgets` to it at the specified `positions`.
    
    Parameters
    ----------
    - widgets (`list`): A list of widgets to be added to the layout. The number of widgets must match 
    the number of positions.
    - positions (`list[tuple]`): A list of tuples specifying the positions of the widgets in the grid. 
    Each tuple can have:
      - 2 elements: (row, column) indicating the position of the widget.
      - 4 elements: (row, column, rowSpan, columnSpan) indicating the position and the span of the widget.

    Returns
    -------
    - `QGridLayout`: The created `QGridLayout` object with the widgets added at the specified positions.
    
    Raises
    ------
    - `ValueError`: 
      - If the number of widgets does not match the number of positions.
      - If any position tuple does not have either 2 or 4 elements.
    """
    if len(widgets) != len(positions):
        raise ValueError("The number of widgets does not match the number of positions.")
    
    layout = QGridLayout()
    for index, widget in enumerate(widgets):
        pos = positions[index]
        if len(pos) == 2:
            layout.addWidget(widget, pos[0], pos[1])
        elif len(pos) == 4:
            layout.addWidget(widget, pos[0], pos[1], pos[2], pos[3])
        else: 
            raise ValueError("The number of positions is invalid, it must have 2 or 4 positions")
    return layout
