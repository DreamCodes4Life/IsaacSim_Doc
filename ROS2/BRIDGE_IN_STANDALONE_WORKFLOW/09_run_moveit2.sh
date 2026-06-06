#set a new clean terminal
env -i \
HOME="$HOME" \
USER="$USER" \
DISPLAY="$DISPLAY" \
XAUTHORITY="$XAUTHORITY" \
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
bash --noprofile --norc

cd ~/isaac-sim #or your isaacsim name directory

export ROS_DISTRO=jazzy
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export LD_LIBRARY_PATH=$HOME/isaac-sim/exts/isaacsim.ros2.bridge/jazzy/lib

./python.sh standalone_examples/api/isaacsim.ros2.bridge/moveit.py

# in a separated terminal
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0
ros2 topic list

# results
/clock
/isaac_joint_commands
/isaac_joint_states
/parameter_events
/rosout


# monitor the topics
ros2 topic echo /clock
ros2 topic echo /isaac_joint_states
ros2 topic info /isaac_joint_commands

# to open the python example
code standalone_examples/api/isaacsim.ros2.bridge/moveit.py