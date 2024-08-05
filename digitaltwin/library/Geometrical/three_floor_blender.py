# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:32:13 2024

@author: Xiaoxue Shen, the Alan Turing Institute

This Python script will generate a three-story floor structure, and 
general stl file.

The script can work in two ways: 
    1). Copy to Blender Python console.
    2). Install Blender in Docker, and use the Python libraries to connect to the Blender.

"""

import bpy
import numpy as np
import math
import datetime
import bmesh
import os
import glob
from mathutils import geometry

# ------------------------------------------------------------------------------------------------
# Import the parameters that initialised in the knowledge graph

from neo4j import GraphDatabase

def query_(parameter_name):
    #print("query_ function:", parameter_name)
    query = (
            f"MATCH (a:parameter {{parameter_name: '{parameter_name}'}}) -[:has_value]->(parametervalue) "
            f"RETURN parametervalue.parameter_value"
        )
    return query#, {"parameter_value": parameter_name['value']}

#MATCH (a:parameter {parameter_name: "m1"})-[:has_value]->(parametervalue)
#RETURN parametervalue.parameter_value

def Extract_Geometric_input(parameter):
    try:
        query = query_(parameter)
        with GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678")) as driver:
            records, _, _ = driver.execute_query(query)
            print(records)
            for record in records:
                print(record["parametervalue.parameter_value"])
    #driver.close()
    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        driver.close()
    
    return record["parametervalue.parameter_value"]

# ------------------------------------------------------------------------------------------------

path_ = './digitaltwin/Data/Blender/components/'
path_whole = './digitaltwin/Data/Blender/assembly/'  


# Function to create a pentagonal prism
def create_pentagonal_prism(loc_, radius, height, rotate_sign):
    mesh = bpy.data.meshes.new(name='Pentagonal_Prism')
    bm = bmesh.new()
    # Create bottom pentagon
    for i in range(5):
        angle = math.radians(72 * i)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        bm.verts.new((x, y, 0))
    # Ensure the bmesh is valid and create the bottom face
    bm.verts.ensure_lookup_table()
    bm.faces.new(bm.verts[:5])
    # Extrude the bottom face to create the prism
    geom = bm.faces[:] + bm.verts[:] + bm.edges[:]
    bmesh.ops.extrude_face_region(bm, geom=geom)
    # Move the extruded vertices up to form the prism shape
    for v in bm.verts[-5:]: # Only the last 5 vertices are moved
        v.co.z += height
    # Update the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()
    # Add the mesh as an object into the scene
    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    # rotate 90 degrees
    obj.rotation_euler[1] = math.pi / 2 * rotate_sign
    # Optional: reposition the object to the scene's origin
    bpy.context.object.location = loc_

# # Call the function with desired radius and height
# create_pentagonal_prism(radius=1, height=2)

    
#  Define the parameters
L_f, B_f, H_f = 0.3005, 0.25, 0.0255               #  floor
L_p, B_p, H_p = 0.0065, 0.0255, 0.555              #  pillar
L_b, B_b, H_b = 0.0125, 0.0255, 0.0255             #  block
L_s_V, B_s_V, H_s_V = 0.0065, 0.0255, 0.05-0.0065  #  plate vertical
L_s_H, B_s_H, H_s_H = 0.05, 0.0255, 0.0065  #  plate horizontal
# The location where you want to add the cube (x, y, z coordinates)   
# Create a new cube

def create_cubes(i, loc, L, B, H, str_):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_cube_add(size=2, location=loc)
    # Optionally, the new cube can be renamed
    new_cube = bpy.context.active_object
    new_cube.name = str_ + str(i+1)
    # Scale
    new_cube.scale = (L/2, B/2, H/2)   # default size is 2m x 2m x 2m
    bpy.ops.export_mesh.stl(filepath=path_+ str_ + str(i+1)+'.stl', use_selection=True)
    # print("stl saved:", str_ + str(i+1))
    # if str_ == "Block_":
    #     count_cylinder = 0
    #     count_bolt = 0
    #     for m in [-1, 1]:
    #         for n in [-1, 1]:
    #             # print(count_cylinder)
    #             loc_hole = (loc[0], loc[1] + m*(B_b/2.0 - 0.006/(np.sqrt(2))), loc[2] + n * (B_b/2.0 - 0.006/(np.sqrt(2))))
    #             bpy.ops.mesh.primitive_cylinder_add(radius=0.0025, depth=H_b, location=loc_hole)   # radius=0.0025, depth=H_b
    #             cylinder_ = bpy.context.active_object
    #             cylinder_.rotation_euler[1] = math.pi / 2
    #             cylinder_.name = 'Cylinder_' + str(count_cylinder)
    #             # Apply Boolean modifier to the outer cylinder to create the hole
    #             boolean_modifier = new_cube.modifiers.new(name='Hole', type='BOOLEAN')
    #             boolean_modifier.object = cylinder_
    #             boolean_modifier.operation = 'DIFFERENCE'
    #             bpy.context.view_layer.objects.active = new_cube
    #             # Apply the modifier and remove the inner cylinder
    #             bpy.ops.object.modifier_apply(modifier=boolean_modifier.name)
    #             # bpy.context.scene.objects.unlink(cylinder_)
    #             # bpy.data.objects.remove(cylinder_)
    #             bpy.data.objects.remove(cylinder_, do_unlink=True)
    #             count_cylinder += 1
    #             # print(count_cylinder)
    #             ###############################################################
    #             # create bolts
    #             loc_bolt = loc_hole
    #             # NB: the depth here should be L_b caz it is in x direction
    #             bpy.ops.mesh.primitive_cylinder_add(radius=0.0025, depth=L_b, location=loc_bolt)   # radius=0.0025, depth=H_b
    #             cylinder_ = bpy.context.active_object
    #             cylinder_.rotation_euler[1] = math.pi / 2
    #             cylinder_.name = 'Cylinder_' + str(count_bolt)
    #             count_bolt += 1
    #             # ###############################################################
    #             # create Gasket
    #             # create bigger cylinder
    #             height_gasket = 0.001
    #             radius_gasket_B = 0.005
    #             sign_ = loc_hole[0] / (np.abs(loc_hole[0]))
    #             loc_gasket = (loc_hole[0] + sign_ *(L_b/2.0 +height_gasket/2.0), loc_hole[1], loc_hole[2])
    #             bpy.ops.mesh.primitive_cylinder_add(radius=radius_gasket_B, depth=height_gasket, location=loc_gasket)   # radius=0.0025, depth=H_b
    #             cylinder_B = bpy.context.active_object
    #             cylinder_B.name = "cylinder_B"
    #             cylinder_B.rotation_euler[1] = math.pi / 2
    #             # create smaller cylinder
    #             bpy.ops.mesh.primitive_cylinder_add(radius=0.0025, depth=height_gasket, location=loc_gasket)   # radius=0.0025, depth=H_b
    #             cylinder_S = bpy.context.active_object
    #             cylinder_S.name = "cylinder_S"
    #             cylinder_S.rotation_euler[1] = math.pi / 2
    #             # Apply Boolean modifier to the outer cylinder to create the hole
    #             boolean_modifier = cylinder_B.modifiers.new(name='Hole', type='BOOLEAN')
    #             boolean_modifier.object = cylinder_S
    #             boolean_modifier.operation = 'DIFFERENCE'
    #             bpy.context.view_layer.objects.active = cylinder_B
    #             # Apply the modifier and remove the inner cylinder
    #             bpy.ops.object.modifier_apply(modifier=boolean_modifier.name)
    #             # bpy.context.scene.objects.unlink(cylinder_)
    #             # bpy.data.objects.remove(cylinder_)
    #             bpy.data.objects.remove(cylinder_S, do_unlink=True)
    #             # ###############################################################
    #             # # create the 
    #             # Call the function with desired radius and height
    #             pentagonal_prism_height = 0.002
    #             loc_pentagonal_prism = (loc_hole[0] + sign_ * (L_b/2.0 +height_gasket/2.0), loc_hole[1], loc_hole[2])
    #             create_pentagonal_prism(loc_=loc_pentagonal_prism, radius=0.004, height=pentagonal_prism_height, rotate_sign=sign_)
    merge_distance=0.01
    dissolve_angle=0.01
    #
    for i in range(0, 10):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.dissolve_degenerate()
        bpy.ops.mesh.remove_doubles(threshold=merge_distance)
        bpy.ops.mesh.dissolve_limited(angle_limit=dissolve_angle)
        bpy.ops.object.mode_set(mode='OBJECT')
    return new_cube



def Boolean_Union(name_, obj1, obj2):
    bool_modifier_1 = obj1.modifiers.new(name=name_, type='BOOLEAN')
    bool_modifier_1.operation = 'UNION'
    bool_modifier_1.object = obj2
    bpy.context.view_layer.objects.active = obj1
    bpy.ops.object.modifier_apply(modifier=bool_modifier_1.name)
    bpy.data.objects.remove(obj2, do_unlink=True)
    ####
    # clean the mesh
    bpy.ops.object.mode_set(mode='OBJECT')
    selected_objects = bpy.context.selected_objects
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    # bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.dissolve_degenerate()
    #
    merge_distance=0.01
    dissolve_angle=0.01
    # Merge vertices by distance
    bpy.ops.mesh.remove_doubles(threshold=merge_distance)
    # Apply limited dissolve to reduce geometry on planar faces
    bpy.ops.mesh.dissolve_limited(angle_limit=dissolve_angle)
    #
    # split the concave face
    bpy.ops.object.mode_set(mode='OBJECT')
    selected_objects = bpy.context.selected_objects
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()   # very important
    bpy.ops.object.mode_set(mode='OBJECT')
    ####
    for i in range(0, 30):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()   # very important
        # obj = bpy.ops.mesh.select_all(action='SELECT')
        # obj.select_set(True)
        # bm = bmesh.from_edit_mesh(obj.data)
        # # Find non-planar faces and triangulate them
        # threshold_angle = 0.01
        # non_planar_faces = [f for f in bm.faces if not f.is_planar(threshold_angle)]
        # bmesh.ops.triangulate(bm, faces=non_planar_faces)
        # # Update the mesh
        # bmesh.update_edit_mesh(obj.data)
        ###
        bpy.ops.mesh.dissolve_degenerate()
        bpy.ops.mesh.remove_doubles(threshold=merge_distance)
        bpy.ops.mesh.dissolve_limited(angle_limit=dissolve_angle)
        bpy.ops.object.mode_set(mode='OBJECT')
    


def Blender_input(parameters_):
    matrix_ = np.zeros(len(parameters_))
    for i in range(0, len(matrix_)):
        matrix_[i]= Extract_Geometric_input(parameters_[i])
    return matrix_

def Blender_output(parameters_):
    [L_f, B_f, H_f,L_p, B_p, H_p, L_b, B_b,
                    H_b,L_s_V, B_s_V, H_s_V, L_s_H, B_s_H, H_s_H] = parameters_
    # Ensure we are in object mode before creating the cube
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    #bpy.ops.object.mode_set(mode='OBJECT')     # Change point 1, context missing active object

    # Delete the default cube if it exists
    if "Cube" in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete()
    

    # Use glob to find all the files in the folder
    files = glob.glob(os.path.join(path_, '*'))
    # Loop through the files and remove each one
    for file_path in files:
        # Make sure it's a file and not a directory
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")
        # create floors  
        for i in range(0, 3):
            loc = (0, 0, 0.0255/2.0 + (i+1) * (0.555 - 0.0255) / 3.0)
            if i==0:
                floor1 = create_cubes(i, loc, L_f, B_f, H_f, "Floor_")
            elif i==1:
                floor2 = create_cubes(i, loc, L_f, B_f, H_f, "Floor_")
            elif i==2:
                floor3 = create_cubes(i, loc, L_f, B_f, H_f, "Floor_")
    

    # create the pillars and all the details
    count_pillar = 0
    count_block = 0
    count_block_feet = 0
    count_cylinder = 0
    count_sheet_Lv = 0
    count_sheet_LH = 0
    for i in [-1, 1]:
        for j in [-1, 1]:    #  1
            loc = (i*(L_f + L_p)/2.0, j*(B_f - B_p)/2.0, 0.555/2.0)
            cube_ = create_cubes(count_pillar, loc, L_p, B_p, H_p, "Pillar_")
            count_pillar += 1
            ######
            ######
            # Union the pillar and first floors
            # Boolean_Union(str(i)+'_'+str(j)+'floor1', floor1, cube_)
            #   blocks
            for k in range(0, 3):
                # print(k)
                loc_b = (i*(L_f + L_p*2 + L_b)/2.0, j*(B_f - B_p)/2.0, 0.0255/2.0 + (k+1) * (0.555 - 0.0255) / 3.0)
                block_ = create_cubes(count_block, loc_b, L_b, B_b, H_b, "Block_")
                count_block += 1
                #
                # boolean the block with the pillar
                Boolean_Union(str(i)+'_'+str(j)+ '_' + str(k) +'block', cube_, block_)
                # Boolean_Union(str(i)+'_'+str(j)+ '_' + str(k) +'block', floor1, block_)
                #
                #  Create the four L-shape feet, vertical
            loc_feet_V = (i*(L_f + L_p*2 + L_s_V)/2.0, j*(B_f - B_p)/2.0, (0.05 - 0.0065)/2.0)
            # create_cubes(count_sheet_Lv, loc_feet_V, L_s_V, B_s_V, H_s_V, "sheet_V")
            # cube_V = bpy.context.active_object
            cube_V = create_cubes(count_sheet_Lv, loc_feet_V, L_s_V, B_s_V, H_s_V, "sheet_V"+str(i)+'_'+str(j))
            #  create the block on the feet
            loc_b_feet = (i*(L_f + L_p*2 + L_s_V*2 + L_b)/2.0, j*(B_f - B_p)/2.0, 0.0255/2.0)
            # create_cubes(count_block_feet, loc_b_feet, L_b, B_b, H_b, "Block_")
            block_feet = create_cubes(count_block_feet, loc_b_feet, L_b, B_b, H_b, "Block_")
            count_block_feet += 1
            # boolean union of the block feet and the L sheet
            Boolean_Union(str(i)+'_'+str(j)+'block_feet', cube_V, block_feet)
            #########
            #  Create the four L-shape feet, Horizontal
            loc_feet_H = (i*(L_f + L_p*2 + L_s_H)/2.0, j*(B_f - B_p)/2.0,  -0.0065/2.0)
            # create_cubes(count_sheet_LH, loc_feet_H, L_s_H, B_s_H, H_s_H, "sheet_H")
            # cube_H = bpy.context.active_object
            cube_H = create_cubes(count_sheet_LH, loc_feet_H, L_s_H, B_s_H, H_s_H, "sheet_H"+str(i)+'_'+str(j))
            # Join the two cubes
            # Select both cubes
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
            cube_V.select_set(True)
            cube_H.select_set(True)
            ##########
            # Make one of the cubes active
            # bpy.context.view_layer.objects.active = cube_V
            # Join the cubes into one
            # bpy.ops.object.join()
            #########
            # Instead of using "join", use "boolean union"
            Boolean_Union(str(i)+'_'+str(j)+'feet', cube_V, cube_H)
            #########
            count_sheet_Lv += 1
            count_sheet_LH += 1
            #######
            # boolean union the vertical L sheet with the pillar
            Boolean_Union(str(i)+'_'+str(j)+'pillar_feet', cube_, cube_V)
            #
            # # Union the pillar and first floors
            Boolean_Union(str(i)+'_'+str(j)+'floor1', floor1, cube_)


    Boolean_Union('floor_12', floor1, floor2)
    Boolean_Union('floor_13', floor1, floor3)      
    


    bpy.ops.object.mode_set(mode='OBJECT')
    selected_objects = bpy.context.selected_objects
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()   # very important
    bpy.ops.object.mode_set(mode='OBJECT')


    for i in range(0, 10):
        # clean the mesh
        bpy.ops.object.mode_set(mode='OBJECT')
        selected_objects = bpy.context.selected_objects
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.quads_convert_to_tris()   # very important
        bpy.ops.mesh.dissolve_degenerate()
        #
        merge_distance=0.01
        dissolve_angle=0.1
        # Merge vertices by distance
        bpy.ops.mesh.remove_doubles(threshold=merge_distance)
        # Apply limited dissolve to reduce geometry on planar faces
        bpy.ops.mesh.dissolve_limited(angle_limit=dissolve_angle)
        bpy.ops.object.mode_set(mode='OBJECT')


    # model = bpy.context.active_object
    # bpy.ops.export_mesh.stl(filepath=path_whole+'Three_story_floor.stl', 
    #                         global_scale=1.0,  
    #                         use_mesh_modifiers=True, 
    #                         batch_mode='OFF')

