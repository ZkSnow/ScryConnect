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
                               None,
                               None,
                               None,
                               ],
            "Slider_Value": [60, 1000, 8, 0, 0, 0, 0, 0],
            "Indexs_Combox": [0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Check_Boxes": [False, False, False,
                            False, False, False, False,
                            False, False, False, False, False,
                            False, False, False, False, False,
                            False, False, False, False, False,
                            False, False, False, False, False,
                            False, False, False],
                },
        
        "ConfigTAB": {
            "Index_Combox": [0, 0, 0],
            },
        },
    }

ARGS_LIST = {
    "scrcpy_2.0": {
        "Version": 2.0,
        "no audio": " --no-audio",
        "no video": " --no-video",
    },
    
    "scrcpy_2.1": {
        "Version": 2.1,
        "no playback": " --no-playback",

    },
    
    "scrcpy_2.5": {
        "Version": 2.5,
        "no mouse hover": " --no-mouse-hover",
    },
    "scrcpy_2.7": {
        "Version": 2.7,
        
        "gamepad": " -G",
        "gamepad otg": " -G --otg",
    },
    
    "scrcpy_3.1": {
        "Version": 3.1,
        
        "no vd destroy": " --no-vd-destroy-content"
    },
    "all_version": {
        "prefer text": " --prefer-text",
        "no k repeat": " --no-key-repeat",
        "raw k events": " --raw-key-events",
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
            
        "Microphone": " --audio-source=mic",
    },
    
    "scrcpy_2.3": {
        "Version": 2.3,
        
        "(flac) C2 Android Flac Encoder": " --audio-codec=flac --audio-encoder=c2.android.flac.encoder",
        "(flac) OMX Google Flac Encoder": " --audio-codec=flac --audio-encoder=OMX.google.flac.encoder",
    },
    "scrcpy_2.6": {
        "Version": 2.6,
        
        "Playback" : " --audio-source=playback",
        "Audio Dup": " --audio-dup",
        "Audio Dup + Playback": " --audio-dup --audio-source=playback",
    },
    
    "scrcpy_3.0": {
        "Version": 3.0,
        
        "0° Degrees": " --capture-orientation=@0",
        "90° Degrees": " --capture-orientation=@90",
        "180° Degrees": " --capture-orientation=@180",
        "270° Degrees": " --capture-orientation=@270",
        "Flip 0° Degrees": " --capture-orientation=@flip0",
        "Flip 90° Degrees": " --capture-orientation=@flip90",
        "Flip 180° Degrees": " --capture-orientation=@flip180",
        "Flip 270° Degrees": " --capture-orientation=@flip270",
    },
    "scrcpy_3.1": {
        "Version": 3.1,
        
        "(av1) C2 Android Av1 Encoder" : " --video-encoder=c2.android.av1.encoder --video-codec=av1",
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
        
        "(h264) C2 Mtk Avc Encoder" : " --video-encoder=c2.mtk.avc.encoder --video-codec=h264",
        "(h264) C2 Android Avc Encoder" : " --video-encoder=c2.android.avc.encoder --video-codec=h264",
        "(h264) OMX Google H264 Encoder" : " --video-encoder=OMX.google.h264.encoder --video-codec=h264",
        "(h264) OMX MTK VIDEO ENCODER AVC": " --video-encoder=OMX.MTK.VIDEO.ENCODER.AVC --video-codec=h264",
        "(h265) C2 Mtk Hevc Encoder" : " --video-encoder=c2.mtk.hevc.encoder --video-codec=h265",
        "(h265) OMX MTK VIDEO ENCODER HEVC" : " --video-encoder=OMX.MTK.VIDEO.ENCODER.HEVC --video-codec=h265",
        "(opus) C2 Android Opus Encoder": " --audio-codec=opus --audio-encoder=c2.android.opus.encoder",   
        "(aac) C2 Android Aac Encoder": " --audio-codec=aac --audio-encoder=c2.android.aac.encoder",
        "(aac) OMX Google Aac Encoder": " --audio-codec=aac --audio-encoder=OMX.google.aac.encoder",
    },
    "deprecated_args": {
        "limit_2.2": {
            "Version": 2.2,
            
            "0° Degrees": " --lock-video-orientation=0",
            "90° Degrees": " --lock-video-orientation=1",
            "180° Degrees": " --lock-video-orientation=2",
            "270° Degrees": " --lock-video-orientation=3",
        },
        "limit_2.7": {
            "Version": 2.7,

            "fwd all clicks": " --forward-all-clicks",
            
            "0° Degrees": " --lock-video-orientation=0",
            "90° Degrees": " --lock-video-orientation=90",
            "180° Degrees": " --lock-video-orientation=180",
            "270° Degrees": " --lock-video-orientation=270", 
        },
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
            (3, 2, 1, 2),
            (3, 1),
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
            (11, 0, 1, 2),
            (12, 0, 1, 2),
            (13, 0),
            (14, 0, 1, 2),
            (15, 0),
            (16, 0, 1, 2),
            (17, 0),
            (18, 0, 1, 2),
            (19, 0, 1, 2),
            (20, 0, 1, 2),
            (0, 4),
            (1, 4, 1, 2),
            (2, 4),
            (3, 4, 1, 2),
            (4, 4),
            (4, 5),
            (5, 4, 1, 2),
            (6, 4, 1, 2),
            (7, 4, 1, 2),
            (8, 4),
            (9, 4, 1, 2),
            (10, 4),
            (11, 4, 1, 2),
            (12, 4, 1, 2),
            (13, 4),
            (13, 5),
            (14, 4, 1, 2),
            (15, 4),
            (15, 5),
            (16, 4, 1, 2),
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
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
            (6, 0, 1, 5),
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
