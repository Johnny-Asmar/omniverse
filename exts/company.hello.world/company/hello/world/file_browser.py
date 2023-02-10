import omni.ui as ui
from omni.kit.window.filepicker import FilePickerDialog
from techoffice.aipipeline.utils.file_dialog_utils import on_click_open, on_filter_item
from techoffice.aipipeline.utils.decorators import time_this
import open3d as o3d
from techoffice.aipipeline.ground.ground_detection import detect_ground, create_ground_texture


def options_pane_build_fn(selected_items):
    with ui.CollapsableFrame("Reference Options"):
        with ui.HStack(height=0, spacing=2):
            ui.Label("Prim Path", width=0)
    return True


class AIPEFileBrowserMenu:
    def __init__(self, set_pc):
        self.path_field = None
        self.point_count = None
        self.pc = None
        self.ground_pc = None
        self.set_pc = set_pc
        self.voxel_size = 4
        self.distance_threshold = 1
        self.pixel_size = 0.2

    def set_voxel_size(self, value):
        self.voxel_size = value

    def set_distance_threshold(self, value):
        self.distance_threshold = value

    def set_pixel_size(self, value):
        self.pixel_size = value

    def build_ui(self):
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

        @time_this
        def load_pointcloud():
            ply_pc = o3d.io.read_point_cloud(self.path_field.model.get_value_as_string())
            self.pc = ply_pc
            self.point_count.text = f"{len(ply_pc.points): ,} loaded from the pointcloud!"
            self.set_pc(ply_pc)

        def do_ground_detection():
            if self.pc is not None:
                self.ground_pc = detect_ground(self.pc, self.set_pc, self.voxel_size, self.distance_threshold)

        def do_ground_texture():
            if self.ground_pc is not None:
                create_ground_texture(self.ground_pc, self.pixel_size)

        with ui.VStack():
            with ui.HStack(height=10):
                self.path_field = ui.StringField()
                ui.Button("Browse", clicked_fn=open_file_dialog)
                ui.Button("Load", clicked_fn=load_pointcloud)
            with ui.Frame(height=12):
                self.point_count = ui.Label("")
            with ui.VStack(height=20):
                ui.Label("down sampling voxel size")
                voxel_size_field = ui.FloatField()
                voxel_size_field.model.set_value(self.voxel_size)
                voxel_size_field.model.add_value_changed_fn(lambda m: self.set_voxel_size(m.get_value_as_float()))

                ui.Label("Distance threshold")
                distance_th_field = ui.FloatField()
                distance_th_field.model.set_value(self.distance_threshold)
                distance_th_field.model.add_value_changed_fn(lambda m:
                                                             self.set_distance_threshold(m.get_value_as_float()))

                ui.Label("Pixel size")
                pixel_size_field = ui.FloatField()
                pixel_size_field.model.set_value(self.pixel_size)
                pixel_size_field.model.add_value_changed_fn(lambda m:
                                                            self.set_pixel_size(m.get_value_as_float()))

                ui.Button("Detect ground plane", clicked_fn=do_ground_detection)
                ui.Button("Create ground texture", clicked_fn=do_ground_texture)
