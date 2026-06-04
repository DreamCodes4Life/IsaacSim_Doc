Open IsaacSim 5.1

# In a new stage, create the Flat Grid environment by going to 
Create > Environments > Flat Grid.

# Add the Forklift C robot by going to 
Isaac Sim Assets > ROBOTS > FORKLIFT > forklift_c.

# Create a new action graph by navigating to 
Window > Graph Editors > Action Graph > New Action Graph.

# Add next nodes:
On PlayBack Tick
Isaac Compute Odometry
Ackerman Controller
ROS2 Subscribe AckermanDrive



