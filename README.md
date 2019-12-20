# CryoPALM

This program is made to control a microscopy setup aimed at imaging biological samples via PALM technique.
It allows to control the microscope (DM6000 from Leica), the camera (Hamamatsu Orca Flash v4.0 LT) and the lasers (Errol modified).
The microscope and the camera are controlled via the micromanager API and the lasers are controlled via communication with an Arduino board.

It allows to :

- Change microscope settings  
- Change camera settings  
- Acquire and display images in live or snapshot modes with grey levels histogram  
- Save acquired images  
- Find the best focus on the imaged area  
- Control the different laser powers independently  
- Perform PALM acquisition (single stream or batch)  

# Installation instructions
1. Install [Micro-manager 2.0 beta](https://valelab4.ucsf.edu/~MM/nightlyBuilds/2.0.0-beta/Windows/MMSetup_64bit_2.0.0-beta3_20171106.exe) (I didn't try with the gamma release).
2. Download those files: https://github.com/zfphil/micro-manager-python3/tree/master/MMCorePy and drop them into your Micro-manager installation folder which should be something like ```C:\Program Files\Micro-Manager-2.0beta```.
3. Run the ```CryoPALMSetup.exe``` and follow the instructions until the installation is complete.
4. In order to use it with the laser controller module, you can check [This project](https://github.com/DocQuantic/SerialControlAnalogOutput) which uses an Arduino to control the laser bench.

# How to use it ?
When you run the program, the Main window will appear (Figure 1). This window is divided in three parts.

![Experiment window](images/MainWindow.jpg "Experiment window")

Figure 1 : Experiment Window

The first one contains all the elements to control the main characteristics of the microscope. It allows to select FLUO or BF mode and then to play with BF light intensity, diaphragms, filters and shutters.

The second one is dedicated to camera control. Exposure time and bining can be modified and it is possible to run acquisition (live or snapshot).

Finally, the last part concerns the PALM acquisition itself. It is possible to modify the number of frames to be acquired and to run single or batch acquisitions. When batch acquisition is selected, it displays the batch acquisition window (Figure 2) which asks for the number of streams in the batch and the save location. By default, during a stream acquisition, only one image over ten will be displayed for speed purpose. Nevertheless, the PALM Acquisition part contains a checkbox to activate a "Fast Mode" which will display each frame acquired. This mode is very usefull to check fluorophore blinking and to adjust experiment parameters such as the laser powers, focus, etc...
