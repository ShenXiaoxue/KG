# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:41:30 2023

@author: me1xs
"""

class Product2Analytical():
    def __init__(self, product, analytical, properties=None):
        self.product = product
        self.analytical = analytical
        self.properties = properties if properties else {}
        self.type = "has_analytical_model"
        
    def create_relationship(self, tx):
        if self.product.node is None or self.analytical.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.product.nodeType} {{{self.product.identified_by}: $product_name}}), "
            f"(b:{self.analytical.nodeType} {{{self.analytical.identified_by}: $analytical_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "product_name": self.product.nodeProperties[self.product.identified_by],
            "analytical_name": self.analytical.nodeProperties[self.analytical.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Analytical2Input():
    def __init__(self, analytical, analyticalinput, properties=None):
        self.analytical = analytical
        self.analyticalinput = analyticalinput
        self.properties = properties if properties else {}
        self.type = "has_input"
        
    def create_relationship(self, tx):
        if self.analytical.node is None or self.analyticalinput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.analytical.nodeType} {{{self.analytical.identified_by}: $analytical_name}}), "
            f"(b:{self.analyticalinput.nodeType} {{{self.analyticalinput.identified_by}: $analyticalinput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "analytical_name": self.analytical.nodeProperties[self.analytical.identified_by],
            "analyticalinput_name": self.analyticalinput.nodeProperties[self.analyticalinput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]

class AnalyticalInput2Parameter():
    def __init__(self, analyticalinput, parameter, properties=None):
        self.analyticalinput = analyticalinput
        self.parameter = parameter
        self.properties = properties if properties else {}
        self.type = "has_parameter"
        
    def create_relationship(self, tx):
        if self.analyticalinput.node is None or self.parameter.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.analyticalinput.nodeType} {{{self.analyticalinput.identified_by}: $analyticalinput_name}}), "
            f"(b:{self.parameter.nodeType} {{{self.parameter.identified_by}: $parameter_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "analyticalinput_name": self.analyticalinput.nodeProperties[self.analyticalinput.identified_by],
            "parameter_name": self.parameter.nodeProperties[self.parameter.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Parameter2Value():
    def __init__(self, parameter, parameter_value,  properties=None):
        self.parameter = parameter
        self.parameter_value = parameter_value
        self.properties = properties if properties else {}
        self.type = "has_value"
        
    def create_relationship(self, tx):
        if self.parameter.node is None or self.parameter_value.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")

        # Ensure the correct properties are being used for matching
        parameter_name = self.parameter.nodeProperties.get(self.parameter.identified_by)
        parameter_value = self.parameter_value.nodeProperties.get(self.parameter_value.identified_by)
        parameter_label = self.parameter_value.nodeProperties.get('label')
        
        if parameter_name is None or parameter_value is None or parameter_label is None:
            raise ValueError("Parameter name, parameter value, or label not found in node properties.")

        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        prop_string = f", {prop_string}" if prop_string else ""
        query = (
            f"MATCH (a:{self.parameter.nodeType} {{{self.parameter.identified_by}: $parameter_name}}), "
            f"(b:{self.parameter_value.nodeType} {{{self.parameter_value.identified_by}: $parameter_value, label: $parameter_label}}) "
            #f"WHERE b.{self.parameter_value.parameter_label} = $parameter_name "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"   # ordering cas there might be multiple results
        )
        parameters = {
            "parameter_name": self.parameter.nodeProperties[self.parameter.identified_by],
            "parameter_value": self.parameter_value.nodeProperties[self.parameter_value.identified_by],
            "parameter_label": parameter_label,
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Parameter2Unit():
    def __init__(self, parameter, parameter_unit,  properties=None):
        self.parameter = parameter
        self.parameter_unit = parameter_unit
        self.properties = properties if properties else {}
        self.type = "has_unit"
        
    def create_relationship(self, tx):
        if self.parameter.node is None or self.parameter_unit.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.parameter.nodeType} {{{self.parameter.identified_by}: $parameter_name}}), "
            f"(b:{self.parameter_unit.nodeType} {{{self.parameter_unit.identified_by}: $parameter_unit}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "parameter_name": self.parameter.nodeProperties[self.parameter.identified_by],
            "parameter_unit": self.parameter_unit.nodeProperties[self.parameter_unit.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Analytical2Output():
    def __init__(self, analytical, analyticaloutput,properties=None):
        self.analytical = analytical
        self.analyticaloutput = analyticaloutput
        self.properties = properties if properties else {}
        self.type = "has_output"
        
    def create_relationship(self, tx):
        if self.analytical.node is None or self.analyticaloutput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.analytical.nodeType} {{{self.analytical.identified_by}: $analytical_name}}), "
            f"(b:{self.analyticaloutput.nodeType} {{{self.analyticaloutput.identified_by}: $analyticaloutput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "analytical_name": self.analytical.nodeProperties[self.analytical.identified_by],
            "analyticaloutput_name": self.analyticaloutput.nodeProperties[self.analyticaloutput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class AnalyticalOutput2Data():
    def __init__(self, analyticaloutput, analyticaldata, properties=None):
        self.analyticaloutput = analyticaloutput
        self.analyticaldata = analyticaldata
        self.properties = properties if properties else {}
        self.type = "has_data"
        
    def create_relationship(self, tx):
        if self.analyticaloutput.node is None or self.analyticaldata.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.analyticaloutput.nodeType} {{{self.analyticaloutput.identified_by}: $analyticaloutput_name}}), "
            f"(b:{self.analyticaldata.nodeType} {{{self.analyticaldata.identified_by}: $analyticaldata_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "analyticaloutput_name": self.analyticaloutput.nodeProperties[self.analyticaloutput.identified_by],
            "analyticaldata_name": self.analyticaldata.nodeProperties[self.analyticaldata.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class AnalyticalData2Value():
    def __init__(self, analyticaldata, parameter_value, properties=None):
        self.analyticaldata = analyticaldata
        self.parameter_value = parameter_value
        self.properties = properties if properties else {}
        self.type = "has_value"
        
    def create_relationship(self, tx):
        if self.analyticaldata.node is None or self.parameter_value.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.analyticaldata.nodeType} {{{self.analyticaldata.identified_by}: $analyticaldata_name}}), "
            f"(b:{self.parameter_value.nodeType} {{{self.parameter_value.identified_by}: $parameter_value}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "analyticaldata_name": self.analyticaldata.nodeProperties[self.analyticaldata.identified_by],
            "parameter_value": self.parameter_value.nodeProperties[self.parameter_value.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]
