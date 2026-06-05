import omni
import omni.graph.core as og
from pxr import Sdf


def set_target_prim_relationship(graph_path, node_name, forklift_path):
    stage = omni.usd.get_context().get_stage()

    node_path = f"{graph_path}/{node_name}"
    node_prim = stage.GetPrimAtPath(node_path)

    if not node_prim.IsValid():
        raise RuntimeError(f"Node prim not found: {node_path}")

    rel = node_prim.GetRelationship("inputs:targetPrim")

    if not rel:
        rel = node_prim.CreateRelationship("inputs:targetPrim")

    rel.SetTargets([Sdf.Path(forklift_path)])


def create_forklift_ackermann_graph(
    forklift_path="/World/forklift_c",
    graph_path="/World/ActionGraph",
    topic_name="/ackermann_cmd",
    wheel_base=1.65,
    track_width=0.82,
    front_wheel_radius=0.32,
    back_wheel_radius=0.255,
    max_wheel_velocity=20.0,
    max_wheel_rotation=0.69813,
    max_steering_angle_velocity=3.0,
    invert_steering=True,
):
    keys = og.Controller.Keys

    og.Controller.edit(
        {
            "graph_path": graph_path,
            "evaluator_name": "execution",
            "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_SIMULATION,
        },
        {
            keys.CREATE_NODES: [
                ("on_playback_tick", "omni.graph.action.OnPlaybackTick"),
                ("ros2_context", "isaacsim.ros2.bridge.ROS2Context"),
                ("ros2_qos_profile", "isaacsim.ros2.bridge.ROS2QoSProfile"),
                ("ros2_subscribe_ackermanndrive", "isaacsim.ros2.bridge.ROS2SubscribeAckermannDrive"),
                ("ackermann_controller", "isaacsim.robot.wheeled_robots.AckermannController"),
                ("steering_articulation_controller", "isaacsim.core.nodes.IsaacArticulationController"),
                ("wheel_articulation_controller", "isaacsim.core.nodes.IsaacArticulationController"),
            ],

            keys.CONNECT: [
                ("on_playback_tick.outputs:tick", "ros2_subscribe_ackermanndrive.inputs:execIn"),
                ("on_playback_tick.outputs:tick", "ackermann_controller.inputs:execIn"),
                ("on_playback_tick.outputs:tick", "steering_articulation_controller.inputs:execIn"),
                ("on_playback_tick.outputs:tick", "wheel_articulation_controller.inputs:execIn"),

                ("on_playback_tick.outputs:deltaSeconds", "ackermann_controller.inputs:dt"),

                ("ros2_context.outputs:context", "ros2_subscribe_ackermanndrive.inputs:context"),
                ("ros2_qos_profile.outputs:qosProfile", "ros2_subscribe_ackermanndrive.inputs:qosProfile"),

                ("ros2_subscribe_ackermanndrive.outputs:acceleration", "ackermann_controller.inputs:acceleration"),
                ("ros2_subscribe_ackermanndrive.outputs:speed", "ackermann_controller.inputs:speed"),
                ("ros2_subscribe_ackermanndrive.outputs:steeringAngle", "ackermann_controller.inputs:steeringAngle"),
                ("ros2_subscribe_ackermanndrive.outputs:steeringAngleVelocity", "ackermann_controller.inputs:steeringAngleVelocity"),

                ("ackermann_controller.outputs:wheelAngles", "steering_articulation_controller.inputs:positionCommand"),
                ("ackermann_controller.outputs:wheelRotationVelocity", "wheel_articulation_controller.inputs:velocityCommand"),
            ],

            keys.SET_VALUES: [
                ("ros2_subscribe_ackermanndrive.inputs:topicName", topic_name),

                ("ackermann_controller.inputs:wheelBase", wheel_base),
                ("ackermann_controller.inputs:trackWidth", track_width),
                ("ackermann_controller.inputs:frontWheelRadius", front_wheel_radius),
                ("ackermann_controller.inputs:backWheelRadius", back_wheel_radius),
                ("ackermann_controller.inputs:maxWheelVelocity", max_wheel_velocity),
                ("ackermann_controller.inputs:maxWheelRotation", max_wheel_rotation),
                ("ackermann_controller.inputs:maxSteeringAngleVelocity", max_steering_angle_velocity),
                ("ackermann_controller.inputs:invertSteering", invert_steering),

                ("steering_articulation_controller.inputs:jointNames", [
                    "left_rotator_joint",
                    "right_rotator_joint",
                ]),

                ("wheel_articulation_controller.inputs:jointNames", [
                    "left_front_wheel_joint",
                    "right_front_wheel_joint",
                    "left_back_wheel_joint",
                    "right_back_wheel_joint",
                ]),
            ],
        },
    )

    set_target_prim_relationship(
        graph_path,
        "steering_articulation_controller",
        forklift_path,
    )

    set_target_prim_relationship(
        graph_path,
        "wheel_articulation_controller",
        forklift_path,
    )

    print(f"Created Ackermann ActionGraph for forklift: {forklift_path}")
    print(f"Graph path: {graph_path}")
    print(f"ROS 2 topic: {topic_name}")


create_forklift_ackermann_graph(
    forklift_path="/World/forklift_c",
    graph_path="/World/ActionGraph",
    topic_name="/ackermann_cmd",
)