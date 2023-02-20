import omni.ext
import omni.usd
from pxr import Sdf, Usd, UsdGeom, Gf
import omni.kit.commands
from pxr import UsdGeom
import omni
from company.hello.world.ui.file_browser import AIPEFileBrowserMenu
from company.hello.world.ui.pc_annotation import PC_Annotation
from company.hello.world.MyWindow import MyWindow

WIDTH = 0.02
PC_PATH = "/World/pc"



# def create_pointcloud(pc, points_path, width):
#         points = [(p[0], p[1], p[2]) for p in pc.points]
#         colors = [(p[0], p[1], p[2]) for p in pc.colors]
#         stage = omni.usd.get_context().get_stage()
#         stage.DefinePrim(points_path, 'Points')
#         pc = UsdGeom.Points(stage.GetPrimAtPath(points_path))
#         pc.CreatePointsAttr(points)
#         pc.CreateWidthsAttr([width] * len(points))
#         pc_prim = stage.GetPrimAtPath(points_path)
#         pc_prim.GetAttribute("primvars:displayColor").Set(colors)
#         create_flow_pointcloud(points_path)



# def create_flow_pointcloud(pc_path):

#     omni.kit.commands.execute("FlowCreateUsdPreset", path=pc_path, layer=0, preset_name="PointCloud",
#                                 url="/home/johnny/.local/share/ov/pkg/deps/1eb06a429c5271adc9ef8e5307b0f59f/extscache/omni.flowusd-104.1.9+104.1.lx64.r.cp37/data/presets/PointCloud/PointCloud.usda",
#                                 is_copy=True, create_ref=False, emitter_only=False)

#     omni.kit.commands.execute("ChangeSetting", path="rtx/flow/enabled", value=True)

#     omni.kit.commands.execute("ChangeSetting", path="rtx/flow/rayTracedReflectionsEnabled", value=True)

#     omni.kit.commands.execute("ChangeSetting", path="rtx/flow/pathTracingEnabled", value=True)





class CompanyHelloWorldExtension(omni.ext.IExt):

    def __init__(self):
        super().__init__()
        self.file_browser_menu = None
        self.annotation_menu = None


    def on_startup(self, ext_id):
        print("startup")
        

        self._window = MyWindow("PC Annotation", width=800, height=800)
        

    def on_shutdown(self):
        print("[company.hello.world] company hello world shutdown")
        








