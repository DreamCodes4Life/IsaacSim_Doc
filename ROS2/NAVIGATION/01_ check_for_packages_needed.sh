source /opt/ros/jazzy/setup.bash

#check for packages in ROS 2
ros2 pkg prefix carter_navigation
ros2 pkg prefix iw_hub_navigation
ros2 pkg prefix isaac_ros_navigation_goal

#exa,mple missing packages:
# carter_navigation         found
# iw_hub_navigation         not found
# isaac_ros_navigation_goal not found

#they might exist within isaac
source ~/IsaacSim-ros_workspaces/jazzy_ws/install/setup.bash

#check again
ros2 pkg prefix carter_navigation
ros2 pkg prefix iw_hub_navigation
ros2 pkg prefix isaac_ros_navigation_goal

# If iw_hub_navigation is still not found, verify it was installed
ls ~/IsaacSim-ros_workspaces/jazzy_ws/install | grep navigation

#if missin packages
# note, you can install them in a different workspace too
# we just make sure the command ros2 can see these packages
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select isaac_ros_navigation_goal iw_hub_navigation carter_navigation
source install/setup.bash
ros2 pkg list | grep -E "carter_navigation|iw_hub_navigation|isaac_ros_navigation_goal"