from omni.kit.window.filepicker import FilePickerDialog
from omni.kit.widget.filebrowser import FileBrowserItem
from typing import List
import omni.ui as ui
import os
import omni
from pxr import Sdf, Usd, UsdGeom, Gf
from company.hello.world.classes.prim import Prim
import json
from builtins import max

class PC_Annotation():
    def __init__(self, dir_path, set_dir_path, refresh, **kwargs):
        super().__init__()
        self.created_prims = ""
        self.dir_path = dir_path
        self.set_dir_path = set_dir_path
        self.refresh  = refresh
        

    def build_ui(self):

        def get_name(prim_path):      
            stage = omni.usd.get_context().get_stage()
            prim_path = Sdf.Path(prim_path)
            prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
            xform = UsdGeom.Xformable(prim)
            # For property name
            name = prim.GetName()
            return name

        def get_transfRot(prim_path):
            stage = omni.usd.get_context().get_stage()
            prim_path = Sdf.Path(prim_path)
            prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
            xform = UsdGeom.Xformable(prim)
            # For property translation
            prop_name = "xformOp:translate"
            translate = prim.GetAttribute(prop_name).Get()
            # For property rotation
            prop_name = "xformOp:rotateXYZ"
            rotation = prim.GetAttribute(prop_name).Get()
            return translate, rotation


        def compute_path_bbox(prim_path):
            bbox = omni.usd.get_context().compute_path_world_bounding_box(prim_path)
            width = bbox[1][0] - bbox[0][0]
            height = bbox[1][1] - bbox[0][1]
            depth = bbox[1][2] - bbox[0][2]
            return width, height, depth


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

            # For USD Files
        def open_dir_dialog_usd():
            item_filters = [".usd"]
            item_filter_options_description = ["Directories with usds(*.usd)"]

            dialog = FilePickerDialog(
                "Demo Filepicker",
                apply_button_label="Open",
                click_apply_handler=lambda filename, dirname: on_click_open_usd(dialog, filename, dirname, self.dir_path_field),
                item_filter_options=item_filter_options_description,
                item_filter_fn=lambda item: on_filter_item(dialog, item, item_filters),
                options_pane_build_fn=options_pane_build_fn,
            )

            dialog.show()

        def on_click_open_usd(dialog: FilePickerDialog, filename: str, dirname: str, dir_path_field: ui.StringField):
            dialog.hide()
            dirname = dirname.strip()
            if dirname and not dirname.endswith("/"):
                dirname += "/"
            fullpath = f"{dirname}{filename}"
            self.dir_path_field.model.set_value(fullpath)
            self.refresh()


        # Write bounding box into a json file
        def save_bb():
            # In case Done is not pressed
            if self.created_prims != "" :
                place_prim()
            file_path  = path_field_json.model.get_value_as_string()
            if file_path == "":
                validation_saving.text = "Browse the json file first!"
            else:
                create_file()
                # creating list to save json objects
                list_of_prims = []
                # Iterate over /World/Scope
                stage = omni.usd.get_context().get_stage()
                prim_path = Sdf.Path("/World/Scope")
                prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
                for p in prim.GetAllChildren():
                    name = get_name(str(p.GetPrimPath()))
                    translate, rotation = get_transfRot(str(p.GetPrimPath()))
                    width, height, depth = compute_path_bbox(str(p.GetPrimPath()))

                    center_x = translate[0]
                    center_y = translate[1]
                    center_z = translate[2]

                    rot_x = rotation[0]
                    rot_y = rotation[1]
                    rot_z = rotation[2]

                    data = Prim(name, center_x, center_y, center_z, rot_x, rot_y, rot_z, width, height, depth)
                    #     appending instances to list
                    list_of_prims.append(data.__dict__)

                
                with open(file_path, 'w') as json_file:
                    json.dump(list_of_prims, json_file, 
                    indent=4,  
                    separators=(',',': '))

                validation_saving.text = "Data Saved!"

        # function will be called from another class
        def get_files_name():
            objects  = []
            directory_path  = self.dir_path_field.model.get_value_as_string()
            if not os.path.isfile(directory_path):
                if os.path.exists(directory_path):
                    for x in os.listdir(directory_path):
                        if x.endswith(".usd"):
                            # Prints only text file present in My Folder
                            objects.append(x.partition('.')[0])

            return objects


        def add_ref_to_scene(ref_scene_path: str, ref_path_in_scene: str):
            from pxr import UsdGeom
            from scipy.spatial.transform import Rotation as R
            stage = omni.usd.get_context().get_stage()
            ref_prim = stage.OverridePrim(ref_path_in_scene)
            ref_prim.GetReferences().AddReference(ref_scene_path)
            # Applying translation
            UsdGeom.XformCommonAPI(ref_prim).CreateXformOps()
            UsdGeom.XformCommonAPI(ref_prim).SetTranslate((0, 0, 0))
            UsdGeom.XformCommonAPI(ref_prim).SetRotate((0, 0, 0))
            UsdGeom.XformCommonAPI(ref_prim).SetScale((1, 1, 1))

        def create_prim(button):
            # global created_prims
            validation_saving.text = ""
            create_file()
            if self.created_prims == "":
                # create_file()
                prim_name = button.text
                # Check if prim already exist
                stage = omni.usd.get_context().get_stage()
                # Access group
                prim_path = Sdf.Path("/World/Scope")
                prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
                # set asset_path of the prim to be created
                asset_path = f"/home/johnny/Downloads/usdfiles/{prim_name}.usd"
                # iterate over /World/Scope
                prim_path = Sdf.Path("/World/Scope")
                prim_scope: Usd.Prim = stage.GetPrimAtPath(prim_path)
                list_on_stage = []
                for p in prim_scope.GetAllChildren():
                    list_on_stage.append(p.GetName())
                # Iterate over all the prims
                taken_idx = list(map(lambda e: int(e.split("_")[-1]), filter(lambda e: e.startswith(f"{prim_name}_"), list_on_stage)))
                idx = min(filter(lambda e: e not in taken_idx, range(max(taken_idx) + 2 if len(taken_idx) > 0 else 1)))

                ref_name = f"/World/Scope/{prim_name}_{idx}"
                add_ref_to_scene(asset_path, ref_name)

                # unlock if it was locked
                omni.kit.commands.execute('UnlockSpecs',
                    spec_paths=[Sdf.Path(ref_name)],
                    hierarchy=False)

                
                self.created_prims = ref_name

            else:
                validation.text = "One Object already created"
                validation_saving.text = ""


        def undo_prim():
            validation_saving.text = ""
            if self.created_prims != "":
                stage = omni.usd.get_context().get_stage()
                prim = stage.DefinePrim(self.created_prims)
                if stage.RemovePrim(self.created_prims):
                    self.created_prims = ""



        def place_prim():
            create_file()
            validation_saving.text = ""
            if self.created_prims != "":
                validation.text = ""
                omni.kit.commands.execute('LockSpecs',
                spec_paths=[Sdf.Path(self.created_prims)],
                hierarchy=False)

                self.created_prims =  ""

            else:
                validation.text = "Select an object!"
                



        def reset_list():
            # Delete prims from scene
            validation.text = ""
            validation_saving.text = ""
            stage = omni.usd.get_context().get_stage()
            # Iterate over /World/Scope
            
            prim_path = Sdf.Path("/World/Scope")
            prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
            if prim.IsValid():

                for p in prim.GetAllChildren():
                    if p.IsValid():
                        stage.RemovePrim(str(p.GetPrimPath()))
                self.created_prims = ""
                omni.kit.commands.execute('DeletePrims',
                    paths=['/World/Scope'],
                    destructive=False)

                    
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


        with ui.VStack():
            with ui.HStack(height=10):
                    ui.Label("Select Directory of USD Files: ")
                    # ui.StringField(self.dir_path)
                    self.dir_path_field = ui.StringField()
                    self.dir_path_field.model.set_value(self.dir_path)
                    self.dir_path_field.model.add_value_changed_fn(lambda m:
                                                            self.set_dir_path(m.get_value_as_string()))

                    
                    ui.Button("Browse", clicked_fn=open_dir_dialog_usd)
                    ui.Button("Refresh", height=ui.Pixel(10), clicked_fn=self.refresh)


            with ui.HStack():

                
                
                objects_in_dir = get_files_name()
                if len(objects_in_dir) != 0:
                    left_frame= ui.ScrollingFrame(
                    height=250, width=200,
                    horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                    vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
                    )
                    with left_frame:
                        with ui.VStack():

                            for but in objects_in_dir:
                                button = ui.Button(but, height=ui.Pixel(40))
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                else:
                    validation_dir = ui.Label("Please check Direcctory path")

                        
                with ui.VStack(width=200):
                    ui.Button("Done", width=ui.Pixel(200), height=ui.Pixel(100), clicked_fn=place_prim)
                    validation = ui.Label("")

                ui.Button("Undo", width=ui.Pixel(200), height=ui.Pixel(100), clicked_fn=undo_prim)
                ui.Button("Reset", width=ui.Pixel(200), height=ui.Pixel(100), clicked_fn=reset_list)

            with ui.VStack():         
                with ui.HStack(height=60):  
                    ui.Label("Save json file in: ")
                    path_field_json = ui.StringField()
                    ui.Button("Browse", clicked_fn=open_file_dialog_json)
                    validation_saving = ui.Label("")
                ui.Button("Save BB", height=ui.Pixel(10), clicked_fn=save_bb)

