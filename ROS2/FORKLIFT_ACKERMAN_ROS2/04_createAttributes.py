import omni.usd
from pxr import Sdf

stage = omni.usd.get_context().get_stage()

forklift_number = 1

for prim in stage.Traverse():

    if not prim.IsValid():
        continue

    prim_name = prim.GetName().lower()

    # Does this prim contain "forklift"?
    if "forklift" not in prim_name:
        continue

    # Check if any parent already contains "forklift"
    parent = prim.GetParent()
    skip = False

    while parent and parent.IsValid():
        if "forklift" in parent.GetName().lower():
            skip = True
            break
        parent = parent.GetParent()

    if skip:
        continue

    # Create or update ForkliftNumber attribute
    attr = prim.GetAttribute("ForkliftNumber")

    if not attr:
        attr = prim.CreateAttribute(
            "ForkliftNumber",
            Sdf.ValueTypeNames.Int,
            custom=True,
        )

    attr.Set(forklift_number)

    print(
        f"Assigned ForkliftNumber={forklift_number} "
        f"to {prim.GetPath()}"
    )

    forklift_number += 1

print(f"\nConfigured {forklift_number - 1} forklifts")