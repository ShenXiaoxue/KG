# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:41:30 2023

@author: me1xs
"""

import glob
import numpy as np
import re
import os
import csv

     
class Component2Component():
    def __init__(self, component1, component2, type_, properties=None):
        self.component1 = component1
        self.component2 = component2
        self.properties = properties if properties else {}
        self.type = type_
        
    def create_relationship(self, tx):
        if self.component1.node is None or self.component2.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.component1.nodeType} {{{self.component1.identified_by}: $component_name1}}), "
            f"(b:{self.component2.nodeType} {{{self.component2.identified_by}: $component_name2}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "component_name1": self.component1.nodeProperties[self.component1.identified_by],
            "component_name2": self.component2.nodeProperties[self.component2.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Product2Geometric():
    def __init__(self, product, geometric, properties=None):
        self.product = product
        self.geometric = geometric
        self.properties = properties if properties else {}
        self.type = "has_geometric"
        
    def create_relationship(self, tx):
        if self.product.node is None or self.geometric.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.product.nodeType} {{{self.product.identified_by}: $product_name}}), "
            f"(b:{self.geometric.nodeType} {{{self.geometric.identified_by}: $geometric_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "product_name": self.product.nodeProperties[self.product.identified_by],
            "geometric_name": self.geometric.nodeProperties[self.geometric.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]

     
class Geometric2Component():
    def __init__(self, geometric, component, properties=None):
        self.geometric = geometric
        self.component = component
        self.properties = properties if properties else {}
        self.type = "has_component"
        
    def create_relationship(self, tx):
        if self.geometric.node is None or self.component.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.geometric.nodeType} {{{self.geometric.identified_by}: $geometric_name}}), "
            f"(b:{self.component.nodeType} {{{self.component.identified_by}: $component_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "geometric_name": self.geometric.nodeProperties[self.geometric.identified_by],
            "component_name": self.component.nodeProperties[self.component.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Geometric2Input():
    def __init__(self, geometric, geometricinput, properties=None):
        self.geometric = geometric
        self.geometricinput = geometricinput
        self.properties = properties if properties else {}
        self.type = "has_input"
        
    def create_relationship(self, tx):
        if self.geometric.node is None or self.geometricinput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.geometric.nodeType} {{{self.geometric.identified_by}: $geometric_name}}), "
            f"(b:{self.geometricinput.nodeType} {{{self.geometricinput.identified_by}: $geometricinput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "geometric_name": self.geometric.nodeProperties[self.geometric.identified_by],
            "geometricinput_name": self.geometricinput.nodeProperties[self.geometricinput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]

class GeometricInput2Component():
    def __init__(self, geometricinput, component, properties=None):
        self.geometricinput = geometricinput
        self.component = component
        self.properties = properties if properties else {}
        self.type = "has_component"
        
    def create_relationship(self, tx):
        if self.geometricinput.node is None or self.component.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.geometricinput.nodeType} {{{self.geometricinput.identified_by}: $geometricinput_name}}), "
            f"(b:{self.component.nodeType} {{{self.component.identified_by}: $component_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "geometricinput_name": self.geometricinput.nodeProperties[self.geometricinput.identified_by],
            "component_name": self.component.nodeProperties[self.component.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Component2Parameter():
    def __init__(self, component, parameter, type_, properties=None):
        self.component = component
        self.parameter = parameter
        self.properties = properties if properties else {}
        self.type = type_
        
    def create_relationship(self, tx):
        if self.component.node is None or self.parameter.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.component.nodeType} {{{self.component.identified_by}: $component_name}}), "
            f"(b:{self.parameter.nodeType} {{{self.parameter.identified_by}: $parameter_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "component_name": self.component.nodeProperties[self.component.identified_by],
            "parameter_name": self.parameter.nodeProperties[self.parameter.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]

class Component2Material():
    def __init__(self, component, material, properties=None):
        self.component = component
        self.material = material
        self.properties = properties if properties else {}
        self.type = "has_material"
        
    def create_relationship(self, tx):
        if self.component.node is None or self.material.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.component.nodeType} {{{self.component.identified_by}: $component_name}}), "
            f"(b:{self.material.nodeType} {{{self.material.identified_by}: $material_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "component_name": self.component.nodeProperties[self.component.identified_by],
            "material_name": self.material.nodeProperties[self.material.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Material2Property():
    def __init__(self, material, material_property, type_,  properties=None):
        self.material = material
        self.material_property = material_property
        self.properties = properties if properties else {}
        self.type = type_
        
    def create_relationship(self, tx):
        if self.material.node is None or self.material_property.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.material.nodeType} {{{self.material.identified_by}: $material_name}}), "
            f"(b:{self.material_property.nodeType} {{{self.material_property.identified_by}: $material_property}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "material_name": self.material.nodeProperties[self.material.identified_by],
            "material_property": self.material_property.nodeProperties[self.material_property.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Property2Value():
    def __init__(self, material_property, property_value,  properties=None):
        self.material_property = material_property
        self.property_value = property_value
        self.properties = properties if properties else {}
        self.type = "has_value"
        
    def create_relationship(self, tx):
        if self.material_property.node is None or self.property_value.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.material_property.nodeType} {{{self.material_property.identified_by}: $material_property}}), "
            f"(b:{self.property_value.nodeType} {{{self.property_value.identified_by}: $property_value}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "material_property": self.material_property.nodeProperties[self.material_property.identified_by],
            "property_value": self.property_value.nodeProperties[self.property_value.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Property2Unit():
    def __init__(self, material_property, property_unit,  properties=None):
        self.material_property = material_property
        self.property_unit = property_unit
        self.properties = properties if properties else {}
        self.type = "has_unit"
        
    def create_relationship(self, tx):
        if self.material_property.node is None or self.property_unit.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.material_property.nodeType} {{{self.material_property.identified_by}: $material_property}}), "
            f"(b:{self.property_unit.nodeType} {{{self.property_unit.identified_by}: $property_unit}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "material_property": self.material_property.nodeProperties[self.material_property.identified_by],
            "property_unit": self.property_unit.nodeProperties[self.property_unit.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Product2Product():
    def __init__(self, product1, product2, relationship, properties=None):
        self.product1 = product1
        self.product2 = product2
        self.properties = properties if properties else {}
        self.type = relationship
        
    def create_relationship(self, tx):
        if self.product1.node is None or self.product2.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.product1.nodeType} {{product_name: $product_name1}}), "
            f"(b:{self.product2.nodeType} {{product_name: $product_name2}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "product_name1": self.product1.nodeProperties[self.product1.identified_by],
            "product_name2": self.product2.nodeProperties[self.product2.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]
        
        
class Geometric2Output():
    def __init__(self, geometric, geometricoutput,properties=None):
        self.geometric = geometric
        self.geometricoutput = geometricoutput
        self.properties = properties if properties else {}
        self.type = "has_output"
        
    def create_relationship(self, tx):
        if self.geometric.node is None or self.geometricoutput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.geometric.nodeType} {{{self.geometric.identified_by}: $geometric_name}}), "
            f"(b:{self.geometricoutput.nodeType} {{{self.geometricoutput.identified_by}: $geometricoutput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "geometric_name": self.geometric.nodeProperties[self.geometric.identified_by],
            "geometricoutput_name": self.geometricoutput.nodeProperties[self.geometricoutput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class GeometricOutput2File():
    def __init__(self, geometricoutput, outputfile, properties=None):
        self.geometricoutput = geometricoutput
        self.outputfile = outputfile
        self.properties = properties if properties else {}
        self.type = "has_file"
        
    def create_relationship(self, tx):
        if self.geometricoutput.node is None or self.outputfile.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.geometricoutput.nodeType} {{{self.geometricoutput.identified_by}: $geometricoutput_name}}), "
            f"(b:{self.outputfile.nodeType} {{{self.outputfile.identified_by}: $outputfile_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "geometricoutput_name": self.geometricoutput.nodeProperties[self.geometricoutput.identified_by],
            "outputfile_name": self.outputfile.nodeProperties[self.outputfile.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class OutputFile2OutputFile():
    def __init__(self, outputfile1, outputfile2, relationship, properties=None):
        self.outputfile1 = outputfile1
        self.outputfile2 = outputfile2
        self.properties = properties if properties else {}
        self.type = relationship
        
    def create_relationship(self, tx):
        if self.outputfile1.node is None or self.outputfile2.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.outputfile1.nodeType} {{outputfile_name: $outputfile_name1}}), "
            f"(b:{self.outputfile2.nodeType} {{outputfile_name: $outputfile_name2}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "outputfile_name1": self.outputfile1.nodeProperties[self.outputfile1.identified_by],
            "outputfile_name2": self.outputfile2.nodeProperties[self.outputfile2.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class OutputFile2FilePath():
    def __init__(self, outputfile, filepath, properties=None):
        self.outputfile = outputfile
        self.filepath = filepath
        self.properties = properties if properties else {}
        self.type = "located_at"
        
    def create_relationship(self, tx):
        if self.outputfile.node is None or self.filepath.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.outputfile.nodeType} {{outputfile_name: $outputfile_name}}), "
            f"(b:{self.filepath.nodeType} {{filepath_name: $filepath_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "outputfile_name": self.outputfile.nodeProperties[self.outputfile.identified_by],
            "filepath_name": self.filepath.nodeProperties[self.filepath.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]
