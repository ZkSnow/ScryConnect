black_theme = """
QMainWindow {
	background-color: #02031a;
}

#test_element {
    background-color: blue;
}

#test_element2 {
    background-color: red;
}

#test_element3 {
    background-color: green;
}

#test_element4 {
    background-color: purple;
}

QWidget {
	background-color: #02031a;
}

QWidget::item {
    color: #ebdfcc;
}

QWidget::item:selected {
    color: #ff0841;
    background-color: #0b0321;
}

QPushButton {
    background-color: #021b2b;
    color: #f0edee;
    border: none;
    border-radius: 5px;
    font-size: 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #b10c43;
}
QPushButton:pressed {
    background-color: #ff0841;
    color: #f0edee;
}
QPushButton:disabled {
    background-color: #6f6f6f;
    color: #e6e6e6;
}
#Shell_Button {
    border-radius: 2px;
    font-size: 13px;
}
#Shell_Button:hover {
    background-color: #b10c43;
}
#Shell_Button:pressed {
    background-color: #ff0841;
}

#Default_Config_Button, #Github_Button {
    border-radius: 2px;
    font-size: 13px;
}
#Github_Button{
    background-color: white;
    font-size: 12px;
}
#Github_Button:hover {
    background-color: black;
    font-size: 13px;
}
#Github_Button:pressed {
    background-color: #ff0841;
}

#ThemeButton {
    border-radius: 0px;
    background-color: #02031a;
    font-size: 13px;
}
#ThemeButton:hover {
    background-color: #ff0841;
    color: #f0edee;
    
}

#ExitButton, #MinimizedButton {
	background-color: #02031a;
    border-radius: 0px;

}

#ExitButton:hover, #MinimizedButton:hover {
    background-color: red;
    color: white;
    font-size: 13px;

}
#Reset_Button {
    border-radius: 1px;
    background-color: white;
    color: black;
}
#Reset_Button:hover {
    background-color: black;
    color: #ff0841;
}
#Reset_Button:pressed {
    background-color: #ff0841;
    color: white;
}

QRadioButton {
    color: #f0edee;
    border: none;
    border-radius: 10px;
    font-size: 12px;
}

QRadioButton::indicator {
    width: 12px;
    height: 12px;
    background-color: #ebdfcc;
    border-radius: 4px;

}

QRadioButton::indicator:hover {
    background-color: #b10c43;
}

QRadioButton::indicator:pressed {
    background-color: #021b2b;
}


QRadioButton::indicator:checked {
    background-color: #ff0841;
}

QRadioButton::indicator:checked:hover {
    background-color: #b10c43;
}
QRadioButton::indicator:checked:pressed {
    background-color: #021b2b;
}


QCheckBox {
    color: #ebdfcc;
}

QCheckBox::indicator {
    width: 12px;
    height: 12px;
    border-radius: 3px;
    background-color: snow;
}

QCheckBox::indicator:hover {
    background-color: #b10c43;

}

QCheckBox::indicator:pressed {
    background-color: #ff0841;

}

QCheckBox::indicator:checked {
    background-color: #ff0841; 
}

QCheckBox::indicator:checked:hover {
    background-color: #b10c43;

}

QCheckBox::indicator:checked:pressed {
    background-color: #021b2b;

}

QLineEdit {
    background-color: #ebdfcc;
    color: #02031a;
    border: none;
    padding: 4px;
    border-radius: 7px;
}

QLineEdit:hover {
    background-color: #eee4d3;
}

QLineEdit:pressed {
    background-color: #ff0841;
}

#port_auto {
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}
#ValuesLines {
    background-color: #f0f0f0;
    border-radius: 5px;
}

QTabWidget {
    border: none;
}

QVBoxLayout {
    background-color: red;
}

QTabWidget::pane {
    border-top: 0px;
}

QTabBar::tab {
    background-color: #021b2b;
    color: #f0edee;
    padding:10px;
    padding-left: 50px;
    padding-right: 50px;
    border-top-right-radius: 2px;

}

QTabBar::tab:selected {
    background-color: #ff0841;
    color: #f0edee;
}

QTabBar::tab:hover {
    background-color: #b10c43;
    color: #f0edee;
}


QTabBar::tab:pressed {
    background-color: #b10c43;
    color: #f0edee;
}

QSlider {
    height: 6px;
    border-radius: 3px;
}



QSlider::handle:horizontal {
    background: white;
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #021b2b;
    border-radius: 5px;
}

QSlider::sub-page:horizontal {
	background-color: #b10c43;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;

}

QSlider::handle:hover {
    background: #ff0841;
}
QSlider::handle:pressed {
    background: #ebdfcc;
}


QSlider::handle:horizontal:disabled,
QSlider::handle:vertical:disabled {
    background: #ff0841;
}

QSlider::groove:horizontal:disabled,
QSlider::groove:vertical:disabled {
    background: #021b2b;
}

QComboBox {
    background-color: #021b2b;
    color: #f0edee;
    border: none;
    padding: 5px;
    border-radius: 5px;
    selection-background-color: #b10c43;
}

QComboBox:hover {
    background-color: #ff0841;
}

QComboBox:pressed {
    background-color: #b10c43;
    color: #f0edee;
}

QComboBox QAbstractItemView {
    background-color: #021b2b;
    color: #f0edee;
    selection-background-color: #b10c43;
    border: none;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #b10c43;
}

QComboBox::drop-down {
    width: 13px;
    background-color: #ff0841;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

QComboBox::drop-down:hover {
	width: 13px;
	background-color: #ebdfcc;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

QLabel {
    color: white;
    font-size: 15px;
}

QScrollArea {
    border-radius: 10px;
}

#FindDevicescontent {
    background-color: #021b2b;
    border-radius: 4px;
}

QGroupBox {
    background-color:  #0b0321;
    border: None;
    border-radius: 5px;
    
}

QScrollBar:vertical {
    background-color: #0b0321;
}

QScrollBar::handle:vertical {
    background-color: #ebdfcc;
    border-radius: 8px;
}

QScrollBar::handle:vertical:hover {
    background-color: #b10c43;
}

QScrollBar::handle:vertical:pressed {
    background-color: #ff0841;
}

QScrollBar::sub-line:vertical,
QScrollBar::add-line:vertical {
    background: none;
}

QScrollBar::sub-page:vertical,
QScrollBar::add-page:vertical {
    background: none;
}
"""

white_theme = """
QMainWindow {
	background-color: #f0edee;
}

QWidget {
	background-color: #f0edee;
}
QPushButton {
    background-color: #e3dedf;
    color: #000001;
    border: none; 
    border-radius: 5px;
    font-size: 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #0e90ff;
}

QPushButton:pressed {
    background-color: #85c6ff;
    color: #f0edee;
}
QPushButton:disabled {
    background-color: #6f6f6f;
    color: #e6e6e6;
}
#Shell_Button {
    border-radius: 2px;
    font-size: 13px;
}
#Shell_Button:hover {
    background-color: #0e90ff;
}
#Shell_Button:pressed {
    background-color: #85c6ff;
}

#Default_Config_Button, #Github_Button {
    border-radius: 2px;
    font-size: 13px;
}

#Github_Button{
    background-color: white;
    font-size: 12px;
}
#Github_Button:hover {
    background-color: black;
    font-size: 13px;
}
#Github_Button:pressed {
    background-color: #90fcf9;
}

#ThemeButton {
    border-radius: 0px;
    background-color: #f0edee;
    font-size: 13px;
    
}
#ThemeButton:hover {
    color: #ff0841;
}

#ExitButton, #MinimizedButton {
	background-color: transparent;
    border-radius: 0px;

}

#ExitButton:hover, #MinimizedButton:hover {
    background-color: red;
    color: white;
    font-size: 13px;

}

#Reset_Button {
    border-radius: 1px;
    background-color: white;
    color: black;
}
#Reset_Button:hover {
    background-color: black;
    color: #90fcf9;
}
#Reset_Button:pressed {
    background-color: #90fcf9;
    color: black;
}

QRadioButton {
    color: #000001;
    border: none;
    border-radius: 10px;
    font-size: 12px;
}

QRadioButton::indicator {
    width: 12px;
    height: 12px;
    background-color: #BFD9E1;
    border-radius: 4px;

}

QRadioButton::indicator:hover {
    background-color: #0e90ff;
}

QRadioButton::indicator:pressed {
    background-color: #90fcf9;
}


QRadioButton::indicator:checked {
    background-color: #40A5FE;
}

QRadioButton::indicator:checked:hover {
    background-color: #0e90ff;
}
QRadioButton::indicator:checked:pressed {
    background-color: #90fcf9;
}

QCheckBox {
    color: #000001;
}

QCheckBox::indicator {
    width: 12px;
    height: 12px;
    border-radius: 3px;
    background-color: #BFD9E1;
}

QCheckBox::indicator:hover {
    background-color: #85c6ff;

}

QCheckBox::indicator:pressed {
    background-color: #90fcf9;

}

QCheckBox::indicator:checked {
    background-color: #40A5FE; 
}

QCheckBox::indicator:checked:hover {
    background-color: #0e90ff;

}

QCheckBox::indicator:checked:pressed {
    background-color: #90fcf9;

}

QLineEdit {
    background-color: #F7FDFF;
    color: #000001;
    border: none;
    padding: 4px;
    border-radius: 7px;
}

QLineEdit:hover {
    background-color: #E6EEF0;
}

QLineEdit:pressed {
    background-color: #E6EEF0;
}

#port_auto {
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    background-color: #DBE5E8;
}
#port_auto:hover {
    background-color: #CAD7DC;
}
#ChargeValuesLines {
    background-color: #F7FDFF;
    border-radius: 5px;
}
QTabWidget {
    border: none;
}

QTabWidget::pane {
    border-top: 0px;
}

QTabBar::tab {
    background-color: #e3dedf;
    color: #000001;
    padding:10px;
    padding-left: 50px;
    padding-right: 50px;
    border-top-right-radius: 2px;

}

QTabBar::tab:hover {
    background-color: #0e90ff;
    color: #f0edee;
}

QTabBar::tab:selected {
    background-color: #85c6ff;
    color: #f0edee;
}

QTabBar::tab:pressed {
    background-color: #90fcf9;
    color: #000001;
}

QSlider {
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #0773D2;
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #CAD7DC;
    border-radius: 5px;
}

QSlider::sub-page:horizontal {
	background-color: #6AB9FF;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;

}
QSlider::handle:hover {
    background: #6EFAFB;
}
QSlider::handle:pressed {
    background: #0482c0;
}

QSlider::handle:horizontal:disabled,
QSlider::handle:vertical:disabled {
    background: #ff0841;
}

QSlider::groove:horizontal:disabled,
QSlider::groove:vertical:disabled {
    background: #021b2b;
}

QComboBox {
    background-color: #CCD8E3;
    color: #000001;
    border: none;
    padding: 5px;
    border-radius: 5px;
    selection-background-color: #CCD8E3;
}

QComboBox:hover {
    background-color: #0e90ff;
    color: #f0edee;
}

QComboBox:pressed {
    background-color: #85c6ff;
    color: #f0edee;
}

QComboBox QAbstractItemView {
    background-color: #CCD8E3;
    color: #000001;
    selection-background-color: #85c6ff;
    border: none;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #90fcf9;
}

QComboBox::drop-down {
    width: 13px;
    background-color: #0e90ff;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

QComboBox::drop-down:hover {
	width: 13px;
	background-color: #90fcf9;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

QLabel {
    background-color: transparent;
    color: #000001;
    font-size: 15px;
}

QScrollArea {
    border-radius: 10px;
}

#FindDevicescontent {
    background-color: #DBDBDB;
    border-radius: 4px;
}

QGroupBox {
    background-color: #EBF4F5;
    border: None;
    border-radius: 5px;
    
}

QScrollBar:vertical {
    background-color: #C6D1D4;
}

QScrollBar::handle:vertical {
    background-color: #F3FEFF;
    border-radius: 8px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00BBEA;
}

QScrollBar::handle:vertical:pressed {
    background-color: #3FD9FF;
}

QScrollBar::sub-line:vertical,
QScrollBar::add-line:vertical {
    background: none;
}

QScrollBar::sub-page:vertical,
QScrollBar::add-page:vertical {
    background: none;
}
"""

black_theme_Alerts = """
QWidget {
	background-color: #020421;
}

QLabel {
    color: white;
    font-size: 15px;
    background-color: transparent;
}

QPushButton {
    background-color: #021f31;
    color: #f0edee;
    border-radius: 5px;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-right: 50px;
    padding-left: 50px;
    font-size: 10px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #b10c43;
}

QPushButton:pressed {
    background-color: #ff0841;
    color: #f0edee;
}
QPushButton:disabled {
    background-color: #6f6f6f;
    color: #e6e6e6;
}
QLineEdit {
    background-color: #ebdfcc;
    color: #02031a;
    border: none;
    padding: 4px;
    border-radius: 7px;
}

QLineEdit:hover {
    background-color: #eee4d3;
}

QLineEdit:pressed {
    background-color: #ff0841;
}

#SelectDeviceButton {
    padding: 0px;
    font-size: 9px;
    border-radius: 0px;
}
#DeviceBoxDisconnect, #DeviceBoxNative {
    border-radius: 3px;
    background-color: #021b2b;
    color: transparent;

}
QScrollArea {
    border: none;
}

QScrollBar:vertical {
    background-color: #0b0321;
}

QScrollBar::handle:vertical {
    background-color: #ebdfcc;
    border-radius: 8px;
}

QScrollBar::handle:vertical:hover {
    background-color: #b10c43;
}

QScrollBar::handle:vertical:pressed {
    background-color: #ff0841;
}

QScrollBar::sub-line:vertical,
QScrollBar::add-line:vertical {
    background: none;
}

QScrollBar::sub-page:vertical,
QScrollBar::add-page:vertical {
    background: none;
}
"""

white_theme_Alerts = """
QWidget {
	background-color: #f0edee;
}

QLabel {
    color: #000001;
    font-size: 15px;
    background-color: transparent;
}

QPushButton {
    background-color: #e3dedf;
    color: #000001;
    border-radius: 5px;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-right: 50px;
    padding-left: 50px;
    font-size: 10px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #0e90ff;
}

QPushButton:pressed {
    background-color: #85c6ff;
    color: #f0edee;
}
QPushButton:disabled {
    background-color: #6f6f6f;
    color: #e6e6e6;
}
QLineEdit {
    background-color: #F7FDFF;
    color: #000001;
    border: none;
    padding: 4px;
    border-radius: 7px;
}

QLineEdit:hover {
    background-color: #E6EEF0;
}

QLineEdit:pressed {
    background-color: #E6EEF0;
}

#SelectDeviceButton {
    padding: 0px;
    font-size: 9px;
    border-radius: 0px;
}

#DeviceBoxDisconnect, #DeviceBoxNative {
    border-radius: 3px;
    background-color: #CCD8E3;
    color: transparent;

}
QScrollArea {
    border: none;
}


QScrollBar:vertical {
    background-color: #0b0321;
}

QScrollBar::handle:vertical {
    background-color: #ebdfcc;
    border-radius: 8px;
}

QScrollBar::handle:vertical:hover {
    background-color: #b10c43;
}

QScrollBar::handle:vertical:pressed {
    background-color: #ff0841;
}

QScrollBar::sub-line:vertical,
QScrollBar::add-line:vertical {
    background: none;
}

QScrollBar::sub-page:vertical,
QScrollBar::add-page:vertical {
    background: none;
}
"""