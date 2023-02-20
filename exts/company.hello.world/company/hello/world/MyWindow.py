import omni.ui as ui

from company.hello.world.ui.file_browser import AIPEFileBrowserMenu
from company.hello.world.ui.pc_annotation import PC_Annotation
from company.hello.world.pc_helper.pointcloud import create_pointcloud


WIDTH = 0.02
PC_PATH = "/World/pc"

class MyWindow(ui.Window):
    def __init__(self, title: str = None, delegate=None, **kwargs):
        super().__init__(title, **kwargs)
        self.frame.set_build_fn(self._build_window)
        self.file_browser_menu = None
        self.annotation_menu = None
        self.pc = None        

    def set_pc(self, pc):
        self.pc = pc
        create_pointcloud(pc, PC_PATH, WIDTH)

    def get_pc(self):
        return self.pc


    def _on_change_info_path(self, changed_path):
        self.frame.rebuild()


    def _build_window(self):
        def refresh():
            self.frame.rebuild()


        self.file_browser_menu = AIPEFileBrowserMenu(self.set_pc)
        self.annotation_menu = PC_Annotation()

        with ui.VStack():
            with ui.CollapsableFrame("Load PC", height=0):
                with ui.Frame():
                    self.file_browser_menu.build_ui()

            with ui.CollapsableFrame("Annotate PC"):
                with ui.Frame():
                    self.annotation_menu.build_ui()
                    
            ui.Button("refresh", clicked_fn=refresh)