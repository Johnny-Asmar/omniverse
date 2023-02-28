from omni.kit.window.filepicker import FilePickerDialog
from omni.kit.widget.filebrowser import FileBrowserItem
from typing import List
import omni.ui as ui
import os
import omni
from pxr import Sdf, Usd, UsdGeom, Gf
import json
from scipy.spatial.transform import Rotation as R
import numpy as np
class Open_JSON():
   


    def build_ui(self):

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


        def options_pane_build_fn(selected_items):
            with ui.CollapsableFrame("Reference Options"):
                with ui.HStack(height=0, spacing=2):
                    ui.Label("Prim Path", width=0)
            return True

                # For JSON Files

        def open_file_dialog_json():
            item_filters = [".json"]
            item_filter_options_description = ["JSON Files (*.json)"]

            dialog = FilePickerDialog(
                "Demo Filepicker",
                apply_button_label="Open",
                click_apply_handler=lambda filename, dirname: on_click_open_json(dialog, filename, dirname, path_field_json),
                item_filter_options=item_filter_options_description,
                item_filter_fn=lambda item: on_filter_item(dialog, item, item_filters),
                options_pane_build_fn=options_pane_build_fn,
            )

            dialog.show()


        def on_click_open_json(dialog: FilePickerDialog, filename: str, dirname: str, path_field_json: ui.StringField):
            dialog.hide()
            dirname = dirname.strip()
            if dirname and not dirname.endswith("/"):
                dirname += "/"
            fullpath = f"{dirname}{filename}"
            path_field_json.model.set_value(fullpath)

       
        def add_ref_to_scene(ref_scene_path, ref_path_in_scene, trans_x, trans_y, trans_z, rot_x, rot_y, rot_z):
            stage = omni.usd.get_context().get_stage()
            ref_prim = stage.OverridePrim(ref_path_in_scene)
            ref_prim.GetReferences().AddReference(ref_scene_path)
             # Save the asset path to reference it later when adding to json
            attr_name = "asset_path"
            omni.kit.commands.execute("CreateUsdAttributeCommand",
                prim=ref_prim,
                attr_name=attr_name,
                attr_type=Sdf.ValueTypeNames.String,

            )
            prim_path = Sdf.Path(ref_path_in_scene)
            prev_value = ref_prim.GetAttribute(attr_name)
            omni.kit.commands.execute("ChangeProperty",
            prop_path=Sdf.Path(prim_path.AppendProperty(attr_name)),
            value=ref_scene_path,
            prev=prev_value.Get()
            )
            # Applying translation

            UsdGeom.XformCommonAPI(ref_prim).CreateXformOps()
            UsdGeom.XformCommonAPI(ref_prim).SetTranslate((trans_x, trans_y, trans_z))
            UsdGeom.XformCommonAPI(ref_prim).SetRotate((rot_x, rot_y, rot_z))
            UsdGeom.XformCommonAPI(ref_prim).SetScale((1, 1, 1))

        def create_file():
             stage = omni.usd.get_context().get_stage()
             prim_path = Sdf.Path("/World/Scope")
             prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
             if not prim.IsValid():
                omni.kit.commands.execute('CreatePrimWithDefaultXform',
                prim_type='Scope',
                prim_path=None,
                attributes={},
                select_new_prim=True)

        def for_center(prim_path):
            bbox = omni.usd.get_context().compute_path_world_bounding_box(prim_path)
            return np.array([bbox[0][0], bbox[0][1], bbox[0][2]]), np.array([bbox[1][0], bbox[1][1], bbox[1][2]])


        # def Lock_all_prims():
        #     # # Lock prim
        #     stage = omni.usd.get_context().get_stage()
        #     # Iterate over /World/Scope
        #     prim_path = Sdf.Path("/World/Scope")
        #     prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
        #     if prim.IsValid():
        #         for p in prim.GetAllChildren():
        #             if p.IsValid():
        #                 omni.kit.commands.execute('LockSpecs',
        #                 spec_paths=[Sdf.Path(p.GetPrimPath())],
        #                 hierarchy=False)



        def read_json():
            json_path = path_field_json.model.get_value_as_string()
            if json_path == "":
                validation_load.text = "Browse the json file first!"
            elif not os.path.isfile(json_path):
                validation_load.text = "There is no file in this name"
            else:
                validation_load.text = ""
                f = open(json_path)
                data = json.load(f)
                data_length = len(data)
                create_file()
                stage = omni.usd.get_context().get_stage()
                
                for i in range(data_length):
                    # get the center 
                    ref_name = f"/World/Scope/{data[i]['name']}"
                    add_ref_to_scene(data[i]['asset_path'], ref_name, data[i]['centroid']['x'], data[i]['centroid']['y'], data[i]['centroid']['z'], data[i]['rotations']['x'], data[i]['rotations']['y'], data[i]['rotations']['z'])
                    # unlock if it was locked
                    omni.kit.commands.execute('UnlockSpecs',
                        spec_paths=[Sdf.Path(ref_name)],
                        hierarchy=False)
                    c_min, c_max = for_center(ref_name)
                    center = (c_min + c_max)/2
                    set_at_x = center[0] - data[i]['centroid']['x']
                    set_at_y = center[1] - data[i]['centroid']['y']
                    set_at_z = center[2] - data[i]['centroid']['z']
                    a = set_at_x.item()
                    b = set_at_y.item()
                    c = set_at_z.item()
                    stage = omni.usd.get_context().get_stage()
                    ref_prim = stage.OverridePrim(ref_name)
                    UsdGeom.XformCommonAPI(ref_prim).CreateXformOps()
                    UsdGeom.XformCommonAPI(ref_prim).SetTranslate((data[i]['centroid']['x'] - a,data[i]['centroid']['y'] - b, data[i]['centroid']['z'] - c))
                # Closing file
                f.close()


        
        with ui.VStack():
            with ui.HStack():  
                path_field_json = ui.StringField()
                ui.Button("Browse", clicked_fn=open_file_dialog_json)
                ui.Button("Load", clicked_fn=read_json)
                # ui.Button("Lock_all_prims", clicked_fn=Lock_all_prims)
            with ui.Frame():
                validation_load = ui.Label("")
            # ui.Button("Open JSON", height=ui.Pixel(10), clicked_fn=open_json)

