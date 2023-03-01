import omni.ext
import omni.usd
from pxr import Sdf, Usd, UsdGeom, Gf
import omni.kit.commands
from pxr import UsdGeom
import omni
from company.hello.world.MyWindow import MyWindow


class CompanyHelloWorldExtension(omni.ext.IExt):

    def __init__(self):
        super().__init__()


    def on_startup(self, ext_id):
        self._window = MyWindow("PC Annotation", width=800, height=800)
        
    def on_shutdown(self):
        print("[company.hello.world] company hello world shutdown")
        








