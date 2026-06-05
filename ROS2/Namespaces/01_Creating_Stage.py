# Import necessary modules
from pxr import UsdGeom
import omni.usd

# Retrieve the current stage
stage = omni.usd.get_context().get_stage()

# Ensure a stage is loaded
if not stage:
    print("No stage is currently loaded. Please load a stage and try again.")
else:
    # Create the mock_robot Xform as the root
    mock_robot = UsdGeom.Xform.Define(stage, "/mock_robot")

    # Create the base_link Xform under mock_robot
    base_link = UsdGeom.Xform.Define(stage, "/mock_robot/base_link")

    # Create lidar_link and position it 0.4 meters above the base_link (Z-axis)
    lidar_link = UsdGeom.Xform.Define(stage, "/mock_robot/base_link/lidar_link")
    lidar_link.AddTranslateOp().Set(value=(0, 0, 0.4))  # Offset along Z-axis

    # Create camera_link and position it 0.2 meters above the base_link (Z-axis)
    camera_link = UsdGeom.Xform.Define(stage, "/mock_robot/base_link/camera_link")
    camera_link.AddTranslateOp().Set(value=(0, 0, 0.2))  # Offset along Z-axis

    # Create wheel_left and wheel_right Xforms under base_link
    wheel_left = UsdGeom.Xform.Define(stage, "/mock_robot/base_link/wheel_left")
    wheel_right = UsdGeom.Xform.Define(stage, "/mock_robot/base_link/wheel_right")

    # Position wheel_left 0.2 meters to the left of the center (X-axis)
    wheel_left.AddTranslateOp().Set(value=(-0.2, 0, 0))

    # Position wheel_right 0.2 meters to the right of the center (X-axis)
    wheel_right.AddTranslateOp().Set(value=(0.2, 0, 0))