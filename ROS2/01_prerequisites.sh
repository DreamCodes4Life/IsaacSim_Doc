Ubuntu 24.04 → best for ROS 2 Jazzy Jalisco
Ubuntu 22.04 → commonly used with older Isaac Sim releases

ROS 2 Jazzy Installed

Colcon Build Tools

rosdep

Git

NVIDIA Driver
RTX-capable GPU
Modern NVIDIA driver (often 550+ for recent versions)

Isaac Sim Installed

Python Environment Compatibility

Create ROS 2 Workspace

Source ROS 2 Before Building

Install Isaac ROS Tutorial Workspace

#Dependencies
sudo apt install \
python3-pip \
python3-colcon-common-extensions \
python3-rosdep \
python3-vcstool \
build-essential

# install laserscan
sudo apt update
sudo apt install ros-jazzy-pointcloud-to-laserscan

# source it again
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/IsaacSim-ros_workspaces/jazzy_ws/install/setup.bash

#Furder with controllers and more available tutorials
# we will create a new workspace here

#check if already installed
ros2 interface package ackermann_msgs

#If not, install it
sudo apt update
sudo apt install -y ros-jazzy-ackermann-msgs

#Source Ros
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

#download packages for tutorials ROS
cd ~
git clone https://github.com/isaac-sim/IsaacSim-ros_workspaces.git

sudo rosdep init
rosdep update