#Add a 2D RTX Lidar sensor by going to 
Create > Sensors > RTX Lidar > NVIDIA > Example Rotary 2D 
#and drag it under 
/mock_robot/base_link/lidar_link.

#Add a Hawk stereo camera system by going to 
Create > Sensors > Camera and Depth Sensors > LeopardImaging > Hawk 
#and drag it under 
/mock_robot/base_link/camera_link.

#Create a Generic Publisher by going to 
Tools > Robotics > ROS 2 OmniGraphs > Generic Publisher. 
#Set Generic Publisher Graph as Publish String and the 
Graph Path to /mock_robot/base_link/wheel_left/String_graph. 
hit OK.

#Create a TF Publisher by going to 
Tools > Robotics > ROS 2 OmniGraphs > TF Publisher. 
Set the Target Prim to /mock_robot  
Graph Path to /mock_robot/base_link/wheel_left/TF_graph. 
hit OK.

#Create a Camera Publisher by going to 
Tools > Robotics > ROS 2 OmniGraphs > Camera. 
Camera Prim to /mock_robot/base_link/camera_link/Hawk/left/camera_left 
Graph Path to /mock_robot/base_link/camera_link/Hawk/Camera_Left_Graph. 
Uncheck the Depth topic and 
hit OK.

#Create a second Camera Publisher by going to 
Tools > Robotics > ROS 2 OmniGraphs > Camera. 
Camera Prim to /mock_robot/base_link/camera_link/Hawk/right/camera_right 
Graph Path to /mock_robot/base_link/camera_link/Hawk/Camera_Right_Graph. 
Uncheck the Depth topic 
hit OK.

#Create a 2D RTX Lidar Publisher by going to 
Tools > Robotics > ROS 2 OmniGraphs > RTX Lidar. 
Lidar Prim to /mock_robot/base_link/lidar_link/Example_Rotary_2D 
Graph Path to /mock_robot/base_link/lidar_link/Lidar_Graph. 
only Laser Scan is enabled 
hit OK.


click play

#test in terminal
ros2 topic list