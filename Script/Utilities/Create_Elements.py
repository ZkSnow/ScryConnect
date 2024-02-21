from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QPushButton, QCheckBox, QRadioButton, 
                             QSlider, QLabel, QLineEdit, QComboBox)

def Button(
    text: str, 
    parent: any = None, 
    w_h: tuple = None, 
    object_name: str = None
) -> QPushButton:
    """Create a button (QPushButton)"""
    button = QPushButton(text, parent)  
    if w_h:
        button.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        button.setObjectName(object_name)

    return button  
    
def CheckBox(
    text: str, 
    parent: any = None, 
    w_h: tuple = None, 
    active: bool = False, 
    object_name: str = None
) -> QCheckBox:
    """Create a checkbox (QCheckBox)"""
    check_box = QCheckBox(text, parent)
    check_box.setChecked(active)
    if w_h:
        check_box.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        check_box.setObjectName(object_name)

    return check_box   
    
def RadioButton(
    text: str, 
    parent: any = None, 
    w_h: tuple = None, 
    active: bool = False, 
    object_name: str = None
) -> QRadioButton:
    """Create a radio button (QRadioButton)"""
    radio = QRadioButton(text, parent)
    radio.setChecked(active)
    if w_h:
        radio.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        radio.setObjectName(object_name)

    return radio
    
def Combox(
    items: list, 
    parent: any = None, 
    w_h: tuple = None, 
    index: int = 0, 
    object_name: str = None,
) -> QComboBox:
    """Create a combo box (QComboBox)"""
    combox = QComboBox(parent)
    combox.addItems(items)
    index = 0 if index > combox.count()-1 or index < 0 else index    
    combox.setCurrentIndex(index)
    if w_h:
        combox.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        combox.setObjectName(object_name)

    return combox
   
def Label(
    text: str, 
    parent: any = None,
    w_h: tuple = None, 
    object_name: str = None,
) -> QLabel:
    """Create a label (QLabel)"""
    label = QLabel(text, parent)
    if w_h:
        label.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        label.setObjectName(object_name)

    return label
    
def LineEdit(
    placeholder: str, 
    parent: any = None,
    w_h: tuple = None, 
    initial_text: str | int = None,
    input_filter: str = None,
    object_name: str = None,
) -> QLineEdit:
    """Create a line edit (QLineEdit)"""
    line = QLineEdit(parent)
    line.setPlaceholderText(placeholder)
    if w_h:
        line.setMinimumSize(w_h[0], w_h[1])
    
    if initial_text:
        line.setText(str(initial_text))
    
    if object_name:
        line.setObjectName(object_name)
    
    if input_filter:
        regex = QRegExp(input_filter)
        line.setValidator(QRegExpValidator(regex))
    
    return line

def Slider(
    parent: any = None, 
    v_min: int = 0, 
    v_max: int = 100,
    step: int = 10,
    initial_value: int = None, 
    w_h: tuple = None, 
    orientation: str = "h", 
    object_name: str = None
) -> QSlider:
    """Create a slider (QSlider)"""
    slider = QSlider(parent)
    slider.setRange(v_min, v_max)
    slider.setPageStep(step)
    if w_h:
        slider.setMinimumSize(w_h[0], w_h[1])

    if initial_value:
        slider.setValue(initial_value)

    if object_name:
        slider.setObjectName(object_name)
        
    if orientation.lower() == "h":
        slider.setOrientation(QtCore.Qt.Horizontal)
    elif orientation.lower() == "v":
        slider.setOrientation(QtCore.Qt.Vertical)
    else:
        raise ValueError("Invalid orientation, h = Horizontal | v = Vetical")

    return slider
        
    
        
    

    