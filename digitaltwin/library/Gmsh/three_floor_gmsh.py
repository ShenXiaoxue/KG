# -*- coding: utf-8 -*-
"""

@author: Xiaoxue Shen, the Alan Turing Institute

This is to generate the .msh file from the .stl file

"""
import gmsh
import os
import math
import sys
import time
from datetime import datetime
import numpy as np
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

def Extract_Gmsh_input(parameter):
    try:
        query = query_(parameter)
        with GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "12345678")) as driver:
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


# # Path to your STL file
path = "./digitaltwin/Data/Blender/assembly/"

path_mesh = "./digitaltwin/Data/Gmsh/Floor_msh/"

def Gmsh_input(parameters_):
    matrix_ = np.zeros(len(parameters_))
    for i in range(0, len(matrix_)):
        matrix_[i]= Extract_Gmsh_input(parameters_[i])
    return matrix_

def Gmsh_output(parameters_):
    [angle_surface_dection, mesh_size, Geometry_tolerance_boolean, curve_angle] = parameters_
    # delete the msh file if it exits
    file_msh = path_mesh +'Three_Floor_structure.msh'
    if os.path.exists(file_msh):
        os.remove(file_msh)

    gmsh.initialize()
    gmsh.clear()

    # Create ONELAB parameters with remeshing options:
    gmsh.onelab.set("""[
      {
        "type":"number",
        "name":"Parameters/Angle for surface detection",
        "values":[40],
        "min":20,
        "max":120,
        "step":1
      },
      {
        "type":"number",
        "name":"Parameters/Create surfaces guaranteed to be parametrizable",
        "values":[0],
        "choices":[0, 1]
      },
      {
        "type":"number",
        "name":"Parameters/Apply funny mesh size field?",
        "values":[0],
        "choices":[0, 1]
      }
    ]""")




    gmsh.model.add("Three_Floor_structure")

    # Set the coherence length scale (geometrical tolerance for merging)
    gmsh.option.setNumber("Geometry.ToleranceBoolean", Geometry_tolerance_boolean) #1e-4)
    gmsh.option.setNumber("Mesh.Algorithm", 8)  # Frontal-Delaunay for 3D meshes
    # gmsh.option.setNumber("Mesh.AngleToleranceFacetOverlap", 0.1)
    # gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 1)
    # gmsh.option.setNumber("Mesh.MinimumElementsPerTwoPi ", 10)

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            gmsh.merge(path + filename)



    # Angle between two triangles above which an edge is considered as sharp,
    # retrieved from the ONELAB database (see below):
    angle = gmsh.onelab.getNumber('Parameters/Angle for surface detection')[0]

    # For complex geometries, patches can be too complex, too elongated or too
    # large to be parametrized; setting the following option will force the
    # creation of patches that are amenable to reparametrization:
    forceParametrizablePatches = gmsh.onelab.getNumber(
        'Parameters/Create surfaces guaranteed to be parametrizable')[0]

    # For open surfaces include the boundary edges in the classification
    # process:
    includeBoundary = True # True

    # Force curves to be split on given angle:
    curveAngle = curve_angle  #180 # 180

    gmsh.model.mesh.classifySurfaces(angle * math.pi / 180., includeBoundary,
                                     forceParametrizablePatches,
                                     curveAngle * math.pi / 180.)

    # Create a geometry for all the discrete curves and surfaces in the mesh, by
    # computing a parametrization for each one
    gmsh.model.mesh.createGeometry()

    ###############################################################################
    # Create a volume from all the surfaces
    s = gmsh.model.getEntities(2)
    l = gmsh.model.geo.addSurfaceLoop([e[1] for e in s])
    gmsh.model.geo.addVolume([l])

    gmsh.model.geo.synchronize()

    # We specify element sizes imposed by a size field, just because we can :-)
    f = gmsh.model.mesh.field.add("MathEval")
    if gmsh.onelab.getNumber('Parameters/Apply funny mesh size field?')[0]:
        print("Yes")
        #time.sleep(10)
        gmsh.model.mesh.field.setString(f, "F", "2*Sin((x+y)/5) + 3")
        # gmsh.model.mesh.field.setString(f, "F", "10")
    else:
        print("No")
        # time.sleep(10)
        gmsh.model.mesh.field.setString(f, "F", str(mesh_size)) #  "0.02")   # 0.005


    gmsh.model.mesh.field.setAsBackgroundMesh(f)

    gmsh.model.mesh.generate(3)


    gmsh.write(path_mesh +'Three_Floor_structure.msh')


"""
# Launch the GUI and handle the "check" event to recreate the geometry and mesh
# with new parameters if necessary:
def checkForEvent():
    action = gmsh.onelab.getString("ONELAB/Action")
    if len(action) and action[0] == "check":
        gmsh.onelab.setString("ONELAB/Action", [""])
        # createGeometryAndMesh()
        # gmsh.graphics.draw()
    return True

if "-nopopup" not in sys.argv:
    gmsh.fltk.initialize()
    while gmsh.fltk.isAvailable():# and checkForEvent():
        gmsh.fltk.wait()

gmsh.finalize()
"""
