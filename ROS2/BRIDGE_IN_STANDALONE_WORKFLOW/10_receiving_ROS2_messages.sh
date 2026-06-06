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

./python.sh standalone_examples/api/isaacsim.ros2.bridge/subscriber.py

# open a new terminal and run
ros2 topic pub -r 1 /move_cube std_msgs/msg/Empty

# you can verify in isaacsim the cube is moving


# to open the python example
code standalone_examples/api/isaacsim.ros2.bridge/subscriber.py