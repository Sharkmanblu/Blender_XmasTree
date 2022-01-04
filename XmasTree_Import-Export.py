bl_info = {
    "name": "XmasTree",
    "author": "Fatutta Gabriele",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Scene Property > Xmas Tree",
    "description": "Import XmasTree Matt Parker/Harvard Coord/RGBValue - Export Rgb Value",
    "warning": "",
    "doc_url": "",
    "category": "Utility",
}

import bpy
import csv
import os
from bpy.props import (StringProperty,PointerProperty,BoolProperty,)
from bpy.types import (Operator,Panel,PropertyGroup,)
from mathutils import Vector


def purge (): # Purge all previews Led Mesh & Material

    bpy.ops.object.select_all(action='SELECT')

    bpy.ops.object.delete()
    
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

def newMaterial(id):

    mat = bpy.data.materials.get(id)

    if mat is None:
        mat = bpy.data.materials.new(name=id)

    mat.use_nodes = True

    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()

    return mat


def newShader(id):# Create new material for each LED
    mat = newMaterial(id) # functon to create base Material data with name(id)
    nodes = mat.node_tree.nodes # Material Nodes
    links = mat.node_tree.links #Material Links
    output = nodes.new(type='ShaderNodeOutputMaterial') # New Output
    shader = nodes.new(type='ShaderNodeEmission')# New emissive material
    nodes["Emission"].inputs[0].default_value = (0, 0, 0, 1) # Set Color to Black
    nodes["Emission"].inputs[1].default_value = 5 #Set intensity value for better preview
    links.new(shader.outputs[0], output.inputs[0]) # link Emissive mat to ouput
    return mat # Return Material Data

def setColor(id, r,g,b,frame): # set Color for Frame
    mat = bpy.data.materials.get(id) # select Correct material
    nodes = mat.node_tree.nodes # material nodes
    nodes["Emission"].inputs[0].default_value = (r/255.0, g/255.0, b/255.0, 1) # set Color - Mapped to 0-1
    nodes["Emission"].inputs[0].keyframe_insert("default_value", frame=int(frame))# set keyframe 
    

def newTreeByCoords(path): # Create Led tree by csv coords
    coll = bpy.data.collections.get('Import Tree')
    if coll is None:
        newcoll = bpy.data.collections.new('Import Tree') # create new collection
        bpy.context.scene.collection.children.link(newcoll) # link collection to scene
#    newpath = path.replace("\\","/")
    path = os.path.abspath(bpy.path.abspath(path))
    x =1
    treename ="MattTree"
    if  bpy.context.scene.temp.harvardBool is True:
        x= 100
        treename= "HarvardTree"
    with open(path,encoding='utf-8-sig') as f: # open coords file
        reader = csv.reader(f) # create csv reader object
        LedCount = 0
        for row in reader: #loop Coords
            LedName = "Led_%d"%(LedCount)
         
            bpy.ops.mesh.primitive_ico_sphere_add(radius=0.05, enter_editmode=False, align='WORLD', location=(float(row[0])/x, float(row[1])/x, float(row[2])/x), scale=(1, 1, 1)) #create icosphere mesh
            obj = bpy.context.active_object #retrieve selected object (last created)
            obj.users_collection[0].objects.unlink(obj)
            bpy.data.collections['Import Tree'].objects.link(obj)
            obj.data.name = LedName #assign name to mesh
            obj.name = LedName #assign name to mesh            
            mat = newShader('M_'+LedName)#create new Material for each Led
            obj.data.materials.append(mat) #assign material to mesh
            LedCount +=1
            
    bpy.context.view_layer.objects.active = bpy.data.objects['Led_1'] # Set active object
    for obj in bpy.data.collections['Import Tree'].all_objects: # select alla object in collection
        obj.select_set(True)
        
    bpy.ops.object.join() # join objects
    bpy.context.scene.cursor.location = Vector((0.0,0.0,0.0))
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    obj = bpy.data.objects['Led_1']
    obj.data.name = treename #assign name to mesh
    obj.name = treename

def setColorByFrame(path): # Set Led's color per frame
#    newpath = path.replace("\\","/")
    path = os.path.abspath(bpy.path.abspath(path))
    with open(path,encoding='utf-8-sig') as f:

        bpy.context.scene.frame_end = sum(1 for line in f) - 2 #Set Timeline end to match number of frame in file
        f.seek(0) #Return ro first row
        reader = csv.reader(f) #Create reader

        change = True # Only for Test - do not change
        
        for row in reader: #Loop rows

            if reader.line_num==1:  #skip first row "FRAME,R_x,G_x,B_x ..."
                continue
            if change !=False:
                frame  = row[0] # Frame Number
                row.pop(0) # Discard Fist colum (frame)
                chunk = [row[i:i+3] for i in range(0,len(row),3)] #Create rgb list
                Rgbcount = 0 #Tracking led number
                for rgb in chunk: # loop RGB fo Led
                    setColor("M_Led_%s"%(Rgbcount),int(rgb[0]),int(rgb[1]),int(rgb[2]),frame) # set Color and Keyframe for each Led at given frame
                    Rgbcount+=1


def exportCoords(path): # Export CSV with led value and frame
    path = os.path.abspath(bpy.path.abspath(path))
    bpy.data.node_groups["Xmas Tree"].nodes["Instance on Points"].mute =True #Mute GeoNode Instace node - Needed to retrieve color value
    if  bpy.context.scene.temp.harvardBoolexp is True:
        ob=bpy.context.scene.objects["Harvard _Tree _Coords_Geo_Node"] #object with geo Node modifier
    else:
        ob=bpy.context.scene.objects["Matt_Parker_Tree_Coords_Geo_Node"] #object with geo Node modifier
    bpy.ops.screen.frame_jump(end=False) #return to frame 0
    first_row = [] #Create list for first row -> add "frame_Id" and rgb value header
    first_row.append("FRAME_ID") 
    for a in range(0,500): 
        first_row.extend(["R_%s"%(a),"G_%s"%(a),"B_%s"%(a)])
    with open(path,mode ="w",encoding='utf-8-sig') as f: #create and open csv file
        writer = csv.writer(f,delimiter=',',lineterminator="\n",quoting=csv.QUOTE_MINIMAL)#csv writer object
        writer.writerow(first_row)#write header/first row
        for fr in range(bpy.data.scenes["Scene"].frame_start,bpy.data.scenes["Scene"].frame_end +1): #write led values in csv for every frame
            bpy.data.scenes['Scene'].frame_set(fr)#set timeline on frame
            data = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).data#evaluate color value
            n = len(data.attributes['Color2'].data) # lenght of array
            vals = [0.,0.,0.,0.] * n # 4 values per element (RGBA)
            data.attributes['Color2'].data.foreach_get("color", vals)#retrieve all RGBA values
            del vals[4-1::4]#discard A values
            vals = [int(x * 255) for x in vals]#map values to 0-255 range (blender work in 0-1 range)
            valuearr = [fr]#add frame number as first row element
            valuearr.extend(vals)#extend array with RGB value
            writer.writerow(valuearr)#write array in CSv file

            
    bpy.data.node_groups["Xmas Tree"].nodes["Instance on Points"].mute =False#Unmute GeoNode Instace node - Needed to retrieve color value

def set_bool1(self, value):
    self["mattBool"] = value
    self["harvardBool"] = not value

def get_bool1(self):
    return self["mattBool"]

def set_bool2(self, value):
    self["harvardBool"] = value
    self["mattBool"] = not value

def get_bool2(self):
    return self["harvardBool"]

def set_boole1(self, value):
    self["mattBoolexp"] = value
    self["harvardBoolexp"] = not value

def get_boole1(self):
    return self["mattBoolexp"]

def set_boole2(self, value):
    self["harvardBoolexp"] = value
    self["mattBoolexp"] = not value

def get_boole2(self):
    return self["harvardBoolexp"]

class XtreeProperty(PropertyGroup):

    coordsPath: StringProperty( #Coords File path
        name="coordsPath",
        description="Select csv file with led coords",
        default="",
        maxlen=1024,
        subtype="FILE_PATH",

        )

    valuePath: StringProperty( #Led value File path
        name="valuePath",
        description="Select csv file with RGB value",
        default="",
        maxlen=1024,
        subtype="FILE_PATH",  
        )
    extPath: StringProperty( #Esport file path
        name="extPath",
        description="Select csv file for export data",
        default="",
        maxlen=1024,
        subtype="FILE_PATH",      
        )
    harvardBool : BoolProperty(
        name="harvard bool",
        description="harvard Bool",
        default = False,
        set=set_bool1,
        get=get_bool1,
        )
    mattBool : BoolProperty(
        name="Matt bool",
        description="matt Bool",
        default = True,
        set=set_bool2,
        get=get_bool2,
        )
    harvardBoolexp : BoolProperty(
        name="harvard bool exp",
        description="harvard Boolexport",
        default = False,
        set=set_boole2,
        get=get_boole2,
        )
    mattBoolexp : BoolProperty(
        name="Matt bool exp",
        description="matt Bool export",
        default = True,
        set=set_boole1,
        get=get_boole1,
        )

class MasterPanel(bpy.types.Panel):
    bl_label = "Xmas Tree"
    bl_idname = "XMASTREE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"    
    def draw(self, context):
        pass
        
class MasterPanel_PT_Panel1(bpy.types.Panel):
    bl_label = "Xmas Tree Import Panel"
    bl_idname = "XMASTREEIMPORT_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_parent_id = "XMASTREE_PT_layout"
    bl_options = {'DEFAULT_CLOSED'}    
    def draw(self, context):
        layout = self.layout
        st = context.space_data
        scene = context.scene
        temp  = scene.temp
        
        layout.label(text="Select COORDS CSV File:")
        row = layout.row()
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(temp, "harvardBool", text="Harvard Coords")
        row.prop(temp, "mattBool", text="Matt Parker Coords")
#        row.operator("test.test", text="Load Led CSV animation")   
        row = layout.row()
#        layout.separator()
        row.prop(temp, "coordsPath",text="")
        row = layout.row()
        row.operator("read.csvtree", text="Load Tree Coords")
        layout.label(text="Select LED CSV File:")
        row = layout.row()
        row.prop(temp, "valuePath",text="")
        row = layout.row()
        row.operator("reada.csvled", text="Load Led CSV animation")
#        row = layout.row()
#        row.operator("purge.all", text="PURGE DATA AND MESH")

        
class MasterPanel_PT_Panel2(bpy.types.Panel):
    bl_label = "Xmas Tree Export Panel"
    bl_idname = "XMASTREEEXPORT_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_parent_id = "XMASTREE_PT_layout"   
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout
        st = context.space_data
        scene = context.scene
        temp  = scene.temp
        
        layout.label(text="Export CSV File name:")
        row = layout.row()
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(temp, "harvardBoolexp", text="Harvard ")
        row.prop(temp, "mattBoolexp", text="Matt Parker ")
        row = layout.row()        
        row.prop(temp, "extPath",text="")
        row = layout.row()
        row.operator("write.csvled", text="Save CSV RGB Value")

        
class ImportCsvTree(Operator):
    bl_idname ="read.csvtree"
    bl_label = "Read CSV Tree and create point"
    
    def execute(self,context):
        path = bpy.context.scene['temp']['coordsPath']
        newTreeByCoords(path)
        return{'FINISHED'}

class ImportCsvLed(Operator):
    bl_idname ="reada.csvled"
    bl_label = "Read CSV LED and create keyframe"
    
    def execute(self,contextd):
        path = bpy.context.scene['temp']['valuePath']
        setColorByFrame(path)
        return{'FINISHED'}
    
class ExportCsv(Operator):
    bl_idname ="write.csvled"
    bl_label = "Write CSV LED"
    
    def execute(self,context):
        path = bpy.context.scene['temp']['extPath']
        exportCoords(path)
        return{'FINISHED'}
  
class TestButton(Operator):
    bl_idname ="test.test"
    bl_label = "test button"
    
    def execute(self,context):
        print("Ciao test")
        print(bpy.context.scene.temp.harvardBool)
        print(bpy.context.scene.temp.mattBool)
        return{'FINISHED'}
  
    
class PurgeData(Operator):
    bl_idname ="purge.all"
    bl_label = "purge alla data and mesh"
    
    def execute(self,context):
        purge()
        return{'FINISHED'}

classes = (
    XtreeProperty,
    MasterPanel,
    MasterPanel_PT_Panel1,
    MasterPanel_PT_Panel2,
    ImportCsvTree,
    ImportCsvLed,
#    PurgeData,
    ExportCsv,
#    TestButton,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.temp = PointerProperty(type=XtreeProperty)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.temp

if __name__ == "__main__":
    register()