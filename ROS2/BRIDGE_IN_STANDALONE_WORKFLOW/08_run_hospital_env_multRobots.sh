# from clean shell:
env -i \
HOME="$HOME" \
USER="$USER" \
DISPLAY="$DISPLAY" \
XAUTHORITY="$XAUTHORITY" \
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
bash --noprofile --norc

cd ~/isaac-sim #check the name of your folder

export isaac_sim_package_path=$HOME/isaac-sim
export ROS_DISTRO=jazzy
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export LD_LIBRARY_PATH=$isaac_sim_package_path/exts/isaacsim.ros2.bridge/jazzy/lib

./python.sh standalone_examples/api/isaacsim.ros2.bridge/carter_multiple_robot_navigation.py --environment hospital

#it may take some time the firs time you load the usd
#this test just showcase how to open a usd scene

# to open the python example
code standalone_examples/api/isaacsim.ros2.bridge/carter_multiple_robot_navigation.py

