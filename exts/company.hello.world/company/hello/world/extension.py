import omni.ext
import omni.ui as ui
import typing
import carb
import omni.usd
import json
from pxr import Sdf, Usd, UsdGeom, Gf
from typing import List
import os
from omni.kit.window.filepicker import FilePickerDialog
from omni.kit.widget.filebrowser import FileBrowserItem
import open3d as o3d
import omni.kit.commands
from pxr import UsdGeom
import omni
from omni.physx.scripts import utils




WIDTH = 0.02
PC_PATH = "/World/pc"
created_prims = 0
add_prims_tojson = [] # list of prim paths to save in bb
asset_paths = [] # list to check occurence asset path of same asset








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



class AIPEFPoseEstimationMenu:
    def __init__(self, get_pc, set_pc, get_bb_list):
        self.path_field = None
        self.asset_label = None
        self.elements = None
        self.reference_models = None
        self.get_pc = get_pc
        self.set_pc = set_pc
        self.get_bb_list = get_bb_list










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



def create_flow_pointcloud(pc_path):

    omni.kit.commands.execute("FlowCreateUsdPreset", path=pc_path, layer=0, preset_name="PointCloud",
                                url="/home/johnny/.local/share/ov/pkg/deps/1eb06a429c5271adc9ef8e5307b0f59f/extscache/omni.flowusd-104.1.9+104.1.lx64.r.cp37/data/presets/PointCloud/PointCloud.usda",
                                is_copy=True, create_ref=False, emitter_only=False)

    omni.kit.commands.execute("ChangeSetting", path="rtx/flow/enabled", value=True)

    omni.kit.commands.execute("ChangeSetting", path="rtx/flow/rayTracedReflectionsEnabled", value=True)

    omni.kit.commands.execute("ChangeSetting", path="rtx/flow/pathTracingEnabled", value=True)




# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[company.hello.world] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.

class AIPEFileBrowserMenu:
    def __init__(self, set_pc):
        self.path_field = None
        self.point_count = None
        self.pc = None
        self.ground_pc = None
        self.set_pc = set_pc



class prim:
  def __init__(self, name, center_x, center_y, center_z, rot_x, rot_y, rot_z, width, height, depth):

    self.name = name

    self.center_x = center_x
    self.center_y = center_y
    self.center_z = center_z

    self.rot_x = rot_x
    self.rot_y = rot_y
    self.rot_z = rot_z

    self.width = width
    self.height = height
    self.depth = depth







class CompanyHelloWorldExtension(omni.ext.IExt):


    

    def __init__(self):
        super().__init__()
        self.file_browser_menu = None
        self.pc = None        
        self.pose_estimation_menu = None
        self.elements = None
        self.bb_list = None

    
    
    def set_pc(self, pc):
        self.pc = pc
        create_pointcloud(pc, PC_PATH, WIDTH)

    def get_pc(self):
        return self.pc

    def set_bb_list(self, bb_list):
        self.bb_list = bb_list

    def get_bb_list(self):
        return self.bb_list

    

    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    

    def on_startup(self, ext_id):
        print("[company.hello.world] company hello world startup")

        





        
        

        self.file_browser_menu = AIPEFileBrowserMenu(self.set_pc)
        self.pose_estimation_menu = AIPEFPoseEstimationMenu(self.get_pc, self.set_pc, self.get_bb_list)

        #  self._window = ui.Window("AIPE", width=600, height=800)
        #  with self._window.frame:
        #      with ui.VStack(spacing=6, height=0):
        #          with ui.CollapsableFrame("Load PC"):
        #              with ui.Frame():
        #                  self.file_browser_menu.build_ui()

        
    

        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                


                

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


                    
                # get bounding box of a prim using prim_path
                # to get width, height and depth
                def compute_path_bbox(prim_path):

                    a = omni.usd.get_context().compute_path_world_bounding_box(prim_path)
                    width = a[1][0] - a [0][0]
                    height = a[1][1] - a[0][1]
                    depth = a[1][2] - a[0][2]
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


                def on_click_open(dialog: FilePickerDialog, filename: str, dirname: str, path_field: ui.StringField):
                    dialog.hide()
                    dirname = dirname.strip()
                    if dirname and not dirname.endswith("/"):
                        dirname += "/"
                    fullpath = f"{dirname}{filename}"
                    path_field.model.set_value(fullpath)



                def options_pane_build_fn(selected_items):
                    with ui.CollapsableFrame("Reference Options"):
                        with ui.HStack(height=0, spacing=2):
                            ui.Label("Prim Path", width=0)
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

                    dialog.show("/home/anthony/PycharmProjects/AIPipeline/files/datasets/real")


                def on_click_open_json(dialog: FilePickerDialog, filename: str, dirname: str, path_field_json: ui.StringField):
                    dialog.hide()
                    dirname = dirname.strip()
                    if dirname and not dirname.endswith("/"):
                        dirname += "/"
                    fullpath = f"{dirname}{filename}"
                    path_field_json.model.set_value(fullpath)



                # Write bounding box into a json file
                def save_bb():
                    # creating list to save json objects
                    list_of_prims = []
                    # Iterate list of prim paths ---- add_prims_tojson

                    for p in add_prims_tojson:

                    
                        name = get_name(p)
                        translate, rotation = get_transfRot(p)
                        width, height, depth = compute_path_bbox(p)

                        center_x = translate[0]
                        center_y = translate[1]
                        center_z = translate[2]

                        rot_x = rotation[0]
                        rot_y = rotation[1]
                        rot_z = rotation[2]

                        data = prim(name, center_x, center_y, center_z, rot_x, rot_y, rot_z, width, height, depth)
                        #     appending instances to list
                        list_of_prims.append(data.__dict__)

                    
                    with open(path_field_json.model.get_value_as_string(), 'w') as json_file:
                          json.dump(list_of_prims, json_file, 
                          indent=4,  
                          separators=(',',': '))




                    #######################



                def load_pointcloud():
                    ply_pc = o3d.io.read_point_cloud(self.path_field.model.get_value_as_string())
                    self.pc = ply_pc
                    self.point_count.text = f"{len(ply_pc.points): ,} loaded from the pointcloud!"
                    self.set_pc(ply_pc)

                

                def create_prim(button):
                    global created_prims
                    if created_prims==0:
                        create_file()
                        prim_name = button.text
                        print(prim_name)
                        # Check if prim already exist
                        stage = omni.usd.get_context().get_stage()
                        # Access group
                        prim_path = Sdf.Path("/World/Added_Prims")
                        prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
                        # set asset_path of the prim to be created
                        asset_path = f"/home/johnny/Downloads/usdfiles/{prim_name}.usd"
                        # count occurence of object if exists
                        count = 0
                        for x in asset_paths:
                            if asset_path == x:
                                count = count + 1

                        ref_name = f"/World/Added_Prims/{prim_name}_{count}"
                        add_ref_to_scene(asset_path, ref_name)
                        
                        created_prims = ref_name
                        # Add path to the list of assets
                        asset_paths.append(asset_path)
                    else:
                        print("One mesh was created!")


                def undo_prim():
                    global created_prims
                    if created_prims!=0:
                        stage = omni.usd.get_context().get_stage()
                        prim = stage.DefinePrim(created_prims)
                        if stage.RemovePrim(created_prims):
                            print('prim removed')
                            created_prims = 0
                            del asset_paths[-1]


                
                def place_prim():
                    global created_prims
                    global add_prims_tojson
                    if created_prims!=0:
                        add_prims_tojson.append(created_prims)
                        created_prims =  0
                        print(add_prims_tojson)
                        print(len(add_prims_tojson))
                        
                

                def reset_list():
                    # Delete prims from scene
                    stage = omni.usd.get_context().get_stage()
                    for x in add_prims_tojson:
                        stage.RemovePrim(x)
                    # Empty List
                    add_prims_tojson.clear()
                    print(add_prims_tojson)
                    
                    








                def create_file():
                    omni.kit.commands.execute('CreatePrimWithDefaultXform',
                    prim_type='Added_Prims',
                    prim_path=None,
                    attributes={},
                    select_new_prim=True)
                    return "done"


                def print_all_children_names():
                    stage = omni.usd.get_context().get_stage()

                    prim_path = Sdf.Path("/World/Added_Prims")
                    prim: Usd.Prim = stage.GetPrimAtPath(prim_path)
                    for child_prim in prim.GetAllChildren():
                        print(child_prim.GetReferences().GetPrim())




                with ui.CollapsableFrame("Load PC", height=0):
                    with ui.HStack(height=10):
                        self.path_field = ui.StringField()
                        ui.Button("Browse", clicked_fn=open_file_dialog)
                        ui.Button("Load", clicked_fn=load_pointcloud)


                with ui.CollapsableFrame("Place Object", height=0):
                    with ui.HStack():
                        left_frame= ui.ScrollingFrame(
                        height=250, width=200,
                        horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                        vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
                        )
                        with left_frame:
                            with ui.VStack():
                                button = ui.Button("Cube")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Cone")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Plane")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Test")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Test")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Test")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Test")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Test")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Test")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Test")
                                button.set_clicked_fn(lambda b=button: create_prim(b))

                                button = ui.Button("Test")
                                button.set_clicked_fn(lambda b=button: create_prim(b))
                        with ui.VStack(width=200):
                            ui.Button("Done", width=ui.Pixel(200), height=ui.Pixel(100), clicked_fn=place_prim)
                            ui.Label("Select just ONE object")
                            ui.Label("Place it by clicking DONE")
                            ui.Label("Roll Back using UNDO")
                        ui.Button("Undo", width=ui.Pixel(200), height=ui.Pixel(100), clicked_fn=undo_prim)
                        ui.Button("Reset", width=ui.Pixel(200), height=ui.Pixel(100), clicked_fn=reset_list)



                with ui.HStack():         
                    # ui.Button("getBounding", clicked_fn=compute_path_bbox)
                    # ui.Button("get_transfRot", clicked_fn=get_transfRot)
                    # ui.Button("write_json", clicked_fn=write_json)
                    # ui.Button("get_name", clicked_fn=get_name)
                    
                    


                    path_field_json = ui.StringField(width=ui.Pixel(200), height=ui.Pixel(10))
                    ui.Button("Browse", width=ui.Pixel(200), height=ui.Pixel(10), clicked_fn=open_file_dialog_json)
                    ui.Button("Save BB", width=ui.Pixel(200), height=ui.Pixel(10), clicked_fn=save_bb)

                    ui.Button("create_file", clicked_fn=create_file)
                    ui.Button("print_all_children_names", clicked_fn=print_all_children_names)
                    ui.Button("get_transfRot", clicked_fn=get_transfRot)
                    
                    


                    




                
                    



                    

    def on_shutdown(self):
        print("[company.hello.world] company hello world shutdown")






