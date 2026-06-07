"""
Occupancy map script for Isaac Sim Script Editor.
Reads Center / UpperBound / LowerBound prims and generates a PNG.

Usage: paste into the Script Editor and click Run.
"""

import asyncio
import omni.kit.app
import omni.timeline
import omni.usd
from pxr import Usd, UsdGeom

# ── Configure ──────────────────────────────────────────────────────────────────
# OUTPUT_DIR  = "YOUR_PATH_TO_SAVE_THE_FILES"
OUTPUT_DIR  = "/home/borja/Documents/IsaacSim_Projects/ROS2_Navigation"
OUTPUT_STEM = "occupancy_map"
CELL_SIZE   = 0.05   # metres per cell

# Image colours  [R, G, B, A]
COL_OCCUPIED  = [0,   0,   0,   255]
COL_FREE      = [255, 255, 255, 255]
COL_UNKNOWN   = [127, 127, 127, 255]
# ───────────────────────────────────────────────────────────────────────────────
#This is an example, choose the path to your prims)
CENTER_PATH = "/World/Occupancy_Map_Limits/Center"
UPPER_PATH  = "/World/Occupancy_Map_Limits/UpperBound"
LOWER_PATH  = "/World/Occupancy_Map_Limits/LowerBound"

# ── Optional: create limit Xforms if missing ───────────────────────────────────
CREATE_LIMIT_XFORMS_IF_MISSING = True

CENTER_TRANSLATION = (0.0, 0.0, 0.0)
LOWER_TRANSLATION  = (-5.0, -5.0, 0.1)
UPPER_TRANSLATION  = (5.0, 5.0, 0.62)


def ensure_xform_prim(path, translation):
    stage = omni.usd.get_context().get_stage()
    prim = stage.GetPrimAtPath(path)

    if prim.IsValid():
        print(f"[OccupancyMap] Prim already exists: {path}")
        return prim

    print(f"[OccupancyMap] Creating Xform: {path} at {translation}")

    xform = UsdGeom.Xform.Define(stage, path)
    xform.AddTranslateOp().Set(translation)

    return xform.GetPrim()


def ensure_limit_prims():
    if not CREATE_LIMIT_XFORMS_IF_MISSING:
        return

    ensure_xform_prim(CENTER_PATH, CENTER_TRANSLATION)
    ensure_xform_prim(LOWER_PATH, LOWER_TRANSLATION)
    ensure_xform_prim(UPPER_PATH, UPPER_TRANSLATION)

def get_world_translation(path):
    stage = omni.usd.get_context().get_stage()
    prim  = stage.GetPrimAtPath(path)
    if not prim.IsValid():
        raise RuntimeError(f"Prim not found: {path}")
    mat = UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    t   = mat.ExtractTranslation()
    return (t[0], t[1], t[2])


async def generate_occupancy_map():
    import traceback
    
    try:
        ensure_limit_prims()

        center = get_world_translation(CENTER_PATH)
        prim_a = get_world_translation(LOWER_PATH)
        prim_b = get_world_translation(UPPER_PATH)

        print(f"[OccupancyMap] center = {center}")
        print(f"[OccupancyMap] bound A (LowerBound prim) = {prim_a}")
        print(f"[OccupancyMap] bound B (UpperBound prim) = {prim_b}")

        # Compute actual min/max corners regardless of prim naming
        min_world = (min(prim_a[0], prim_b[0]), min(prim_a[1], prim_b[1]), min(prim_a[2], prim_b[2]))
        max_world = (max(prim_a[0], prim_b[0]), max(prim_a[1], prim_b[1]), max(prim_a[2], prim_b[2]))

        # The UI passes bounds as offsets relative to the origin
        lower_rel = (min_world[0] - center[0], min_world[1] - center[1], min_world[2] - center[2])
        upper_rel = (max_world[0] - center[0], max_world[1] - center[1], max_world[2] - center[2])

        print(f"[OccupancyMap] lower_rel = {lower_rel}")
        print(f"[OccupancyMap] upper_rel = {upper_rel}")

        from isaacsim.asset.gen.omap.bindings import _omap
        from isaacsim.asset.gen.omap.utils import compute_coordinates, generate_image, update_location

        om = _omap.acquire_omap_interface()

        # Stop → play so PhysX rebuilds collision data
        timeline = omni.timeline.get_timeline_interface()
        timeline.stop()
        await omni.kit.app.get_app().next_update_async()
        timeline.play()
        await omni.kit.app.get_app().next_update_async()

        # Set bounds and cell size AFTER play (required for PhysX to pick them up)
        update_location(om, list(center), list(lower_rel), list(upper_rel))
        om.set_cell_size(CELL_SIZE)

        # Wait several frames so PhysX has time to build broadphase for a complex scene
        for _ in range(10):
            await omni.kit.app.get_app().next_update_async()

        print("[OccupancyMap] Generating …")
        om.generate()
        await omni.kit.app.get_app().next_update_async()

        timeline.stop()

        dims = om.get_dimensions()
        print(f"[OccupancyMap] dims = {dims.x} x {dims.y}")

        if dims.x == 0 or dims.y == 0:
            print("[OccupancyMap] ERROR: map is empty — check that collision geometry is inside the bounds")
            return

        image_data = generate_image(om, COL_OCCUPIED, COL_UNKNOWN, COL_FREE)

        from PIL import Image
        im = Image.frombytes("RGBA", (dims.x, dims.y), bytes(image_data))
        im = im.rotate(180, expand=True)   # match the UI's default orientation

        # Unique output path
        import os
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        candidate = os.path.join(OUTPUT_DIR, f"{OUTPUT_STEM}.png")
        counter = 1
        while os.path.exists(candidate):
            candidate = os.path.join(OUTPUT_DIR, f"{OUTPUT_STEM}_{counter}.png")
            counter += 1

        im.save(candidate)
        print(f"[OccupancyMap] Saved → {candidate}")

        # ── YAML (ROS nav_msgs/OccupancyGrid format) ──────────────────────────
        # For 180° rotation (our default), bottom_left of the final image
        # corresponds to top_right from compute_coordinates.
        _, top_right, _, _, _ = compute_coordinates(om, CELL_SIZE)
        bottom_left_yaml = top_right   # corner that lands at pixel (0, h-1) after 180° rotate

        try:
            from isaacsim.core.utils.stage import get_stage_units
            scale_to_m = 1.0 / get_stage_units()
        except Exception:
            scale_to_m = 1.0  # assume stage is already in metres

        yaml_path = candidate.replace(".png", ".yaml")
        yaml_text = (
            f"image: {os.path.basename(candidate)}\n"
            f"resolution: {CELL_SIZE / scale_to_m}\n"
            f"origin: [{float(bottom_left_yaml[0] / scale_to_m):.6f},"
            f" {float(bottom_left_yaml[1] / scale_to_m):.6f}, 0.0000]\n"
            f"negate: 0\n"
            f"occupied_thresh: 0.65\n"
            f"free_thresh: 0.196\n"
        )
        with open(yaml_path, "w") as f:
            f.write(yaml_text)
        print(f"[OccupancyMap] YAML  → {yaml_path}")

    except Exception:
        import traceback as tb
        print("[OccupancyMap] ERROR:")
        tb.print_exc()


asyncio.ensure_future(generate_occupancy_map())
