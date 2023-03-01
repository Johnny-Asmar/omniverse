import omni.ext
import omni.usd
from pxr import Sdf, Usd, UsdGeom, Gf
import omni.kit.commands
from pxr import UsdGeom
import omni
from company.hello.world.ui.file_browser import AIPEFileBrowserMenu
from company.hello.world.ui.pc_annotation import PC_Annotation
from company.hello.world.MyWindow import MyWindow


class CompanyHelloWorldExtension(omni.ext.IExt):

    def __init__(self):
        super().__init__()
        self.file_browser_menu = None
        self.annotation_menu = None

    # def on_stage_event(self, event):
    #     if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
    #         ctx = omni.usd.get_context()
    #         # returns a list of prim path strings
    #         selection = ctx.get_selection().get_selected_prim_paths()
    #         if len(selection) > 0:
    #             prim_path = Sdf.Path(selection[0])
    #             stage = omni.usd.get_context().get_stage()
    #             prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
    #             while (prim.GetParent().GetPrimPath() != "/World/Scope"):
    #                 prim = prim.GetParent()

    #             old_prim = selection[0]
    #             new_selected_prim = str(prim.GetPrimPath())

    #             omni.kit.commands.execute('SelectPrimsCommand',
    #             old_selected_paths=old_prim,
    #             new_selected_paths=[new_selected_prim],
    #             expand_in_stage=True)

    

    def on_startup(self, ext_id):
        self._window = MyWindow("PC Annotation", width=800, height=800)
        # usd_context = omni.usd.get_context()
        # events = usd_context.get_stage_event_stream()
        # self.stage_event_sub = events.create_subscription_to_pop(self.on_stage_event, name="selection update")

        
    def on_shutdown(self):
        print("[company.hello.world] company hello world shutdown")
        








