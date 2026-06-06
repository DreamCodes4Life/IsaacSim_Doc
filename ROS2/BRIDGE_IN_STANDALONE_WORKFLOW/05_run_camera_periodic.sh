# edit the example or run your own. we are just adding a node for context with the other script 05...
code ~/isaac-sim/standalone_examples/api/isaacsim.ros2.bridge/camera_periodic.py

# run from terminal in your isaacsim folder
./python.sh standalone_examples/api/isaacsim.ros2.bridge/camera_periodic.py

# if you have a missmatch versions with python open a new clean terminal
env -i \
HOME="$HOME" \
USER="$USER" \
DISPLAY="$DISPLAY" \
XAUTHORITY="$XAUTHORITY" \
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
bash --noprofile --norc

#in another terminal review topics
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=1
ros2 topic list