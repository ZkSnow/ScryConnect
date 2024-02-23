# ScryConnect :globe_with_meridians:
ScryConnet is an interface made with `PyQt5` for the screen mirroring program `Scrcpy`, which focuses on making it easier to use, with features thinking about usability and practicality for the user.

## Requiriments :toolbox:
Make sure you have `Scrcpy` and `ADB` installed correctly before continuing
[Scrcpy Repository](https://github.com/Genymobile/scrcpy).

```
python 3.10 or newer
psutil==5.9.6
PyQt5==5.15.10
```
Install the dependencies with `pip install -r requiriments.txt` and start the program with `python start.py` ↓ 
```
pip install -r requirements.txt
python start.py
```
### :rotating_light: Known Linux Problems :rotating_light:

When using ScryConnect on Linux, you may encounter the following known issues:

### 1.  **Ignoring XDG_SESSION_TYPE=wayland in Gnome:**
   If you are using the Gnome desktop environment, you may encounter a warning similar to this one
   To fix this, you can install the `libxcb-xinerama0` package by running the following command:
`sudo apt-get install libxcb-xinerama0`

### 2. **Python error: source code cannot contain null bytes:**
   If you encounter an error related to **null bytes** in the `Python` source code, you can correct it by running the following command on any file that is generating the error: `sed -i 's/\x0//g' FileName`

# UI Features :milky_way:

### Connection Features :twisted_rightwards_arrows:
This ui allows you to connect your devices in **3** different ways:

* **Manual saved connection**
  * This UI allows you to save connections from different `IP:PORT` for quick access from different devices ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/ea3f1100-a0dd-4260-99f5-a1ccac52e4fc
    
* **Manual connection by text line**
  * If you don't want to save, just type `IP:PORT` in the text lines and simply connect, no need to save or anything, great for testing 
`IP:PORT` before saving ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/5b64ae11-4617-4d38-a5a2-d1f0a4536f98
     
* **Connection auto-detection of devices**
  * If you don't feel like typing in IPs, no problem! You can simply click the **Detect Devices** button and the program will automatically detect all valid devices, display them in the *UI* so that you can connect ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/b0d0ab9b-4dbd-4449-889b-a298a345cdf4

* **Disconnect device**
  * This UI allows you to disconnect a device just by choosing it without having to type anything ↓ 

    https://github.com/ZkSnow/ScryConnect/assets/128258706/ec252df4-2182-477f-b9d6-0c39b13fa238

### Start Scrcpy Features :white_check_mark:
There are two ways to start `Scrcpy` and some utilities to speed up the process of starting it.

* **Start with UI**
  * When you start `Scrcpy` using the UI, you don't have to type in practically anything, you just have to drag sliders and activate or deactivate features, so that the desired configuration for the program is achieved in a more practical way.
is achieved in a more practical way ↓
  
    https://github.com/ZkSnow/ScryConnect/assets/128258706/4ac9ac98-d3cc-4417-98ee-56f8f2bc5e36

* **Saving configuration presets**
  * Changing each of these elements or writing them down several times for each need can be tiresome, but don't worry, this UI has the solution! Here you can simply save different configuration presets for different scenarios, making everything faster and easier ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/ddcc1584-1a8f-441d-bdd8-184f08691866

* **Start Custom Args**
  * So you still prefer to write? no problem! just use the **Custom** text line and manually write all the `--args` you want and start directly from the UI, this
line of text is also saved in the presets, so you can save several of them freely ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/5dd81723-2c22-46a0-989b-23edd56e13ee

* **Starting the device shell directly from the UI**
  * Need to access your Android's Shell? Well, you can do that in this UI, just by clicking the :computer: button and choosing the device to open your 
device ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/1f85fd86-f744-4a22-8258-66143d349390

### Config Features :wrench:
Here you can change the scrcpy versions, choose where to save the video files or even change the resolution of the devices.

* **Multiple Scrcpy Versions (WINDOWS ONLY)**
  * This UI allows you to use different versions of `Scrcpy` by saving the folders of different versions and allowing you to choose which one to use to start it ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/635f6498-8409-4365-af3f-5068fe7e90bb

* **Custom Resolution**
  * Using the `wm size` command, this UI allows you to change the resolution of the device to a different resolution that is ***valid***, if a non-compatible resolution is not chosen.   
chosen, the device will turn off and on, if you want to return to the resolution, just click on the **Native Resolution** button ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/2dd92a0c-afc5-4f8c-8203-4841ca7c8921

* **Path to Save Recording**
  * This UI allows you to choose where `scrcpy` recordings will be saved, or simply leave it as the default and save them in the version folder ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/cf728815-728f-4762-be00-02abbc191c7c

### Extra Features :sparkles:
* **Themes**
  * This UI allows you to choose between two themes ***Dark/White*** to allow you to choose the one you like best! ↓
 
    https://github.com/ZkSnow/ScryConnect/assets/128258706/e598659c-3bd1-46d6-9ac1-826f719d27bf

* **Reset Server**
  * This UI allows you to turn the `ADB` server off and on with one click to troubleshoot possible server problems ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/7dfe14be-02b6-477b-83b5-ee67fbf2415c

* **Stop All Scrcpy**
  * You can close all instances of `scrcpy` that are running, for example if you have several mirrors open with a single click you can close them all :rotating_light: this option will corrupt videos that are being **recorded** by the affected `scrcpy` :rotating_light: ↓

    https://github.com/ZkSnow/ScryConnect/assets/128258706/3c6795af-81f4-4fc5-be62-d45115bf45c7

### Scrcpy Shortcuts
When screen mirroring starts, you can use the following shortcuts to speed things up :D ↓

 Action                                      |   Shortcut
 | ------------------------------------------- |:-----------------------------
 | Switch fullscreen mode                      | <kbd>MOD</kbd>+<kbd>f</kbd>
 | Rotate display left                         | <kbd>MOD</kbd>+<kbd>←</kbd> _(left)_
 | Rotate display right                        | <kbd>MOD</kbd>+<kbd>→</kbd> _(right)_
 | Flip display horizontally                   | <kbd>MOD</kbd>+<kbd>Shift</kbd>+<kbd>←</kbd> _(left)_ \| <kbd>MOD</kbd>+<kbd>Shift</kbd>+<kbd>→</kbd> _(right)_
 | Flip display vertically                     | <kbd>MOD</kbd>+<kbd>Shift</kbd>+<kbd>↑</kbd> _(up)_ \| <kbd>MOD</kbd>+<kbd>Shift</kbd>+<kbd>↓</kbd> _(down)_
 | Resize window to 1:1 (pixel-perfect)        | <kbd>MOD</kbd>+<kbd>g</kbd>
 | Resize window to remove black borders       | <kbd>MOD</kbd>+<kbd>w</kbd> \| _Double-left-click¹_
 | Click on `HOME`                             | <kbd>MOD</kbd>+<kbd>h</kbd> \| _Middle-click_
 | Click on `BACK`                             | <kbd>MOD</kbd>+<kbd>b</kbd> \| <kbd>MOD</kbd>+<kbd>Backspace</kbd> \| _Right-click²_
 | Click on `APP_SWITCH`                       | <kbd>MOD</kbd>+<kbd>s</kbd> \| _4th-click³_
 | Click on `MENU` (unlock screen)⁴            | <kbd>MOD</kbd>+<kbd>m</kbd>
 | Click on `VOLUME_UP`                        | <kbd>MOD</kbd>+<kbd>↑</kbd> _(up)_
 | Click on `VOLUME_DOWN`                      | <kbd>MOD</kbd>+<kbd>↓</kbd> _(down)_
 | Click on `POWER`                            | <kbd>MOD</kbd>+<kbd>p</kbd>
 | Power on                                    | _Right-click²_
 | Turn device screen off (keep mirroring)     | <kbd>MOD</kbd>+<kbd>o</kbd>
 | Turn device screen on                       | <kbd>MOD</kbd>+<kbd>Shift</kbd>+<kbd>o</kbd>
 | Rotate device screen                        | <kbd>MOD</kbd>+<kbd>r</kbd>
 | Expand notification panel                   | <kbd>MOD</kbd>+<kbd>n</kbd> \| _5th-click³_
 | Expand settings panel                       | <kbd>MOD</kbd>+<kbd>n</kbd>+<kbd>n</kbd> \| _Double-5th-click³_
 | Collapse panels                             | <kbd>MOD</kbd>+<kbd>Shift</kbd>+<kbd>n</kbd>
 | Copy to clipboard⁵                          | <kbd>MOD</kbd>+<kbd>c</kbd>
 | Cut to clipboard⁵                           | <kbd>MOD</kbd>+<kbd>x</kbd>
 | Synchronize clipboards and paste⁵           | <kbd>MOD</kbd>+<kbd>v</kbd>
 | Inject computer clipboard text              | <kbd>MOD</kbd>+<kbd>Shift</kbd>+<kbd>v</kbd>
 | Enable/disable FPS counter (on stdout)      | <kbd>MOD</kbd>+<kbd>i</kbd>
 | Pinch-to-zoom                               | <kbd>Ctrl</kbd>+_click-and-move_
 | Drag & drop APK file                        | Install APK from computer
 | Drag & drop non-APK file                    | Push file to device

## License
The license used for this UI is the **Apache License 2.0** ↓
```
  Copyright (C) 2025 ZkSnow
  
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  
      http://www.apache.org/licenses/LICENSE-2.0
  
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
```

