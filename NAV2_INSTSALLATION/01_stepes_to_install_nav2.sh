# Install the ROS 2 binary packages as described in the official docs
# before installing, check if you already have them
which ros2

# if not, you can check the documentation or go to our tutorial to install ROS2
https://docs.ros.org/en/rolling/Installation/Ubuntu-Install-Debs.html

# NOTE: my system uses ubuntu 24.04 and Jazzy

# source your ros2
#NOTE: your path might be different, use the one you got when run which ros2
source /opt/ros/jazzy/setup.bash

# if you want to make the source permanent
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc

# check your workspace direectory
# mine is
/home/borja/ros2_ws

#check first if you already have the packages installed
dpkg -l | grep ros-jazzy-navigation2
dpkg -l | grep ros-jazzy-nav2-bringup

# if installed you can skip next steps
# if not keep going
sudo apt install ros-$ROS_DISTRO-navigation2
sudo apt install ros-$ROS_DISTRO-nav2-bringup