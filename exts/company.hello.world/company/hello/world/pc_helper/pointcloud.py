import omni.kit.commands
import omni.usd
from pxr import UsdGeom
import os 


def create_pointcloud(pc, points_path, width):
    points = [(p[0], p[1], p[2]) for p in pc.points]
    colors = [(p[0], p[1], p[2]) for p in pc.colors]
    stage = omni.usd.get_context().get_stage()
    stage.DefinePrim(points_path, 'Points')
    pc = UsdGeom.Points(stage.GetPrimAtPath(points_path))
    pc.CreatePointsAttr(points)
    pc.CreateWidthsAttr([width] * len(points))
    pc_prim = stage.GetPrimAtPath(points_path)
    pc_prim.GetAttribute("primvars:displayColor").Set(colors)
    create_flow_pointcloud(points_path)



def get_url():
    for dirpath, dirnames, filenames in os.walk("/home"): 
        for filename in filenames: 
            if filename.endswith("PointCloud.usda") and "1eb" in dirpath: 
                path = os.path.join(dirpath, filename)

    return path

def create_flow_pointcloud(pc_path):

    omni.kit.commands.execute("FlowCreateUsdPreset", path=pc_path, layer=0, preset_name="PointCloud",
                              url=get_url(),
                              is_copy=True, create_ref=False, emitter_only=False)

    omni.kit.commands.execute("ChangeSetting", path="rtx/flow/enabled", value=True)

    omni.kit.commands.execute("ChangeSetting", path="rtx/flow/rayTracedReflectionsEnabled", value=True)

    omni.kit.commands.execute("ChangeSetting", path="rtx/flow/pathTracingEnabled", value=True)

