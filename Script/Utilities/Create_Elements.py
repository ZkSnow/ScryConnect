from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QPushButton,
    QCheckBox,
    QRadioButton,
    QSlider,
    QLabel,
    QLineEdit,
    QComboBox
)

def Button(
    text: str, 
    w_h: tuple = None, 
    object_name: str = None,
    parent: any = None,
) -> QPushButton:
    """
    Creates a QPushButton instance with optional customization.

    This function simplifies the creation of a `QPushButton` widget, allowing you 
    to set its parent, dimensions, and object name during initialization.

    Parameters
    ----------
    - text (`str`): The label or text displayed on the button.
    - w_h (`tuple`, optional): A tuple `(width, height)` specifying the minimum dimensions of the button. 
    Defaults to `None`.
    - object_name (`str`, optional): The object name assigned to the button for styling or identification purposes. 
    Defaults to `None`.
    - parent (`any`, optional): The parent widget of the button. Defaults to `None`.

    Returns
    -------
    - `QPushButton`: A configured `QPushButton` instance.
    
    Notes
    -----
    - If `w_h` is provided, it sets the button's minimum size using the values in the tuple.
    - If `object_name` is provided, it assigns the name to the button for identification 
    (useful for styling with QSS).
    """
    button = QPushButton(text, parent)  
    if w_h:
        button.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        button.setObjectName(object_name)

    return button  
    
def CheckBox(
    text: str, 
    w_h: tuple = None, 
    active: bool = False, 
    object_name: str = None,
    parent: any = None, 
) -> QCheckBox:
    """
    Creates a QCheckBox instance with optional customization.

    This function facilitates the creation of a `QCheckBox` widget, allowing you 
    to configure its parent, dimensions, initial state, and object name.

    Parameters
    ----------
    - text (`str`): The label or text displayed next to the checkbox.
    - w_h (`tuple`, optional): A tuple `(width, height)` specifying the minimum dimensions of the checkbox. 
    Defaults to `None`.
    - active (`bool`, optional): Specifies whether the checkbox should be checked (`True`) or unchecked (`False`) 
    initially. Defaults to `False`.
    - object_name (`str`, optional): The object name assigned to the checkbox for styling or identification purposes. 
    Defaults to `None`.
    - parent (`any`, optional): The parent widget of the checkbox. Defaults to `None`.

    Returns
    -------
    - `QCheckBox`: A configured `QCheckBox` instance.

    Notes
    -----
    - If `w_h` is provided, it sets the checkbox's minimum size using the values in the tuple.
    - The `active` parameter allows you to predefine the initial state of the checkbox 
    (checked or unchecked).
    - If `object_name` is provided, it assigns the name to the checkbox for identification 
    (useful for styling with QSS).
    """
    check_box = QCheckBox(text, parent)
    check_box.setChecked(active)
    if w_h:
        check_box.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        check_box.setObjectName(object_name)

    return check_box   
    
def RadioButton(
    text: str, 
    w_h: tuple = None, 
    active: bool = False, 
    object_name: str = None,
    parent: any = None, 
) -> QRadioButton:
    """
    Creates a QRadioButton instance with optional customization.

    This function simplifies the creation of a `QRadioButton` widget, allowing you 
    to set its parent, dimensions, initial state, and object name during initialization.

    Parameters
    ----------
    - text (`str`): The label or text displayed next to the radio button.
    - w_h (`tuple`, optional): A tuple `(width, height)` specifying the minimum dimensions of the radio button. 
    Defaults to `None`.
    - active (`bool`, optional): Indicates whether the radio button should be selected (`True`) or deselected (`False`) 
    initially. Defaults to `False`.
    - object_name (`str`, optional): The object name assigned to the radio button for styling or identification purposes. 
    Defaults to `None`.
    - parent (`any`, optional): The parent widget of the radio button. Defaults to `None`.

    Returns
    -------
    - `QRadioButton`: A configured `QRadioButton` instance.
    
    Notes
    -----
    - If `w_h` is provided, it sets the radio button's minimum size using the values in the tuple.
    - The `active` parameter allows you to predefine the initial state of the radio button 
    (selected or not selected).
    - If `object_name` is provided, it assigns the name to the radio button for identification 
    (useful for styling with QSS).
    """
    radio = QRadioButton(text, parent)
    radio.setChecked(active)
    if w_h:
        radio.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        radio.setObjectName(object_name)

    return radio
    
def Combox(
    items: list, 
    w_h: tuple = None, 
    index: int = 0, 
    object_name: str = None,
    parent: any = None, 
) -> QComboBox:
    """
    Creates a QComboBox instance with optional customization.

    This function simplifies the creation of a `QComboBox` widget, allowing you 
    to populate it with items, set its parent, dimensions, default selected index, 
    and object name during initialization.

    Parameters
    ----------
    - items (`list`): A list of strings to populate the combo box.
    - w_h (`tuple`, optional): A tuple `(width, height)` specifying the minimum dimensions of the combo box. 
    Defaults to `None`.
    - index (`int`, optional): The zero-based index of the item to be selected by default. 
    If the index is out of range, it defaults to `0`. Defaults to `0`.
    - object_name (`str`, optional): The object name assigned to the combo box for styling or identification purposes. 
    Defaults to `None`.
    - parent (`any`, optional): The parent widget of the combo box. Defaults to `None`.

    Returns
    -------
    - `QComboBox`: A configured `QComboBox` instance.
    
    Notes
    -----
    - If `w_h` is provided, it sets the combo box's minimum size using the values in the tuple.
    - The `index` parameter ensures the default selected item is within the valid range of items. 
    If the provided index is out of range (negative or greater than the number of items), it defaults to `0`.
    - If `object_name` is provided, it assigns the name to the combo box for identification 
    (useful for styling with QSS).
    """
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
    w_h: tuple = None, 
    object_name: str = None,
    parent: any = None,
) -> QLabel:
    """
    Creates a QLabel instance with optional customization.

    This function simplifies the creation of a `QLabel` widget, allowing you 
    to set its parent, dimensions, and object name during initialization.

    Parameters
    ----------
    - text (`str`): The text to be displayed on the label.
    - w_h (`tuple`, optional): A tuple `(width, height)` specifying the minimum dimensions of the label. 
    Defaults to `None`.
    - object_name (`str`, optional): The object name assigned to the label for styling or identification purposes. 
    Defaults to `None`.
    - parent (`any`, optional): The parent widget of the label. Defaults to `None`.

    Returns
    -------
    - `QLabel`: A configured `QLabel` instance.
    
    Notes
    -----
    - If `w_h` is provided, it sets the label's minimum size using the values in the tuple.
    - If `object_name` is provided, it assigns the name to the label for identification 
    (useful for styling with QSS).
    """
    label = QLabel(text, parent)
    if w_h:
        label.setMinimumSize(w_h[0], w_h[1])
    
    if object_name:
        label.setObjectName(object_name)

    return label
    
def LineEdit(
    placeholder: str, 
    w_h: tuple = None, 
    initial_text: str | int = None,
    input_filter: str = None,
    object_name: str = None,
    parent: any = None,
) -> QLineEdit:
    """
    Creates a QLineEdit instance with optional customization.

    This function simplifies the creation of a `QLineEdit` widget, allowing you 
    to set its placeholder text, parent, dimensions, initial text, input filter, 
    and object name during initialization.

    Parameters
    ----------
    - placeholder (`str`): The placeholder text displayed when the line edit is empty.
    - w_h (`tuple`, optional): A tuple `(width, height)` specifying the minimum dimensions of the line edit. 
    Defaults to `None`.
    - initial_text (`str | int`, optional): The initial text or value to display in the line edit. 
    Converted to a string if not already. Defaults to `None`.
    - input_filter (`str`, optional): A regular expression (`regex`) to restrict the input. 
    Only inputs matching the `regex` are accepted. Defaults to `None`.
    - object_name (`str`, optional): The object name assigned to the line edit for styling or identification purposes. 
    Defaults to `None`.
    - parent (`any`, optional): The parent widget of the line edit. Defaults to `None`.

    Returns
    -------
    - `QLineEdit`: A configured `QLineEdit` instance.

    Notes
    -----
    - If `w_h` is provided, it sets the line edit's minimum size using the values in the tuple.
    - The `initial_text` parameter initializes the line edit with a predefined value if provided.
    - The `input_filter` parameter uses a regular expression to validate the input. Inputs not matching 
    the filter are not accepted.
    - If `object_name` is provided, it assigns the name to the line edit for identification 
    (useful for styling with QSS).
    """
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
    v_min: int = 0, 
    v_max: int = 100,
    step: int = 10,
    initial_value: int = None, 
    w_h: tuple = None, 
    orientation: str = "h", 
    object_name: str = None,
    parent: any = None,
) -> QSlider:
    """
    Creates a QSlider instance with optional customization.

    This function simplifies the creation of a `QSlider` widget, allowing you 
    to configure its range, step size, initial value, dimensions, orientation, 
    and object name during initialization.

    Parameters
    ----------
    - v_min (`int`, optional): The minimum value of the slider's range. Defaults to `0`.
    - v_max (`int`, optional): The maximum value of the slider's range. Defaults to `100`.
    - step (`int`, optional): The step size for the slider. Defaults to `10`.
    - initial_value (`int`, optional): The initial value of the slider. Defaults to `None`.
    - w_h (`tuple`, optional): A tuple `(width, height)` specifying the minimum dimensions of the slider. 
    Defaults to `None`.
    - orientation (`str`, optional): The orientation of the slider. Use `"h"` for horizontal 
    and `"v"` for vertical. Defaults to `"h"`.
    - object_name (`str`, optional): The object name assigned to the slider for styling or identification purposes. 
    Defaults to `None`.
    - parent (`any`, optional): The parent widget of the slider. Defaults to `None`.

    Returns
    -------
    - `QSlider`: A configured `QSlider` instance.

    Raises
    ------
    - `ValueError`: If an invalid orientation is provided (only `"h"` or `"v"` are allowed).

    Notes
    -----
    - The `initial_value` parameter sets the slider's starting value, if provided.
    - The `orientation` parameter controls whether the slider is horizontal (`"h"`) 
    or vertical (`"v"`). An invalid orientation raises a `ValueError`.
    - If `w_h` is provided, it sets the slider's minimum size using the values in the tuple.
    - If `object_name` is provided, it assigns the name to the slider for identification 
    (useful for styling with QSS).
    """
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
        
    
        
    

    
