"""
This is the main function that creates the blueprint, imports in the modules, and defines some generic routes such as the home and error pages.
"""
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint

bp = Blueprint('templateDTOP', __name__) # Creates the name of the app

from .routes import module1

# X Shen added
from .library import buildgraph
from .library.ODE import three_dof
from .library.Geometrical import three_floor_blender
from .library.Gmsh import three_floor_gmsh
from .library.Gmsh2XDMF import Gmsh2XDMF


import numpy as np
import time
import subprocess

@bp.route('/')
@bp.route('/home')
@bp.route('/index')
def home():
    return render_template('home.html')

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


for i in range(0, 10):
    print("Testing..")
          
# Initialise the knowledge graph
kg_ = buildgraph.knowledgeGraph()

#################################################
# Run the agent "ODE" to generate reponse
#ODE_input
parameters_ODE = ["m1", "m2", "m3", "k1", "k2", "k3", "c1", "c2", "c3"]
ode_input = three_dof.ODE_input(parameters_ODE)
print('\n' * 5)
print("Received ODE parameters, run the ODE agent..")
time.sleep(5)
ode_output = three_dof.ODE_output(Mi=ode_input[0:3], Ki=ode_input[3:6], Ci=ode_input[6:9])

print('\n' * 5)
print("ODE agent task finished.")
time.sleep(5)
# ODE_output
kg_.ODE()

#################################################
# Geometric
components_ = ["floor", "pillar", "block", "V", "H"]
directions_ = ["Len_", "Wid_", "Hei_"]
parameters_Geometric = []    #  Get input
# parameters all about length, width and height. The coordinates can be calculated by these.
for i in range(0, 5):
    for j in range(0, 3):
        parameters_Geometric.append(directions_[j] + components_[i])


geometric_input = three_floor_blender.Blender_input(parameters_Geometric)

print('\n' * 5)
print("Received geometric parameters, run the Blender agent..")
time.sleep(5)

three_floor_blender.Blender_output(geometric_input)

print('\n' * 5)
print("Blender agent task finished.")

print(parameters_Geometric, geometric_input)
kg_.Geometric()
################################################
# Gmsh
three_floor_gmsh.Gmsh_output()
parameters_Gmsh = ["angle_surface_dection", "mesh_size", "Geometry_tolerance_boolean", "curve_angle"]
Gmsh_input_ = three_floor_gmsh.Gmsh_input(parameters_Gmsh)
#print(parameters_Gmsh, Gmsh_input_)

print('\n' * 5)
print("Received meshing parameters, run the Gmsh agent..")
time.sleep(5)


#three_floor_gmsh.Gmsh_output(Gmsh_input_)

print('\n' * 5)
print("Gmsh agent task finished.")
time.sleep(5)

kg_.Gmsh_()


################################################
# Python XDMF
print('\n' * 5)
print("Run the Gmsh_to_XDMF agent..")
time.sleep(5)

Gmsh2XDMF.Gmsh2XDMF()
kg_.Gmsh2XDMF()

print('\n' * 5)
print("Gmsh2XDMF agent task finished.")

################################################
# FEM
#import os
#os.system('sh ./digitaltwin/library/sleep.sh')
#subprocess.call("./digitaltwin/library/sleep.sh", shell=True)
#three_floor_FEM_ModalAnalysis.FEM_output()

#kg_.FEM_()




