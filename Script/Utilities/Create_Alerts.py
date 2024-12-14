from typing import Union
from os.path import join

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QGridLayout

from Script.Utilities import Create_Elements as Create
from Script.Utilities.Utils import get_current_alert_theme
from Theme.icon_alert import *

def create_alert(
    title: str = "", 
    msg: str = "", 
    alert_type: str = "alert",
    regex_filter: str = None,
) -> Union[None, str, bool]:
    """
    Creates an alert dialog with different types of interactions.

    This function can create three types of alerts: 
    - `alert`: A simple informational alert with an "OK" button.
    - `input`: A prompt for the user to enter text, with validation via regex.
    - `confirm`: A confirmation dialog with "OK" and "Cancel" buttons.

    Parameters
    ----------
    - title (`str`, optional): The title of the alert dialog. Defaults to `""`.
    - msg (`str`, optional): The message displayed in the alert. Defaults to `""`.
    - alert_type (`str`, optional): The type of alert to create. 
    Must be one of `"alert"`, `"input"`, or `"confirm"`. Defaults to `"alert"`.
    - regex_filter (`str`, optional): A regular expression used to validate the input text 
    when `alert_type` is `"input"`. Defaults to `None`.

    Returns
    -------
    - `None`: If the `alert_type` is `"alert"`.
    - `str`, `bool`: If the `alert_type` is `"input"`, returns the entered text (as a string) 
    and a boolean indicating whether the user confirmed the input.
    - `bool`: If the `alert_type` is `"confirm"`, returns `True` if the user clicked "OK", 
    and `False` if the user clicked "Cancel".

    Raises
    ------
    - `ValueError`: If `alert_type` is not one of `"alert"`, `"input"`, or `"confirm"`.
    
    Notes
    -----
    - If `regex_filter` is provided, it is used to validate the user input in the `"input"` alert type.
    - The dialog appearance is customized using a predefined stylesheet (`get_current_alert_theme()`), and an icon (`icon_alert.ico`).
    """
    if alert_type not in ["alert", "input", "confirm"]:
        raise ValueError(
            f"The '{alert_type}' mode is invalid --> 'alert' | 'input' | 'confirm'"
        )
    
    alert = QDialog(None)
    alert.setWindowIcon(QIcon(join(":", "icon_alert.ico")))
    alert.setMinimumWidth(300)
    alert.setWindowTitle(title)
    alert.setStyleSheet(get_current_alert_theme())

    alert_type = alert_type.lower()
    if alert_type == "alert":
        ok = Create.Button("OK")
        ok.clicked.connect(alert.accept)
        
        layout = QGridLayout()
        msg = Create.Label(msg)
        msg.setOpenExternalLinks(True)
        layout.addWidget(Create.Label(title), 0, 0, 1, 2)
        layout.addWidget(msg, 1, 0, 1, 2)
        layout.addWidget(ok, 2, 0, 1, 2)
        alert.setLayout(layout)
        alert.exec()
        
        return None
    elif alert_type == "input":
        input_text = Create.LineEdit("Enter here...", input_filter=regex_filter)
        ok = Create.Button("OK")
        cancel = Create.Button("Cancel")
        ok.clicked.connect(alert.accept)
        cancel.clicked.connect(alert.close)
        
        layout = QGridLayout()
        msg = Create.Label(msg)
        msg.setOpenExternalLinks(True)
        layout.addWidget(msg, 0, 0, 1, 2)
        layout.addWidget(input_text, 1, 0, 1, 2)
        layout.addWidget(ok, 2, 0)
        layout.addWidget(cancel, 2, 1)
        alert.setLayout(layout)
        confirm = alert.exec()

        return (input_text.text().lower().rstrip(), True) \
               if confirm == 1 else ("", False)
    else:
        ok = Create.Button("Ok")
        cancel = Create.Button("Cancel")
        ok.clicked.connect(alert.accept)
        cancel.clicked.connect(alert.close)
     
        layout = QGridLayout()
        msg = Create.Label(msg)
        msg.setOpenExternalLinks(True)
        layout.addWidget(Create.Label(title), 0, 0, 1, 2)
        layout.addWidget(msg, 1, 0, 1, 2)
        layout.addWidget(ok, 2, 0)
        layout.addWidget(cancel, 2, 1)
        alert.setLayout(layout)
        confirm = alert.exec()
        
        return confirm == 1
        
