# Note: For this tutorial--> Ubuntu 24.04 - Driver Version: 580.142 - RTX 5090 - ROS2 Jazzy - IsaacSim 5.1


cd ~
git clone https://github.com/isaac-sim/IsaacSim-ros_workspaces.git

cd ~/IsaacSim-ros_workspaces/jazzy_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash

ros2 pkg list | grep isaac_tutorials

echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "source ~/IsaacSim-ros_workspaces/jazzy_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo apt update
sudo apt install -y ros-jazzy-ackermann-msgs

source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

#verify
dpkg -l | grep ackermann

ros2 interface show ackermann_msgs/msg/AckermannDriveStamped


# optional: if you want to install the packahes in your ros workspace
cp -r ~/IsaacSim-ros_workspaces/jazzy_ws/src/isaac_tutorials ~/ros2_ws/src/
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select isaac_tutorials
source install/setup.bash

#verify
ros2 topic list
   #/parameter_events
   #/rosout



