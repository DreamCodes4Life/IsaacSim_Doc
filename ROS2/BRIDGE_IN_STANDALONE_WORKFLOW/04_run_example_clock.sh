# run from terminal in your isaacsim folder
./python.sh standalone_examples/api/isaacsim.ros2.bridge/clock.py

# if you have a missmatch versions with python open a new clean terminal
env -i \
HOME="$HOME" \
USER="$USER" \
DISPLAY="$DISPLAY" \
XAUTHORITY="$XAUTHORITY" \
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
bash --noprofile --norc

# inside that shell run
cd ~/isaac-sim

export isaac_sim_package_path=$HOME/isaac-sim
export ROS_DISTRO=jazzy
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export LD_LIBRARY_PATH=$isaac_sim_package_path/exts/isaacsim.ros2.bridge/jazzy/lib

./python.sh standalone_examples/api/isaacsim.ros2.bridge/clock.py


# in another tab run
ros2 topic echo /sim_time
ros2 topic echo /manual_time

#NOTE: if you dont see the clock, run again the clock.py