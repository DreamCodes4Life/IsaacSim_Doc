#running this example
https://docs.nav2.org/getting_started/index.html#running-the-example

#use your ros2-distro, for me is:
source /opt/ros/jazzy/setup.bash
echo $ROS_DISTRO

#run
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False

# follow the steps on the tutorial

# if you want to see the launch file
#your path to the workspace might be different
code /opt/ros/jazzy/share/nav2_bringup/launch/tb3_simulation_launch.py