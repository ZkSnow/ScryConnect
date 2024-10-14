"""
This module contains the static datas for ScryConnect, 
this includes the keys and other informations that are used in other parts of the program.

The static datas are divided into 4 categories:

- `USERDATA`: Stores user data, such as theme, saved IPs/ports, and connected devices.
- `ARGS_LIST` and `EXTRA_ARGS_LIST`: These are lists of arguments that can be passed to Scrcpy.
- `ERRORS_LIST`: This is a list of some errors codes that can be returned by Scrcpy.
- `LAYOUT_POSITIONS`: Positions of UI elements in layout.


Static datas are data that is constant and does not change during the program runtime.
This includes constants used by the program such as Scrcpy arguments, keys for the `UserData.json` file, and UI element positions.
All of these data are stored in a module so that they can be easily accessed and modified by other parts of the program.
"""
from pathlib import Path
from os.path import join

PATH_DATA_DIR = join(
    Path(__file__).parent.parent.parent.resolve(), # Returns two folders up to the root of the project
    "Data",
)

USERDATA = {
    "Theme_Active": 0,
    
    "Connect": {
                "Custom_Ip_Saved": {},
                "Port_Auto": None,
                "Connect_Devices": [],
            },
    
    "Custom_Config_Set": {},

    "Resolutions": {
                   "Saved_Resolution": {},
                },
    
    "Versions": {
                "Selected_Version": {
                    "Path": "", 
                    "Version": 0.0,
                }, 
                "Saved_Versions": {},
            },
    
    "File_Path_Config": {
                "Path_selected": None,
                "Saved_Path_Files": {},
                "Path_Mode_Radio": [False, True],
            },
    
    "Last_Session_Config": {
        "ConnectTAB": {
                "Ip_Index": 0,
                "LineEdit_Texts": [None,
                                   None],
                    },
        
        "StartTAB": {
            "LineEdit_Texts": [None,
                               None,
                               None,
                               None,
                               None],
            "Slider_Value": [60, 1000, 8, 0, 0, 0],
            "Indexs_Combox": [0, 0, 0, 0, 0, 0, 0],
            "Check_Boxes": [False, False, False,
                            False, False, False, False,
                            False, False, False, False, False,
                            False, False, False, False, False,
                            False, False, False, False, False],
                },
        
        "ConfigTAB": {
            "Index_Combox": [0, 0, 0],
            },
        },
    }

ARGS_LIST = {
    "scrcpy_2.0": {
        "Version": 2.0,
        "audio buffer": " --audio-buffer ",
        "no audio": " --no-audio",
        "no video": " --no-video",
    },
    
    "scrcpy_2.1": {
        "Version": 2.1,
        "time limit": " --time-limit ",
        "no playback": " --no-playback",

    },
    
    "scrcpy_2.2": {
        "Version": 2.2,

    },
    
    "all_version": {
        "record": " -r ",
        "prefer text": " --prefer-text",
        "no k repeat": " --no-key-repeat",
        "raw k events": " --raw-key-events",
        "fwd all clicks": " --forward-all-clicks",
        "video buffer": " --display-buffer ",
        "crop": " --crop ",
        "ctrl sct": " --shortcut-mod=lctrl,rctrl",
        "alt-ctrl sct": " --shortcut-mod=lalt,ralt,lctrl,rctrl",
        "show touches": " --show-touches",
        "no control": " --no-control",
        "fullscreen": " -f",
        "always on top": " --always-on-top",
        "stay awake": " --stay-awake",
        "screen off": " --turn-screen-off",
        "borderless": " --window-borderless",
        "max fps": " --max-fps ",
        "max size": " -m ",
        "orientation": " --lock-video-orientation",
        "otg": " --otg ",
        "bit-rate": " -b ",
    }
}

EXTRA_ARGS_LIST = {
    "scrcpy_2.2": {
        "Version": 2.2,
        
        "Screen": " --video-source=display",
        "Back Camera": " --video-source=camera --camera-facing=back",
        "Front Camera": " --video-source=camera --camera-facing=front",
        "External Camera": " --video-source=camera --camera-facing=external",
            
        "Device Sound": "",
        "Microphone": " --audio-source=mic",
    },
    
    "scrcpy_2.3": {
        "Version": 2.3,
        
        "Initial Orientation": " --lock-video-orientation",
        "Vertical Orientation": " --lock-video-orientation=0",
        "Upside Down": " --lock-video-orientation=180",
        "Horizontal Left": " --lock-video-orientation=270", 
        "Horizontal Right": " --lock-video-orientation=90",
    },
    
    "all_version": {
        "AoA Mouse": " --otg --mouse=aoa",
        "SDK Mouse": " --mouse=sdk",
        "uHid Mouse": " --mouse=uhid",
        "AoA Keyboard": " --otg --keyboard=aoa",
        "SDK Keyboard": " --keyboard=sdk",
        "uHid Keyboard": " --keyboard=uhid",
        "AoA Mouse + Keyboard": " --otg --mouse=aoa --keyboard=aoa",
        "SDK Mouse + Keyboard": " --mouse=sdk --keyboard=sdk",
        "uHid Mouse + Keyboard": " --mouse=uhid --keyboard=uhid",
    },
    "deprecated_args": {
        "limit_2.2": {
            "Version": 2.2,
            
            "Initial Orientation": " --lock-video-orientation",
            "Vertical Orientation": " --lock-video-orientation=0",
            "Upside Down": " --lock-video-orientation=2",
            "Horizontal Left": " --lock-video-orientation=1",
            "Horizontal Right": " --lock-video-orientation=3",
        }
    }
}
 
ERRORS_LIST = {
            "device_not_found": [
                                 "could not find any adb",
                                 "could not find adb device",
                            ],
            
            "args_unexpected": [
                                "unexpected additional arg",
                                "ambiguous option",
                                "unknown option",
                            ],
            
            "value_error": [
                            "illegalargument",
                            "could not parse",
                            "option requires an arg",
                        ],
            }

LAYOUT_POSITIONS = {
    "connect_tab": {
        "upper":[
            (0, 0), 
            (1, 0),
            (1, 1, 1, 3),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (3, 0),
            (3, 1, 1, 3),
            (5, 0),
            (6, 0, 1, 4)
        ],
        
        "lower":[
            (0, 0, 1, 2),
            (1, 0),
        ],
    },
    
    "start_tab": {
        "upper":[
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0, 1, 2),
            (2, 0, 1, 2),
            (3, 0),
            (3, 1),
            (3, 2),
            (1, 2),
            (2, 2),
        ],
            
        "middle":[
            (0, 0),
            (0, 1),
            (1, 0, 1, 2),
            (2, 0),
            (2, 1),
            (3, 0, 1, 2),
            (4, 0),
            (4, 1),
            (5, 0, 1, 2),
            (6, 0),
            (6, 1),
            (7, 0, 1, 2),
            (8, 0),
            (8, 1),
            (9, 0, 1, 2),
            (10, 0),
            (10, 1),
            (11, 0),
            (11, 1),
            (0, 4),
            (1, 4, 1, 2),
            (2, 4),
            (3, 4, 1, 2),
            (4, 4),
            (5, 4, 1, 2),
            (6, 4),
            (7, 4, 1, 2),
            (8, 4),
            (9, 4, 1, 2),
            (10, 4, 1, 2),
            (11, 4),
            (11, 5),
            (12, 4, 1, 2),
            (13, 4),
                ],
                
        "lower":[
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (4, 0, 1, 5),
            ],
    },
    
    "config_tab": {
        "upper":[
            (0, 0),
            (1, 0, 1, 2),
            (2, 0, 1, 2),
            (3, 0),
            (3, 1),
            (4, 0, 1, 2),
            (6, 0),
            (7, 0, 1, 2),
            (8, 0),
            (8, 1),
            (10, 0, 1, 2),
            (11, 0, 1, 2),
            (13, 0),
            (14, 0, 1, 2),
            (15, 0, 1, 2),
            (16, 0),
            (16, 1),
            (17, 0, 1, 2),
        ],
            
        "lower":[
            (0, 0),
            (1, 0),
            (3, 0),
            (4, 0, 1, 2),
            (5, 0, 1, 2),
        ],
    },
}
