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

running_on_windows = system() == "Windows"
def open_or_save_data_json(json_url: str, open_mode: str, data_to_save: dict = None) -> dict:
    """
    This function opens or saves a `JSON` file.
    
    Parameters
    ----------
    - json_url (`str`): The URL of the `JSON` file.
    - open_mode (`str`): The mode to open the `JSON` file.
    - data_to_save (`dict`, `optional`): The data to save in the `JSON` file. Defaults to None.
    
    Returns
    -------
    - `dict` if `open_mode` is 'r', else `None`
    
    Raises
    ------
    - `ValueError`: If `open_mode` is not a valid mode.
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
    This function connects a signal to a `method` using `getattr` and `partial`.
    
    Parameters
    ----------
    - element (`any`): The element to connect the signal to.
    - conn_type (`str`): The type of signal to connect.
    - method (`Callable`): The method to be called when the signal is emitted.
    - *args (`tuple`): The arguments to be passed to the method.
    
    Raises
    ------
    - `ValueError`: If `conn_type` is not a valid connection type.
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
        raise ValueError(f"Invalid connection type: '{conn_type}'. " 
                         f"Valid types: '{valid_conn_types}'")
    
    if conn_type in valid_conn_types:
        getattr(element, conn_type).connect(partial(method, *args))
        
def toggle_button_state(
    buttons: list, 
    toggle_to: bool, 
    old_texts: list = None,
    charge_text: bool = True,
    disabled_text = "LOADING...",
) -> list:
    """
    This function toggles the `state` of a list of `buttons`.
    
    Parameters
    ----------
    - buttons (`list`): A list of buttons.
    - toggle_to (`bool`): True to enable the buttons, False to disable them.
    - old_texts (`list`, `optional`): A list of texts to be replaced by the disabled text. Defaults to None.
    - charge_text (`bool`, `optional`): True to charge the text with the disabled text. Defaults to True.
    - disabled_text (`str`, `optional`): The text to be displayed when the button is disabled. Defaults to "LOADING...".
    
    Returns
    -------
    - `list` if `toggle_to` is True, else `None`
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
    This function verifies if the `scrcpy` and `adb` files are in the same path.
    
    Parameters
    ----------
    - path (`str`): The path where the `scrcpy` and `adb` files are located.
    
    Returns
    -------
    - `bool`: True if the `scrcpy` and `adb` files are in the same path, False otherwise.
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
    This function checks if the given string is an `IP address`.
    
    Parameters
    ----------
    - ip (`str`): The string to be checked.
    
    Returns
    -------
    - `bool`: True if the string is an `IP address`, False otherwise.
    """
    ipv4 = findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", ip)
    ipv6 = findall(r"\b(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}\b", ip)
    
    return bool(ipv4 or ipv6)

def get_file_name(arg_line: str, path: str = "") -> str:
    """
    This function returns the `file name` from the `command string`.
    
    Parameters
    ----------
    - cmd (`str`): The command string to extract the `file name` from.
    
    Returns
    -------
    - `str`: The `file name` extracted from the command string.
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
    This function checks if the `max-size` value is `valid`. It checks if the value is an `integer` and greater than `200`.
    
    Parameters
    ----------
    - cmd (`str`): The command string to check.
    
    Returns
    -------
    - `bool`: True if the `max-size` value is valid, False otherwise.
    """
    max_size = findall(r"-(?:m|--max-size)\s+(\S+)", cmd)
    max_size = max_size[0] if max_size else ""
    max_size = int(max_size) if max_size.isdigit() else ""
    
    return max_size >= 500 if max_size else True

def update_data_file(value: any, keys: list, delete_value: bool = False) -> None:
    """
    This function `updates` the `data file` with the given `value` and `keys`.
    
    Parameters
    ----------
    - value (`any`): The value to be updated.
    - keys (`list`): The keys to be updated.
    - delete_value (`bool`, `optional`): If True, the value will be deleted. Defaults to False.
    """
    path = join(".", "Data", "UserData.json")
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
    This function returns the `current alert` theme based on the `user's selected theme`.
    
    Returns
    -------
    - `dict`: The current alert theme.
    """
    select_theme = open_or_save_data_json(join(".", "Data", "UserData.json"), "r")["Theme_Active"]
    return black_theme_Alerts if select_theme == 0 else white_theme_Alerts   

def add_widget_set(widgets: list, positions: list[tuple]) -> QGridLayout:
    """
    This function creates a `QGridLayout` with the given `widgets` and `positions`.
    
    Parameters
    ----------
    - widgets (`list`): A list of widgets to be added to the layout.
    - positions (`list[tuple]`): A list of tuples containing the positions of the widgets.
    
    Returns
    -------
    - `QGridLayout`: The created `QGridLayout` object.
    
    Raises
    ------
    - `ValueError`: If the number of widgets does not match the number of positions.
    
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
