# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:09:23 2023

@author: me1xs
"""
import numpy as np
#from py2neo import Graph, Node, NodeMatcher
from neo4j import GraphDatabase
#import entity as et
#import relation as rel
from .Geometrical.entity_geometrical import Product,Geometric, Component, Material, MaterialProperty, PropertyValue, PropertyUnit, GeometricInput, GeometricOutput, OutputFile, FilePath
from .ODE.entity_analytical import Analytical,AnalyticalInput, Parameter, ParameterValue, ParameterUnit, AnalyticalOutput, AnalyticalData

from .Gmsh.entity_gmsh import Meshing, MeshingInput, MeshingOutput

from .UQ.entity_UQ import UQ, UQInput, UQOutput, Data

from .Geometrical.relation_geometrical import Product2Geometric,Geometric2Component, Component2Material, Material2Property, Property2Value, Property2Unit, Component2Component, Component2Parameter, Geometric2Input, GeometricInput2Component, Geometric2Output, GeometricOutput2File, OutputFile2OutputFile, OutputFile2FilePath

from .Gmsh.relation_gmsh import Product2Meshing, Meshing2Input, Meshing2Output, MeshingInput2Parameter, MeshingInput2OutputFile, MeshingOutput2OutputFile

#from relation_geometrical import Component2Component

from .ODE.relation_analytical import Product2Analytical, Parameter2Value, Parameter2Unit, Analytical2Input, AnalyticalInput2Parameter, Analytical2Output, AnalyticalOutput2Data, AnalyticalData2Value

from .UQ.relation_UQ import Product2UQ, UQ2Input, UQ2Output, UQInput2Data, UQOutput2Data

from .FEM.entity_FEM import FEM, FEMAnalysis, FEMInput, Mesh, FEMModelParameter, FEMOutput, BoundaryCondition, Force
from .FEM.relation_FEM import Product2FEM, FEM2Analysis, FEMAnalysis2Input, FEMAnalysis2Input, FEMInput2Mesh, FEMInput2Material, FEMInput2Parameter, FEMModelParameter2Value, FEMAnalysis2Output, FEMInput2BounaryCondition, FEMInput2Force, Mesh2Outputfile


import time
import glob
import csv
import os.path
import re



class Database:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def deleteAll(self):
        with self.driver.session() as session:
            session.execute_write(self._delete_all)

    def _delete_all(self, tx):
        query = "MATCH (n) DETACH DELETE n"
        tx.run(query)
        
    def add_product(self, product):
        #print("all good 2")
        with self.driver.session() as session:
            return session.execute_write(product.create_node)
            #return session.write_transaction(product.create_node)
            #print("all good 3")
        

    def add_geometric(self, geometric):
        with self.driver.session() as session:
            return session.execute_write(geometric.create_node)

    def add_component(self, component):
        with self.driver.session() as session:
            return session.execute_write(component.create_node)

    def add_material(self, material):
        with self.driver.session() as session:
            return session.execute_write(material.create_node)

    def add_material_property(self, material_property):
        with self.driver.session() as session:
            return session.execute_write(material_property.create_node)

    def add_property_value(self, property_value):
        with self.driver.session() as session:
            return session.execute_write(property_value.create_node)


    def add_property_unit(self, property_unit):
        with self.driver.session() as session:
            return session.execute_write(property_unit.create_node)

    #####################################################################

    def add_product2geometric(self, product2geometric):
        with self.driver.session() as session:
            return session.execute_write(product2geometric.create_relationship)

    def add_geometric2component(self, geometric2component):
        with self.driver.session() as session:
            return session.execute_write(geometric2component.create_relationship)


    def add_component2material(self, component2material):
        with self.driver.session() as session:
            return session.execute_write(component2material.create_relationship)

    def add_material2property(self, material2property):
        with self.driver.session() as session:
            return session.execute_write(material2property.create_relationship)

    def add_property2value(self, property2value):
        with self.driver.session() as session:
            return session.execute_write(property2value.create_relationship)

    def add_property2unit(self, property2unit):
        with self.driver.session() as session:
            return session.execute_write(property2unit.create_relationship)

    def add_component2parameter(self, component2parameter):
        with self.driver.session() as session:
            return session.execute_write(component2parameter.create_relationship)

    def add_geometricinput(self, geometricinput):
        with self.driver.session() as session:
            return session.execute_write(geometricinput.create_node)

    def add_geometricoutput(self, geometricoutput):
        with self.driver.session() as session:
            return session.execute_write(geometricoutput.create_node)

    def add_outputfile(self, outputfile):
        with self.driver.session() as session:
            return session.execute_write(outputfile.create_node)

    def add_filepath(self, filepath):
        with self.driver.session() as session:
            return session.execute_write(filepath.create_node)
    

    # Geometrical relationship
    def add_component2component(self, component2component):
        with self.driver.session() as session:
            return session.execute_write(component2component.create_relationship)

    def add_geometric2input(self, geometric2input):
        with self.driver.session() as session:
            return session.execute_write(geometric2input.create_relationship)

    def add_geometricinput2component(self, geometricinput2component):
        with self.driver.session() as session:
            return session.execute_write(geometricinput2component.create_relationship)

    def add_geometric2output(self, geometric2output):
        with self.driver.session() as session:
            return session.execute_write(geometric2output.create_relationship)

    def add_geometricoutput2file(self, geometricoutput2file):
        with self.driver.session() as session:
            return session.execute_write(geometricoutput2file.create_relationship)

    def add_outputfile2outputfile(self, outputfile2outputfile):
        with self.driver.session() as session:
            return session.execute_write(outputfile2outputfile.create_relationship)

    def add_outputfile2filepath(self, outputfile2filepath):
        with self.driver.session() as session:
            return session.execute_write(outputfile2filepath.create_relationship)

    #####################################################################
    # Meshing entity
    def add_meshing(self, meshing):
        with self.driver.session() as session:
            return session.execute_write(meshing.create_node)

    def add_meshinginput(self, meshinginput):
        with self.driver.session() as session:
            return session.execute_write(meshinginput.create_node)

    def add_meshingoutput(self, meshingoutput):
        with self.driver.session() as session:
            return session.execute_write(meshingoutput.create_node)

    # Meshing relationship
    def add_product2meshing(self, product2meshing):
        with self.driver.session() as session:
            return session.execute_write(product2meshing.create_relationship)

    def add_meshing2input(self, meshing2input):
        with self.driver.session() as session:
            return session.execute_write(meshing2input.create_relationship)

    def add_meshing2output(self, meshing2output):
        with self.driver.session() as session:
            return session.execute_write(meshing2output.create_relationship)

    def add_meshinginput2parameter(self, meshinginput2parameter):
        with self.driver.session() as session:
            return session.execute_write(meshinginput2parameter.create_relationship)

    def add_meshinginput2outputfile(self, meshinginput2outputfile):
        with self.driver.session() as session:
            return session.execute_write(meshinginput2outputfile.create_relationship)

    def add_meshingoutput2outputfile(self, meshingoutput2outputfile):
        with self.driver.session() as session:
            return session.execute_write(meshingoutput2outputfile.create_relationship)

    

    #####################################################################

    # Analytical model -> parameters
    def add_analytical(self, analytical):
        with self.driver.session() as session:
            return session.execute_write(analytical.create_node)

    def add_analyticalinput(self, analyticalinput):
        with self.driver.session() as session:
            return session.execute_write(analyticalinput.create_node)
    
    def add_parameter(self, parameter):
        with self.driver.session() as session:
            return session.execute_write(parameter.create_node)

    def add_parameter_value(self, parameter_value):
        with self.driver.session() as session:
            return session.execute_write(parameter_value.create_node)


    def add_parameter_unit(self, parameter_unit):
        with self.driver.session() as session:
            return session.execute_write(parameter_unit.create_node)

    def add_analyticaloutput(self, analyticaloutput):
        with self.driver.session() as session:
            return session.execute_write(analyticaloutput.create_node)

    def add_analyticaldata(self, analyticaldata):
        with self.driver.session() as session:
            return session.execute_write(analyticaldata.create_node)

    

    # Analytical relationship
    def add_product2analytical(self, product2analytical):
        with self.driver.session() as session:
            return session.execute_write(product2analytical.create_relationship)

    def add_analytical2input(self, analytical2input):
        with self.driver.session() as session:
            return session.execute_write(analytical2input.create_relationship)
        
    def add_analyticalinput2parameter(self, analyticalinput2parameter):
        with self.driver.session() as session:
            return session.execute_write(analyticalinput2parameter.create_relationship)

    def add_parameter2value(self, parameter2value):
        with self.driver.session() as session:
            return session.execute_write(parameter2value.create_relationship)

    def add_parameter2unit(self, parameter2unit):
        with self.driver.session() as session:
            return session.execute_write(parameter2unit.create_relationship)

    def add_analytical2output(self, analytical2output):
        with self.driver.session() as session:
            return session.execute_write(analytical2output.create_relationship)

    def add_analytical2output(self, analytical2output):
        with self.driver.session() as session:
            return session.execute_write(analytical2output.create_relationship)

    def add_analyticaloutput2data(self, analyticaloutput2data):
        with self.driver.session() as session:
            return session.execute_write(analyticaloutput2data.create_relationship)

    def add_analyticaldata2value(self, analyticaldata2value):
        with self.driver.session() as session:
            return session.execute_write(analyticaldata2value.create_relationship)

    #####################################################################

    # Bayesian UQ
    def add_uq(self, uq):
        with self.driver.session() as session:
            return session.execute_write(uq.create_node)

    def add_uqinput(self, uqinput):
        with self.driver.session() as session:
            return session.execute_write(uqinput.create_node)

    def add_uqoutput(self, uqoutput):
        with self.driver.session() as session:
            return session.execute_write(uqoutput.create_node)

    def add_data(self, data):
        with self.driver.session() as session:
            return session.execute_write(data.create_node)

    ###
    # Bayesian UQ relationship
    def add_product2uq(self, product2uq):
        with self.driver.session() as session:
            return session.execute_write(product2uq.create_relationship)

    def add_uq2input(self, uq2input):
        with self.driver.session() as session:
            return session.execute_write(uq2input.create_relationship)

    def add_uq2output(self, uq2output):
        with self.driver.session() as session:
            return session.execute_write(uq2output.create_relationship)

    def add_uqinput2data(self, uqinput2data):
        with self.driver.session() as session:
            return session.execute_write(uqinput2data.create_relationship)

    def add_uqoutput2data(self, uqoutput2data):
        with self.driver.session() as session:
            return session.execute_write(uqoutput2data.create_relationship)

    #####################################################################
    # FEM entities
    def add_fem(self, fem):
        with self.driver.session() as session:
            return session.execute_write(fem.create_node)

    def add_femanalysis(self, femanalysis):
        with self.driver.session() as session:
            return session.execute_write(femanalysis.create_node)

    def add_feminput(self, feminput):
        with self.driver.session() as session:
            return session.execute_write(feminput.create_node)

    def add_mesh(self, mesh):
        with self.driver.session() as session:
            return session.execute_write(mesh.create_node)

    def add_femmodelparameter(self, femmodelparameter):
        with self.driver.session() as session:
            return session.execute_write(femmodelparameter.create_node)

    def add_femoutput(self, femoutput):
        with self.driver.session() as session:
            return session.execute_write(femoutput.create_node)

    def add_boundarycondition(self, boundarycondition):
        with self.driver.session() as session:
            return session.execute_write(boundarycondition.create_node)

    def add_force(self, force):
        with self.driver.session() as session:
            return session.execute_write(force.create_node)

    # FEM relationships
    def add_product2fem(self, product2fem):
        with self.driver.session() as session:
            return session.execute_write(product2fem.create_relationship)

    def add_fem2analysis(self, fem2analysis):
        with self.driver.session() as session:
            return session.execute_write(fem2analysis.create_relationship)

    def add_femanalysis2input(self, femanalysis2input):
        with self.driver.session() as session:
            return session.execute_write(femanalysis2input.create_relationship)

    def add_feminput2mesh(self, feminput2mesh):
        with self.driver.session() as session:
            return session.execute_write(feminput2mesh.create_relationship)

    def add_feminput2material(self, feminput2material):
        with self.driver.session() as session:
            return session.execute_write(feminput2material.create_relationship)

    def add_feminput2parameter(self, feminput2parameter):
        with self.driver.session() as session:
            return session.execute_write(feminput2parameter.create_relationship)

    def add_femmodelparameter2value(self, femmodelparameter2value):
        with self.driver.session() as session:
            return session.execute_write(femmodelparameter2value.create_relationship)

    def add_femanalysis2output(self, femanalysis2output):
        with self.driver.session() as session:
            return session.execute_write(femanalysis2output.create_relationship)

    def add_feminput2boundarycondition(self, feminput2boundarycondition):
        with self.driver.session() as session:
            return session.execute_write(feminput2boundarycondition.create_relationship)

    def add_feminput2force(self, feminput2force):
        with self.driver.session() as session:
            return session.execute_write(feminput2force.create_relationship)

    def add_mesh2outputfile(self, mesh2outputfile):
        with self.driver.session() as session:
            return session.execute_write(mesh2outputfile.create_relationship)

    #####################################################################
    
    
    #####################################################################
    #  Additional relationships
    def com2com(self, com1name, com2name, type_, parameters=None):
        # Ensure that `parameters` is a dictionary if not provided.
        if parameters is None:
            parameters = {}

        # Add component names to the parameters dictionary.
        parameters.update({"com1name": com1name, "com2name": com2name})
        query = (
            f"MATCH (a:Component {{component_name: $com1name}}), "
            f"(b:Component {{component_name: $com2name}}) "
            f"CREATE (a)-[r: {type_}]->(b) "
            f"RETURN r"
        )
        with self.driver.session() as session:
            result = session.run(query, parameters)
            session.execute_write(result.single()[0])
            print("RUN")


def list_files_in_folder(folder_path):
    try:
        # List all files in the specified folder
        files = os.listdir(folder_path)
        # Filter out directories
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        files_without_suffix = [os.path.splitext(f)[0] for f in files if os.path.isfile(os.path.join(folder_path, f))]
        return files, files_without_suffix
    except Exception as e:
        return str(e)



class knowledgeGraph:
    def __init__(self):
        self.db = Database("bolt://neo4j:7687", "neo4j", "12345678")
        ###############################
        self.db.deleteAll()
        self.product_3storyFloor = Product("Three_story_Floor")
        self.db.add_product(self.product_3storyFloor)
        # Add analytical parameters
        self.analy_model = Analytical("ODE_MassSpringDamper") 
        self.db.add_analytical(self.analy_model)
        # product -> analytical
        self.db.add_product2analytical(Product2Analytical(self.product_3storyFloor, self.analy_model))
        # analytical -> input
        self.analyticalinput_ = AnalyticalInput("Parameters")
        self.db.add_analyticalinput(self.analyticalinput_)
        self.db.add_analytical2input(Analytical2Input(self.analy_model, self.analyticalinput_))
        # analytical-> parameters
        analy_m, analy_k, analy_c = ["m1", "m2", "m3"], ["k1", "k2", "k3"], ["c1", "c2", "c3"]
        m, k, c = [5.0394, 4.9919, 4.9693], [34958.3691, 43195.1237, 43295.9086], [7.8963, 4.0129, 5.4905]
        unit_ = ["kg", "N/m", "Ns/m"]
        analy_m_unit = ParameterUnit(unit_[0])
        analy_k_unit = ParameterUnit(unit_[1])
        analy_c_unit = ParameterUnit(unit_[2])
        self.db.add_parameter_unit(analy_m_unit)
        self.db.add_parameter_unit(analy_k_unit)
        self.db.add_parameter_unit(analy_c_unit)
        #
        for i in range(0, 3):
            analy_m_ = Parameter(analy_m[i])
            analy_k_ = Parameter(analy_k[i])
            analy_c_ = Parameter(analy_c[i])
            self.db.add_parameter(analy_m_)
            self.db.add_parameter(analy_k_)
            self.db.add_parameter(analy_c_)
            self.db.add_analyticalinput2parameter(AnalyticalInput2Parameter(self.analyticalinput_, analy_m_))
            self.db.add_analyticalinput2parameter(AnalyticalInput2Parameter(self.analyticalinput_, analy_k_))
            self.db.add_analyticalinput2parameter(AnalyticalInput2Parameter(self.analyticalinput_, analy_c_))
            analy_m_value = ParameterValue(str(m[i]), analy_m[i])
            analy_k_value = ParameterValue(str(k[i]), analy_k[i])
            analy_c_value = ParameterValue(str(c[i]), analy_c[i])
            self.db.add_parameter_value(analy_m_value)
            self.db.add_parameter_value(analy_k_value)
            self.db.add_parameter_value(analy_c_value)
            #
            self.db.add_parameter2value(Parameter2Value(analy_m_, analy_m_value))
            self.db.add_parameter2value(Parameter2Value(analy_k_, analy_k_value))
            self.db.add_parameter2value(Parameter2Value(analy_c_, analy_c_value))
            #
            self.db.add_parameter2unit(Parameter2Unit(analy_m_, analy_m_unit))
            self.db.add_parameter2unit(Parameter2Unit(analy_k_, analy_k_unit))
            self.db.add_parameter2unit(Parameter2Unit(analy_c_, analy_c_unit))

        ###############
        # Blender geometric
        self.geometric_ = Geometric("Geometric")
        self.db.add_geometric(self.geometric_)
        self.db.add_product2geometric(Product2Geometric(self.product_3storyFloor, self.geometric_))
        geometricInput_ = GeometricInput("GeoInput")
        self.db.add_geometricinput(geometricInput_)
        self.db.add_geometric2input(Geometric2Input(self.geometric_, geometricInput_))
        # floor, pillar, block, V, H
        components_ = ["floor", "pillar", "block", "V", "H"]
        directions_ = ["Len_", "Wid_", "Hei_"]
        dimensions_ = np.array([[0.3005, 0.25, 0.0255],   # L_f, B_f, H_f  floor
                       [0.0065, 0.0255, 0.555],           # L_p, B_p, H_p  pillar
                       [0.0125, 0.0255, 0.0255],          # L_b, B_b, H_b  block
                       [0.0065, 0.0255, 0.05-0.0065],     # L_s_V, B_s_V, H_s_V,  V
                       [0.05, 0.0255, 0.0065]])           # L_s_H, B_s_H, H_s_H    H

        L_f, B_f, H_f = dimensions_[0, 0], dimensions_[0, 1], dimensions_[0, 2]
        L_p, B_p, H_p = dimensions_[1, 0], dimensions_[1, 1], dimensions_[1, 2]
        L_b, B_b, H_b = dimensions_[2, 0], dimensions_[2, 1], dimensions_[2, 2]
        L_s_V, B_s_V, H_s_V = dimensions_[3, 0], dimensions_[3, 1], dimensions_[3, 2]
        L_s_H, B_s_H, H_s_H = dimensions_[4, 0], dimensions_[4, 1], dimensions_[4, 2]

        parameter_ = {}
        for i in range(0, 5):
            for j in range(0, 3):
                instance_name = f"{directions_[j]} + {components_[i]}"
                parameter_[instance_name] = Parameter(directions_[j] + components_[i])
                parameter_value_ = ParameterValue(dimensions_[i, j], directions_[j] + components_[i])
                self.db.add_parameter(parameter_[instance_name])
                self.db.add_parameter_value(parameter_value_)
                self.db.add_parameter2value(Parameter2Value(parameter_[instance_name], parameter_value_))
        
        #############
        type_dim = ["has_length", "has_width", "has_height"]
        # three floors
        for j in range(0, 3):
            # floor
            component_floor = Component("Floor_"+str(j+1))
            self.db.add_component(component_floor)
            self.db.add_geometricinput2component(GeometricInput2Component(geometricInput_, component_floor))
            loc_ = (0, 0, 0.0255/2.0 + (i+1) * (0.555 - 0.0255) / 3.0)
            parameter_loc = Parameter(f"Loc_Floor_{str(j)}")
            parameter_locValue = ParameterValue(str(loc_), f"Loc_Floor_{str(j)}")
            self.db.add_parameter(parameter_loc)
            self.db.add_parameter_value(parameter_locValue)
            self.db.add_parameter2value(Parameter2Value(parameter_loc, parameter_locValue))
            self.db.add_component2parameter(Component2Parameter(component_floor, parameter_loc, "has_loc"))
            for k in range(0, 3):
                self.db.add_component2parameter(Component2Parameter(component_floor, parameter_[f"{directions_[k]} + {components_[0]}"], type_dim[k]))
            
        # four pillars
        for i in range(0, 4):
            component_pillar = Component("Pillar_"+str(i+1))
            self.db.add_component(component_pillar)
            self.db.add_geometricinput2component(GeometricInput2Component(geometricInput_, component_pillar))
            # loc of the four pillars
            if i==0:
                m, n = -1, -1
            elif i==1:
                m, n = -1, 1
            elif i==2:
                m, n = 1, -1
            elif i==3:
                m, n = 1, 1
            loc_ = (m*(L_f + L_p)/2.0, n*(B_f - B_p)/2.0, H_p/2.0)
            parameter_loc = Parameter(f"Loc_Pillar_{str(i)}")
            parameter_locValue = ParameterValue(str(loc_), f"Loc_Pillar_{str(i)}")
            self.db.add_parameter(parameter_loc)
            self.db.add_parameter_value(parameter_locValue)
            self.db.add_parameter2value(Parameter2Value(parameter_loc, parameter_locValue))
            self.db.add_component2parameter(Component2Parameter(component_pillar, parameter_loc, "has_loc"))
            ################
            for k in range(0, 3):
                self.db.add_component2parameter(Component2Parameter(component_pillar, parameter_[f"{directions_[k]} + {components_[1]}"], type_dim[k]))
            for j in range(0, 3):
                component_block = Component("Block_" + str(i) + "_" + str(j))
                self.db.add_component(component_block)
                self.db.add_geometricinput2component(GeometricInput2Component(geometricInput_, component_block))
                self.db.add_component2component(Component2Component(component_pillar, component_block, "adjacent"))  # pillar and 3 blocks
                loc_ = (m*(L_f + L_p*2 + L_b)/2.0, n*(B_f - B_p)/2.0, 0.0255/2.0 + (j+1) * (0.555 - 0.0255) / 3.0)   ##
                parameter_loc = Parameter(f"Loc_block_{str(i)}_{str(j)}")
                parameter_locValue = ParameterValue(str(loc_), f"Loc_block_{str(i)}_{str(j)}")
                self.db.add_parameter(parameter_loc)
                self.db.add_parameter_value(parameter_locValue)
                self.db.add_parameter2value(Parameter2Value(parameter_loc, parameter_locValue))
                self.db.add_component2parameter(Component2Parameter(component_block, parameter_loc, "has_loc"))
                for o in range(0, 3):
                    self.db.add_component2parameter(Component2Parameter(component_block, parameter_[f"{directions_[o]} + {components_[2]}"], type_dim[o]))
            ###
            # the vertical plate
            component_V = Component("V_plate"+str(i+1))
            self.db.add_component(component_V)
            self.db.add_geometricinput2component(GeometricInput2Component(geometricInput_, component_V))
            #
            loc_ = (m*(L_f + L_p*2 + L_s_V)/2.0, n*(B_f - B_p)/2.0, (0.05 - 0.0065)/2.0)
            parameter_loc = Parameter(f"Loc_V_{str(i)}")
            parameter_locValue = ParameterValue(str(loc_), f"Loc_V_{str(i)}")
            self.db.add_parameter(parameter_loc)
            self.db.add_parameter_value(parameter_locValue)
            self.db.add_parameter2value(Parameter2Value(parameter_loc, parameter_locValue))
            self.db.add_component2parameter(Component2Parameter(component_V, parameter_loc, "has_loc"))
            #
            for k in range(0, 3):
                self.db.add_component2parameter(Component2Parameter(component_V, parameter_[f"{directions_[k]} + {components_[3]}"], type_dim[k]))
            # the horizontal plate
            component_H = Component("H_plate"+str(i+1))
            self.db.add_component(component_H)
            self.db.add_geometricinput2component(GeometricInput2Component(geometricInput_, component_H))
            #
            loc_ = (m*(L_f + L_p*2 + L_s_H)/2.0, n*(B_f - B_p)/2.0,  -0.0065/2.0)
            parameter_loc = Parameter(f"Loc_H_{str(i)}")
            parameter_locValue = ParameterValue(str(loc_), f"Loc_H_{str(i)}")
            self.db.add_parameter(parameter_loc)
            self.db.add_parameter_value(parameter_locValue)
            self.db.add_parameter2value(Parameter2Value(parameter_loc, parameter_locValue))
            self.db.add_component2parameter(Component2Parameter(component_H, parameter_loc, "has_loc"))
            for k in range(0, 3):
                self.db.add_component2parameter(Component2Parameter(component_H, parameter_[f"{directions_[k]} + {components_[4]}"], type_dim[k]))


        ############
        # STL to MSH
        gmsh_ = Meshing("Meshing")
        self.db.add_meshing(gmsh_)
        self.db.add_product2meshing(Product2Meshing(self.product_3storyFloor, gmsh_))
        #
        self.gmshinput_ = MeshingInput("Gmsh_input")
        self.db.add_meshinginput(self.gmshinput_)
        self.db.add_meshing2input(Meshing2Input(gmsh_, self.gmshinput_))
        #
        self.gmshoutput_ = MeshingOutput("Gmsh_output")
        self.db.add_meshingoutput(self.gmshoutput_)
        self.db.add_meshing2output(Meshing2Output(gmsh_, self.gmshoutput_))
        #
        # angle_surface_ = Parameter("angle_surface_dection")
        # mesh_size = Parameter("mesh_size")
        # geoTolBoolean_ = Parameter("Geometry_tolerance_boolean")
        # curveAngle_ = Parameter("curve_angle")
        parameters_ = ["angle_surface_dection", "mesh_size", "Geometry_tolerance_boolean", "curve_angle"]
        values_ = [40, 0.02, 1e-4, 180]
        for i in range(0, len(parameters_)):
            para_ = Parameter(parameters_[i])
            value_ = ParameterValue(str(values_[i]), parameters_[i])
            self.db.add_parameter(para_)
            self.db.add_parameter_value(value_)
            self.db.add_meshinginput2outputfile(MeshingInput2OutputFile(self.gmshinput_, para_))
            self.db.add_parameter2value(Parameter2Value(para_, value_))
        
        



        
        #############
        # Material
        material_aluminum = Material("al6082")
        self.db.add_material(material_aluminum)
        ####
        aluminum_density = MaterialProperty("density")
        aluminum_youngsmodulus = MaterialProperty("youngsmodulus")
        aluminum_possionsratio = MaterialProperty("possionsratio")
        self.db.add_material_property(aluminum_density)
        self.db.add_material_property(aluminum_youngsmodulus)
        self.db.add_material_property(aluminum_possionsratio)
        ####
        aluminum_density_value = PropertyValue("2700")
        aluminum_density_unit = PropertyUnit("kg/m3")
        self.db.add_property_value(aluminum_density_value)
        self.db.add_property_unit(aluminum_density_unit)
        ####
        aluminum_E_value = PropertyValue("70e9")
        aluminum_E_unit = PropertyUnit("N/m2")
        self.db.add_property_value(aluminum_E_value)
        self.db.add_property_unit(aluminum_E_unit)
        ####
        aluminum_mu_value = PropertyValue("0.3")
        aluminum_mu_unit = PropertyUnit("-")
        self.db.add_property_value(aluminum_mu_value)
        self.db.add_property_unit(aluminum_mu_unit)
        #########
        self.db.add_property2value(Property2Value(aluminum_density, aluminum_density_value))
        self.db.add_property2unit(Property2Unit(aluminum_density, aluminum_density_unit))
        #
        self.db.add_property2value(Property2Value(aluminum_youngsmodulus, aluminum_E_value))
        self.db.add_property2unit(Property2Unit(aluminum_youngsmodulus, aluminum_E_unit))
        #
        self.db.add_property2value(Property2Value(aluminum_possionsratio, aluminum_mu_value))
        self.db.add_property2unit(Property2Unit(aluminum_possionsratio, aluminum_mu_unit))
        ####
        self.db.add_material2property(Material2Property(material_aluminum, aluminum_density, "has_density"))
        self.db.add_material2property(Material2Property(material_aluminum, aluminum_youngsmodulus, "has_E"))
        self.db.add_material2property(Material2Property(material_aluminum, aluminum_possionsratio, "has_mu"))

        
        # FEM
        data_path_ = "./digitaltwin/Data/FEM/"
        fem_ = FEM("FEM")
        self.db.add_fem(fem_)
        self.db.add_product2fem(Product2FEM(self.product_3storyFloor, fem_))
        #
        fem_modal = FEMAnalysis("ModalAnalysis")
        self.db.add_femanalysis(fem_modal)
        self.db.add_fem2analysis(FEM2Analysis(fem_, fem_modal))
        #
        fem_steadystate = FEMAnalysis("SteadyState")
        self.db.add_femanalysis(fem_steadystate)
        self.db.add_fem2analysis(FEM2Analysis(fem_, fem_steadystate))
        #
        fem_modal_input_ = FEMInput("Modal_Input")
        self.db.add_feminput(fem_modal_input_)
        self.db.add_femanalysis2input(FEMAnalysis2Input(fem_modal, fem_modal_input_))
        #
        fem_steady_input_ = FEMInput("Steady_Input")
        self.db.add_feminput(fem_steady_input_)
        self.db.add_femanalysis2input(FEMAnalysis2Input(fem_steadystate, fem_steady_input_))
        #
        self.mesh_ = Mesh("Mesh", data_path_)
        self.db.add_mesh(self.mesh_)
        self.db.add_feminput2mesh(FEMInput2Mesh(fem_modal_input_, self.mesh_))
        self.db.add_feminput2mesh(FEMInput2Mesh(fem_steady_input_, self.mesh_))
        #
        self.db.add_feminput2material(FEMInput2Material(fem_modal_input_, material_aluminum))
        self.db.add_feminput2material(FEMInput2Material(fem_steady_input_, material_aluminum))
        #
        # modal analysis parameters
        num_freqs = FEMModelParameter("NoEigen")
        self.db.add_femmodelparameter(num_freqs)
        self.db.add_feminput2parameter(FEMInput2Parameter(fem_modal_input_, num_freqs))
        num_ = ParameterValue("12")
        self.db.add_parameter_value(num_)
        self.db.add_femmodelparameter2value(FEMModelParameter2Value(num_freqs, num_))
        #
        # modal analysis output
        eigen_freqs = FEMOutput("EigenFreqs")
        self.db.add_femoutput(eigen_freqs)
        self.db.add_femanalysis2output(FEMAnalysis2Output(fem_modal, eigen_freqs))
        eigen_vectors = FEMOutput("EigenVecs")
        self.db.add_femoutput(eigen_vectors)
        self.db.add_femanalysis2output(FEMAnalysis2Output(fem_modal, eigen_vectors))
        # Steady-state
        bc_ = BoundaryCondition("BC", data_path_)
        self.db.add_boundarycondition(bc_)
        self.db.add_feminput2boundarycondition(FEMInput2BounaryCondition(fem_steady_input_, bc_))
        force_ = Force("Impluse", data_path_)
        self.db.add_force(force_)
        self.db.add_feminput2force(FEMInput2Force(fem_steady_input_, force_))
        #
        fem_disp = FEMOutput("FEM_Disp")
        self.db.add_femoutput(fem_disp)
        self.db.add_femanalysis2output(FEMAnalysis2Output(fem_steadystate, fem_disp))

        


    
    def ODE(self):
        #db = Database("bolt://localhost:7687", "neo4j", "12345678")
        # analytical output
        analyoutput_ = AnalyticalOutput("Results")
        self.db.add_analyticaloutput(analyoutput_)
        self.db.add_analytical2output(Analytical2Output(self.analy_model, analyoutput_))
        ######
        folder_path = "./digitaltwin/Data/ODE/"
        files, files_without_suffix  = list_files_in_folder(folder_path)
        for file_, file_without_suffix_ in zip(files, files_without_suffix):
            #print(file_, file_without_suffix_)
            analyoutputdata_ = AnalyticalData(file_without_suffix_, folder_path + file_)
            self.db.add_analyticaldata(analyoutputdata_)
            self.db.add_analyticaloutput2data(AnalyticalOutput2Data(analyoutput_, analyoutputdata_))
            data_value_ = np.load(folder_path + file_)
            #print(data_value_)
            value_ = ParameterValue(str(data_value_))
            self.db.add_parameter_value(value_)
            self.db.add_analyticaldata2value(AnalyticalData2Value(analyoutputdata_, value_))

    def Geometric(self):
         geometricoutput_ = GeometricOutput("Output")
         self.db.add_geometricoutput(geometricoutput_)
         self.db.add_geometric2output(Geometric2Output(self.geometric_, geometricoutput_))
         #####
         self.stlFile_ = OutputFile("STL")
         self.db.add_outputfile(self.stlFile_)
         self.db.add_geometricoutput2file(GeometricOutput2File(geometricoutput_, self.stlFile_))
         #stlFilePath_ = FilePath("Three_story_floor.stl")
         #self.db.add_filepath(FilePath(stlFilePath_))
         #self.db.add_outputfile2filepath(OutputFile2FilePath(self.stlFile_, stlFilePath_))

    def Gmsh_(self):
        self.gmshoutputFile_ = OutputFile("MSH")
        self.db.add_outputfile(self.gmshoutputFile_)
        self.db.add_outputfile2outputfile(OutputFile2OutputFile(self.stlFile_, self.gmshoutputFile_, "Transform_Msh"))
        self.db.add_meshinginput2outputfile(MeshingInput2OutputFile(self.gmshinput_, self.stlFile_))
        self.db.add_meshingoutput2outputfile(MeshingOutput2OutputFile(self.gmshoutput_, self.gmshoutputFile_))
        #mshFilePath_ = FilePath('./digitaltwin/Data/Gmsh/Floor_msh/Three_story_floor.msh')
        #self.db.add_filepath(FilePath(mshFilePath_))
        #self.db.add_outputfile2filepath(OutputFile2FilePath(self.gmshoutput_, mshFilePath_))

    def Gmsh2XDMF(self):
        self.xdmfoutput_ = OutputFile("XDMF")
        self.db.add_outputfile(self.xdmfoutput_)
        self.db.add_outputfile2outputfile(OutputFile2OutputFile(self.gmshoutputFile_, self.xdmfoutput_, "Tranform_XDMF"))
        xdmf_ = ["Three_Floor_structure.h5", "Three_Floor_structure.xdmf", "Three_Floor_structure_facets.h5", "Three_Floor_structure_facets.xdmf"]
        for i in range(0, 4):
           xdmfFile_ = OutputFile(xdmf_[i])
           self.db.add_outputfile(xdmfFile_)
           self.db.add_outputfile2outputfile(OutputFile2OutputFile(self.xdmfoutput_, xdmfFile_, "has_XDMF_file"))
        
        

    def FEM_(self):
        self.db.add_mesh2outputfile(Mesh2Outputfile(self.mesh_, self.xdmfoutput_))
                                
            

        

    
    

    
"""
    # Add UQ
    uq_ = UQ("Bayesian")
    db.add_uq(uq_)
    db.add_product2uq(Product2UQ(product_3storyFloor, uq_))
    #
    uqinput_ = UQInput("Displacment")
    db.add_uqinput(uqinput_)
    db.add_uq2input(UQ2Input(uq_, uqinput_))
    #
    
    tt_ =  Data("tt", data_path_)
    xx_ = Data("displacements", data_path_)
    noise_ = Data("noise", data_path_)
    db.add_data(tt_)
    db.add_data(xx_)
    db.add_data(noise_)
    
    db.add_uqinput2data(UQInput2Data(uqinput_, tt_))
    db.add_uqinput2data(UQInput2Data(uqinput_, xx_))
    db.add_uqinput2data(UQInput2Data(uqinput_, noise_))
    
    #
    uqoutput_ = UQOutput("parameters")
    uqoutput_k1 = Data("k1", data_path_)
    uqoutput_k2 = Data("k2", data_path_)
    uqoutput_k3 = Data("k3", data_path_)
    db.add_uqoutput(uqoutput_)
    db.add_data(uqoutput_k1)
    db.add_data(uqoutput_k2)
    db.add_data(uqoutput_k3)
    #
    db.add_uq2output(UQ2Output(uq_, uqoutput_))
    #
    db.add_uqoutput2data(UQOutput2Data(uqoutput_, uqoutput_k1))
    db.add_uqoutput2data(UQOutput2Data(uqoutput_, uqoutput_k2))
    db.add_uqoutput2data(UQOutput2Data(uqoutput_, uqoutput_k3))

    #############
    # FEM
    fem_ = FEM("FEM")
    db.add_fem(fem_)
    db.add_product2fem(Product2FEM(product_3storyFloor, fem_))
    #
    fem_modal = FEMAnalysis("ModalAnalysis")
    db.add_femanalysis(fem_modal)
    db.add_fem2analysis(FEM2Analysis(fem_, fem_modal))
    #
    fem_steadystate = FEMAnalysis("SteadyState")
    db.add_femanalysis(fem_steadystate)
    db.add_fem2analysis(FEM2Analysis(fem_, fem_steadystate))
    #
    fem_modal_input_ = FEMInput("Modal_Input")
    db.add_feminput(fem_modal_input_)
    db.add_femanalysis2input(FEMAnalysis2Input(fem_modal, fem_modal_input_))
    #
    fem_steady_input_ = FEMInput("Steady_Input")
    db.add_feminput(fem_steady_input_)
    db.add_femanalysis2input(FEMAnalysis2Input(fem_steadystate, fem_steady_input_))
    #
    mesh_ = Mesh("Mesh", data_path_)
    db.add_mesh(mesh_)
    db.add_feminput2mesh(FEMInput2Mesh(fem_modal_input_, mesh_))
    db.add_feminput2mesh(FEMInput2Mesh(fem_steady_input_, mesh_))
    #
    db.add_feminput2material(FEMInput2Material(fem_modal_input_, material_aluminum))
    db.add_feminput2material(FEMInput2Material(fem_steady_input_, material_aluminum))
    #
    # modal analysis parameters
    num_freqs = FEMModelParameter("NoEigen")
    db.add_femmodelparameter(num_freqs)
    db.add_feminput2parameter(FEMInput2Parameter(fem_modal_input_, num_freqs))
    num_ = ParameterValue("12")
    db.add_parameter_value(num_)
    db.add_femmodelparameter2value(FEMModelParameter2Value(num_freqs, num_))
    #
    # modal analysis output
    eigen_freqs = FEMOutput("EigenFreqs")
    db.add_femoutput(eigen_freqs)
    db.add_femanalysis2output(FEMAnalysis2Output(fem_modal, eigen_freqs))
    eigen_vectors = FEMOutput("EigenVecs")
    db.add_femoutput(eigen_vectors)
    db.add_femanalysis2output(FEMAnalysis2Output(fem_modal, eigen_vectors))
    # Steady-state
    bc_ = BoundaryCondition("BC", data_path_)
    db.add_boundarycondition(bc_)
    db.add_feminput2boundarycondition(FEMInput2BounaryCondition(fem_steady_input_, bc_))
    force_ = Force("Impluse", data_path_)
    db.add_force(force_)
    db.add_feminput2force(FEMInput2Force(fem_steady_input_, force_))
    #
    fem_disp = FEMOutput("FEM_Disp")
    db.add_femoutput(fem_disp)
    db.add_femanalysis2output(FEMAnalysis2Output(fem_steadystate, fem_disp))

"""



    

                       
