from typing import Union
from os.path import join

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QGridLayout

from Script.Utilities import Create_Elements as Create
from Script.Utilities.Utils import get_current_alert_theme
from Theme.icon_alert import *

def create_alert(
    title: str = "Default Title", 
    msg: str = "Default Menssage", 
    alert_type: str = "alert",
    regex_filter: str = None,
) -> Union[None, str, bool]:
    """
    This function creates an alert, it can be `alert`, `input` or `confirm`, depending on the `alert_type` parameter.
    
    Parameters
    ----------
    - title (`str`, `optional`): The title of the alert. Defaults to "Default Title".
    - msg (`str`, `optional`): The message of the alert. Defaults to "Default Menssage".
    - alert_type (`str`, `optional`): The type of the alert. Defaults to "alert".
    - regex_filter (`str`, `optional`): The regex filter to be applied to the input. Defaults to None.
    
    Returns
    -------
    - `None` if alert_type is `alert`.
    - (`str`, `bool`) if alert_type is `input`.
    - `bool` if alert_type is `confirm`.
    
    Raises
    ------
    - `ValueError`: If `alert_type` is not a valid alert type.
    """
    if alert_type not in ["alert", "input", "confirm"]:
        raise ValueError(f"The '{alert_type}' mode is invalid --> 'alert' | 'input' | 'confirm'")
    
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
        
