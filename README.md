# CryoPALM
This program is made to control a microscopy setup aimed at imaging biological samples via PALM technique.
It allows to control the microscope (DM6000 from Leica), the camera (Hamamatsu Orca Flash v4.0 LT) and the lasers (Errol modified).
The microscope and the camera are controlled via the micromanager API and the lasers are controlled via communication with an Arduino board.

The program allows to :

-Change microscope settings  
-Change camera settings  
-Acquire images live  
-Acquire images snapshot  
-Save snapshots  
-Find the best focus on the imaged area  
-Display the acquired images  
-Display the corresponding histogram  
-Control the different laser powers independently  
-Perform PALM acquisition (single stream or batch)  

When the program starts, it shows the main experiment wimdow which is divided in 4 main parts.

# Installation instructions
1. Install [Micro-manager 2.0 beta](https://valelab4.ucsf.edu/~MM/nightlyBuilds/2.0.0-beta/Windows/MMSetup_64bit_2.0.0-beta3_20171106.exe) (I didn't try with the gamma release).
2. Download those files: https://github.com/zfphil/micro-manager-python3/tree/master/MMCorePy and drop them into your Micro-manager installation folder which should be something like ```C:\Program Files\Micro-Manager-2.0beta```.
3. Run the ```CryoPALMSetup.exe``` and follow the instructions until the installation is complete.
