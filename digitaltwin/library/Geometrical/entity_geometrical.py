import numpy as np
import matplotlib.pyplot as plt
import glob
#from py2neo import Node, Graph
from neo4j import GraphDatabase
#from neo4j.graph import Node
import json
import re
import csv
import os.path, time

class Product:
    identified_by = 'product_name'
    nodeType = "product"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{product_name: $product_name}}) RETURN p"
        result = tx.run(query, product_name=self.nodeProperties['product_name'])
        self.node = result.single()[0]
        return self.node


class Geometric:
    identified_by = 'geometric_name'
    nodeType = "geometric"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{geometric_name: $geometric_name}}) RETURN p"
        result = tx.run(query, geometric_name=self.nodeProperties['geometric_name'])
        self.node = result.single()[0]
        return self.node


class Component:
    identified_by = 'component_name'
    nodeType = "component"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{component_name: $component_name}}) RETURN p"
        result = tx.run(query, component_name=self.nodeProperties['component_name'])
        self.node = result.single()[0]
        return self.node



    
class Material:
    identified_by = 'material_name'
    nodeType = "material"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, material_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = material_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{material_name: $material_name}}) RETURN p"
        result = tx.run(query, material_name=self.nodeProperties['material_name'])
        self.node = result.single()[0]
        return self.node

    
class MaterialProperty:
    identified_by = 'material_property'
    nodeType = "material_property"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, material_property):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = material_property
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{material_property: $material_property}}) RETURN p"
        result = tx.run(query, material_property=self.nodeProperties['material_property'])
        self.node = result.single()[0]
        return self.node


class PropertyValue:
    identified_by = 'property_value'
    nodeType = "property_value"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, property_value):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = property_value
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{property_value: $property_value}}) RETURN p"
        result = tx.run(query, property_value=self.nodeProperties['property_value'])
        self.node = result.single()[0]
        return self.node


class PropertyUnit:
    identified_by = 'property_unit'
    nodeType = "property_unit"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, property_unit):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = property_unit
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{property_unit: $property_unit}}) RETURN p"
        result = tx.run(query, property_unit=self.nodeProperties['property_unit'])
        self.node = result.single()[0]
        return self.node

class GeometricInput:
    identified_by = 'geometricinput_name'
    nodeType = "geometricinput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, geometricinput_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = geometricinput_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{geometricinput_name: $geometricinput_name}}) RETURN p"
        result = tx.run(query, geometricinput_name=self.nodeProperties['geometricinput_name'])
        self.node = result.single()[0]
        return self.node


class GeometricOutput:
    identified_by = 'geometricoutput_name'
    nodeType = "geometricoutput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, geometricoutput_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = geometricoutput_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{geometricoutput_name: $geometricoutput_name}}) RETURN p"
        result = tx.run(query, geometricoutput_name=self.nodeProperties['geometricoutput_name'])
        self.node = result.single()[0]
        return self.node



class OutputFile:
    identified_by = 'outputfile_name'
    nodeType = "outputfile"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{outputfile_name: $file_name}}) RETURN p"
        result = tx.run(query, file_name=self.nodeProperties['outputfile_name'])
        self.node = result.single()[0]
        return self.node


class FilePath:
    identified_by = 'filepath_name'
    nodeType = "filepath"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{filepath_name: $filepath_name}}) RETURN p"
        result = tx.run(query, filepath_name=self.nodeProperties['filepath_name'])
        self.node = result.single()[0]
        return self.node
