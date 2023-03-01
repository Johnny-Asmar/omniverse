import omni.ui as ui
from pxr import Sdf, Usd, UsdGeom, Gf
import omni
from company.hello.world.ui.file_browser import AIPEFileBrowserMenu
from company.hello.world.ui.pc_annotation import PC_Annotation
from company.hello.world.ui.open_json import Open_JSON
from company.hello.world.pc_helper.pointcloud import create_pointcloud

WIDTH = 0.02
PC_PATH = "/World/pc"

class MyWindow(ui.Window):
    def __init__(self, title: str = None, **kwargs):
        super().__init__(title, **kwargs)
        self.frame.set_build_fn(self._build_window)
        self.file_browser_menu = None
        self.annotation_menu = None
        self.pc = None
        self.dir_path = ""
        self.open_json_menu = None

    def set_pc(self, pc):
        self.pc = pc
        create_pointcloud(pc, PC_PATH, WIDTH)

    def set_dir_path(self, new_path):
        self.dir_path = new_path

    def refresh(self):
        self.frame.rebuild()

    def on_stage_event(self, event):
        if self.select_feature.model.get_value_as_bool():
            if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
                ctx = omni.usd.get_context()
                # returns a list of prim path strings
                selection = ctx.get_selection().get_selected_prim_paths()
                if len(selection) > 0:
                    prim_path = Sdf.Path(selection[0])
                    stage = omni.usd.get_context().get_stage()
                    prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
                    list_of_children = []
                    while (prim.GetPrimPath() != "/World/Scope"):
                        if prim.GetPrimPath() == "/":
                            return # Don't do anything if out of World/Scope
                        list_of_children.append(prim.GetPrimPath())
                        prim = prim.GetParent()
                    if len(list_of_children) > 0:
                        old_prim = selection[0]
                        new_selected_prim = str(list_of_children[-1])
                        omni.kit.commands.execute('SelectPrimsCommand',
                        old_selected_paths=old_prim,
                        new_selected_paths=[new_selected_prim],
                        expand_in_stage=True)
                    

    def _build_window(self):

        self.file_browser_menu = AIPEFileBrowserMenu(self.set_pc)
        self.annotation_menu = PC_Annotation(self.dir_path, self.set_dir_path, self.refresh)
        self.open_json_menu = Open_JSON()
        usd_context = omni.usd.get_context()
        events = usd_context.get_stage_event_stream()
        self.stage_event_sub = events.create_subscription_to_pop(self.on_stage_event, name="selection update")
        
        with ui.VStack():       
            with ui.CollapsableFrame("Load PC", height=0):
                with ui.Frame():
                    self.file_browser_menu.build_ui()

            with ui.CollapsableFrame("Annotate PC", height=0):
                with ui.Frame():
                    with ui.VStack():
                        self.annotation_menu.build_ui()

            with ui.CollapsableFrame("Open JSON", height=0):
                with ui.Frame():
                    with ui.VStack():
                        self.open_json_menu.build_ui() 
            with ui.Frame(height=0, width=40):
                with ui.HStack():       
                    self.select_feature = ui.CheckBox()
                    self.select_feature.model.set_value(True)
                    ui.Label("Always select parent prim")
