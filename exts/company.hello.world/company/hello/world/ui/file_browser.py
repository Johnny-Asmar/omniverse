import omni.ui as ui
from omni.kit.window.filepicker import FilePickerDialog
from omni.kit.widget.filebrowser import FileBrowserItem
import open3d as o3d
from typing import List
import os


class AIPEFileBrowserMenu:
    def __init__(self, set_pc):
        self.path_field = None
        self.point_count = None
        self.pc = None
        self.set_pc = set_pc

    

    def build_ui(self):

        def options_pane_build_fn(selected_items):
            with ui.CollapsableFrame("Reference Options"):
                with ui.HStack(height=0, spacing=2):
                    ui.Label("Prim Path", width=0)
            return True

        def on_click_open(dialog: FilePickerDialog, filename: str, dirname: str, path_field: ui.StringField):
            dialog.hide()
            dirname = dirname.strip()
            if dirname and not dirname.endswith("/"):
                dirname += "/"
            fullpath = f"{dirname}{filename}"
            path_field.model.set_value(fullpath)

        def on_filter_item(dialog: FilePickerDialog, item: FileBrowserItem, exts: List) -> bool:
            if not item or item.is_folder:
                return True
            if dialog.current_filter_option == 0:
                # Show only files with listed extensions
                _, ext = os.path.splitext(item.path)
                if ext in exts:
                    return True
                else:
                    return False
            else:
                # Show All Files (*)
                return True


        def open_file_dialog():
            item_filters = [".ply"]
            item_filter_options_description = ["PLY Files (*.ply)"]

            dialog = FilePickerDialog(
                "Demo Filepicker",
                apply_button_label="Open",
                click_apply_handler=lambda filename, dirname: on_click_open(dialog, filename, dirname, self.path_field),
                item_filter_options=item_filter_options_description,
                item_filter_fn=lambda item: on_filter_item(dialog, item, item_filters),
                options_pane_build_fn=options_pane_build_fn,
            )

            dialog.show("/home/anthony/PycharmProjects/AIPipeline/files/datasets/real")



        def load_pointcloud():
            ply_pc = o3d.io.read_point_cloud(self.path_field.model.get_value_as_string())
            self.pc = ply_pc
            self.point_count.text = f"{len(ply_pc.points): ,} loaded from the pointcloud!"
            self.set_pc(ply_pc)

            

        

        with ui.VStack():
            with ui.HStack(height=0):
                self.path_field = ui.StringField()
                ui.Button("Browse", clicked_fn=open_file_dialog)
                ui.Button("Load", clicked_fn=load_pointcloud)
            with ui.Frame(height=12):
                self.point_count = ui.Label("")