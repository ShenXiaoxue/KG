# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:46:22 2024

@author: Xiaoxue Shen, Alan Turing Institute
"""

import meshio
path_Gmsh = "./digitaltwin/Data/Gmsh/Floor_msh/"
#path_XDMF = "./digitaltwin/Data/XDMF/"
path_XDMF = "./digitaltwin/library/fenicsx/shared/"
mesh_name = "Three_Floor_structure"

# msh = meshio.read(path_mesh + mesh_name + ".msh")

def msh_to_xdmf(filename: str, prune: bool = True):
    """Convert a .msh file to .xdmf.
    
    Parameters
    ==========
    filename:
        The file name to read/write (not including extension). The extension ".msh" is
        appended to create the 'read from' file name, and the extension ".xdmf" is
        appended to create the 'write to' file name. If any mesh facets are marked as
        "Physical" regions, the suffix "_facets.xdmf" is appended to create the file
        name for exporting this information.
    prune:
        Force the geometric dimension to match the topological dimension of the mesh by
        removing geometry coordinates of higher dimension than the mesh topology (i.e.
        for 1D meshes, only the x-coordinate is retained, for 2D meshes only the
        x- and y-coordinates are retained, etc.)
    """
    # Importing mesh from gmsh and defining surface and boundary markers
    msh = meshio.read(path_Gmsh + filename + ".msh")
    
    # Determine mesh topological dimension
    if "tetra" in msh.cells_dict:
        tdim = 3
        cell_lbl = "tetra"
        facet_lbl = "triangle"
    elif "triangle" in msh.cells_dict:
        tdim = 2
        cell_lbl = "triangle"
        facet_lbl = "line"
    else:
        tdim = 1
        cell_lbl = "line"
        facet_lbl = "point"
    
    # Extract node coordinates
    if prune:
        points = msh.points[:, :tdim]
        print("this one")
    else:
        points = msh.points
    
    # Extract cells and facets
    cells = msh.cells_dict[cell_lbl]
    if facet_lbl in msh.cells_dict:
        facets = msh.cells_dict[facet_lbl]
    else:
        facets = None
    
    # Extract cell and facet markers
    if cell_lbl in msh.cell_data_dict["gmsh:geometrical"]:   # physical
        cell_data = msh.cell_data_dict["gmsh:geometrical"][cell_lbl]
    else:
        cell_data = None
        
    
    if facet_lbl in msh.cell_data_dict["gmsh:geometrical"]:
        facet_data = msh.cell_data_dict["gmsh:geometrical"][facet_lbl]
    else:
        facet_data = None
    
    cell_mesh = meshio.Mesh(
        points=points,
        cells={cell_lbl: cells},
        point_data=None,
        cell_data={"cell_marker": [cell_data]} if cell_data is not None else None,
        field_data=None,
        point_sets=None,
        cell_sets=None,
        gmsh_periodic=None, #TODO: see if it is necessary to propagate this data
        info=None,
    )
    meshio.write(path_XDMF + filename + ".xdmf", cell_mesh)
    
    if facet_data is not None:
        facet_mesh = meshio.Mesh(
            points=points,
            cells={facet_lbl: facets},
            cell_data={"facet_marker": [facet_data]},
        )
        meshio.write(path_XDMF + filename + "_facets.xdmf", facet_mesh)




def Gmsh2XDMF():
    import sys
    prune = "-prune" in sys.argv
    msh_to_xdmf(mesh_name, prune)  # prune
