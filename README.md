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
