import pkg_resources
import ast

class Vendor:
    usbid    = None
    name     = None
    products = None

    def __init__(self, *arg):
        pass

    def get_id(self):
        return self.usbid;

    def get_name(self):
        return self.name;

    
class Product:
    vendor      = None
    usbid       = None
    name        = None
    width       = None
    length      = None
    regmark     = False
    margin_left = None
    margin_top  = None

    def __init__(self, vendor, name, prophash):
        self.vendor = vendor
        self.name = name;
        if usbid in prophash:
            
        pass
    
    def get_vendorid():
        pass

    def get_vendorname():
        pass

class Devices:

    # {
    #     'VENDOR_ID_GRAPHTEC': {
    #         'usbid': 0x0b4d, 'name': 'Graphtec',
    #         'products': {
    #             'PRODUCT_ID_CC200_20': {
    #                 'usbid': 0x110a, 'name': 'Craft Robo CC200-20'
    #             },
    #             'PRODUCT_ID_CC300_20': {
    #                 'usbid': 0x111a, 'name': 'Craft Robo CC300-20'
    #             },
    #             'PRODUCT_ID_SILHOUETTE_SD_1': {
    #                 'usbid': 0x111c, 'name': 'Silhouette SD 1'
    #             },
    #             'PRODUCT_ID_SILHOUETTE_SD_2': {
    #                 'usbid': 0x111d, 'name': 'Silhouette SD 2'
    #             },
    #             'PRODUCT_ID_SILHOUETTE_CAMEO': {
    #                 'usbid': 0x1121, 'name': 'Silhouette Cameo',     'width_mm': 304, 'length_mm': 3000, 'regmark': True, 'margin_left_mm':9.0, 'margin_top_mm':1.0
    #             },
    #             'PRODUCT_ID_SILHOUETTE_CAMEO2': {
    #                 'usbid': 0x112b, 'name': 'Silhouette Cameo2',    'width_mm': 304, 'length_mm': 3000, 'regmark': True, 'margin_left_mm':9.0, 'margin_top_mm':1.0
    #             },
    #             'PRODUCT_ID_SILHOUETTE_CAMEO3': {
    #                 'usbid': 0x112f, 'name': 'Silhouette Cameo3',    'width_mm': 304, 'length_mm': 3000, 'regmark': True, 'margin_left_mm':5,   'margin_top_mm':15.5
    #             },
    #             'PRODUCT_ID_SILHOUETTE_PORTRAIT': {
    #                 'usbid': 0x1123, 'name': 'Silhouette Portrait',  'width_mm': 206, 'length_mm': 3000, 'regmark': True
    #             },
    #             'PRODUCT_ID_SILHOUETTE_PORTRAIT2': {
    #                 'usbid': 0x1132, 'name': 'Silhouette Portrait2', 'width_mm': 203, 'length_mm': 3000, 'regmark': True
    #             }
    #         }
    #     }
    # }
    def __init__(self):
        defaults = pkg_resources.resource_filename(__name__,"devices.dat")
        with open(defaults,'r') as f:
            s = f.read()
            self._elements = ast.literal_eval(s)

    def __getattr__(self,name):
        if name.startswith('VENDOR_ID'):
            pass
        elif name.startswith('PRODUCT_ID'):
            pass
        else:
            raise Exception("Get Attribute","Unrecognized attribute name: %s" % name)

    
