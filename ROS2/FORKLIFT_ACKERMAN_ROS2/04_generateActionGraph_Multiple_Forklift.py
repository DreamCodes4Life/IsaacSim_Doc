import omni
import omni.graph.core as og
from pxr import Sdf, Usd


# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

WORLD_PATH = "/World"
GRAPH_NAME_PREFIX = "AckermannGraph"

FORKLIFT_PAYLOAD_HINT = "ForkliftC"

STEERING_JOINTS = [
    "left_rotator_joint",
    "right_rotator_joint",
]

WHEEL_JOINTS = [
    "left_front_wheel_joint",
    "right_front_wheel_joint",
    "left_back_wheel_joint",
    "right_back_wheel_joint",
]

WHEEL_BASE = 1.65
TRACK_WIDTH = 0.82
FRONT_WHEEL_RADIUS = 0.32
BACK_WHEEL_RADIUS = 0.255

MAX_WHEEL_VELOCITY = 20.0
MAX_WHEEL_ROTATION = 0.69813
MAX_STEERING_ANGLE_VELOCITY = 3.0

INVERT_STEERING = True


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def get_stage():
    return omni.usd.get_context().get_stage()


def prim_has_forklift_number(prim):
    attr = prim.GetAttribute("ForkliftNumber")
    return attr and attr.HasValue()


def get_forklift_number(prim):
    attr = prim.GetAttribute("ForkliftNumber")
    if attr and attr.HasValue():
        return int(attr.Get())
    return None


def is_forklift_prim(prim):
    """
    Detection method:
    1. Prefer prims with custom ForkliftNumber.
    2. Optionally also check name/path.
    """
    if not prim.IsValid():
        return False

    if prim_has_forklift_number(prim):
        return True

    name = prim.GetName().lower()
    path = str(prim.GetPath()).lower()

    if "forklift" in name or "forklift" in path:
        return True

    return False


def find_forklifts(world_path=WORLD_PATH):
    stage = get_stage()
    world = stage.GetPrimAtPath(world_path)

    if not world.IsValid():
        print(f"World prim not found: {world_path}")
        return []

    forklifts = []

    for prim in Usd.PrimRange(world):
        if prim == world:
            continue

        if is_forklift_prim(prim):
            number = get_forklift_number(prim)

            # Only use actual numbered forklifts
            if number is not None:
                forklifts.append((prim, number))

    forklifts.sort(key=lambda item: item[1])
    return forklifts


def graph_exists_for_forklift(forklift_path, forklift_number):
    stage = get_stage()

    graph_path = f"{forklift_path}/{GRAPH_NAME_PREFIX}_{forklift_number:02d}"

    if stage.GetPrimAtPath(graph_path).IsValid():
        return True, graph_path

    forklift_prim = stage.GetPrimAtPath(forklift_path)

    for child in forklift_prim.GetChildren():
        if child.GetName().startswith(GRAPH_NAME_PREFIX):
            return True, str(child.GetPath())

    return False, graph_path


# ---------------------------------------------------------
# CREATE GRAPH
# ---------------------------------------------------------

def create_forklift_ackermann_graph(
    forklift_path,
    forklift_number,
):
    topic_name = f"/forklift_{forklift_number:02d}/ackermann_cmd"
    graph_path = f"{forklift_path}/{GRAPH_NAME_PREFIX}_{forklift_number:02d}"

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

                ("ackermann_controller.inputs:wheelBase", WHEEL_BASE),
                ("ackermann_controller.inputs:trackWidth", TRACK_WIDTH),
                ("ackermann_controller.inputs:frontWheelRadius", FRONT_WHEEL_RADIUS),
                ("ackermann_controller.inputs:backWheelRadius", BACK_WHEEL_RADIUS),
                ("ackermann_controller.inputs:maxWheelVelocity", MAX_WHEEL_VELOCITY),
                ("ackermann_controller.inputs:maxWheelRotation", MAX_WHEEL_ROTATION),
                ("ackermann_controller.inputs:maxSteeringAngleVelocity", MAX_STEERING_ANGLE_VELOCITY),
                ("ackermann_controller.inputs:invertSteering", INVERT_STEERING),

                ("steering_articulation_controller.inputs:jointNames", STEERING_JOINTS),
                ("wheel_articulation_controller.inputs:jointNames", WHEEL_JOINTS),

                # Target articulation root prims
                ("steering_articulation_controller.inputs:targetPrim", [Sdf.Path(forklift_path)]),
                ("wheel_articulation_controller.inputs:targetPrim", [Sdf.Path(forklift_path)]),
            ],
        },
    )

    print(f"Created graph: {graph_path}")
    print(f"ROS 2 topic: {topic_name}")
    print(f"Target prim: {forklift_path}")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def generate_action_graphs_for_all_forklifts():
    forklifts = find_forklifts()

    if not forklifts:
        print("No numbered forklifts found.")
        return

    created = 0
    skipped = 0

    for prim, number in forklifts:
        forklift_path = str(prim.GetPath())

        exists, graph_path = graph_exists_for_forklift(forklift_path, number)

        if exists:
            print(f"Skipping forklift {number}: graph already exists at {graph_path}")
            skipped += 1
            continue

        create_forklift_ackermann_graph(
            forklift_path=forklift_path,
            forklift_number=number,
        )

        created += 1

    print("")
    print("Done.")
    print(f"Created graphs: {created}")
    print(f"Skipped forklifts: {skipped}")


generate_action_graphs_for_all_forklifts()