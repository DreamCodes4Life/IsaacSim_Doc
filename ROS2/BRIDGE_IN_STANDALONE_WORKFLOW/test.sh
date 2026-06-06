#to test
# check ROS2 topic list in a terminal

ros2 topic list

#results should be
/parameter_events
/rosout

#set the Domain
export ROS_DOMAIN_ID=1

#click play
play

# open ActionGraph
select node "On Impulse Event"
Inputs -> click send event

# check again
ros2 topic list

#results should be
/clock
/parameter_events
/rosout
