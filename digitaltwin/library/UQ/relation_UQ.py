# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:41:30 2023

@author: me1xs
"""

class Product2UQ():
    def __init__(self, product, uq, properties=None):
        self.product = product
        self.uq = uq
        self.properties = properties if properties else {}
        self.type = "has_uq"
        
    def create_relationship(self, tx):
        if self.product.node is None or self.uq.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.product.nodeType} {{{self.product.identified_by}: $product_name}}), "
            f"(b:{self.uq.nodeType} {{{self.uq.identified_by}: $uq_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "product_name": self.product.nodeProperties[self.product.identified_by],
            "uq_name": self.uq.nodeProperties[self.uq.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class UQ2Input():
    def __init__(self, uq, uqinput, properties=None):
        self.uq = uq
        self.uqinput = uqinput
        self.properties = properties if properties else {}
        self.type = "has_input"
        
    def create_relationship(self, tx):
        if self.uq.node is None or self.uqinput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.uq.nodeType} {{{self.uq.identified_by}: $uq_name}}), "
            f"(b:{self.uqinput.nodeType} {{{self.uqinput.identified_by}: $uqinput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "uq_name": self.uq.nodeProperties[self.uq.identified_by],
            "uqinput_name": self.uqinput.nodeProperties[self.uqinput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]

class UQ2Output():
    def __init__(self, uq, uqoutput, properties=None):
        self.uq = uq
        self.uqoutput = uqoutput
        self.properties = properties if properties else {}
        self.type = "has_output"
        
    def create_relationship(self, tx):
        if self.uq.node is None or self.uqoutput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.uq.nodeType} {{{self.uq.identified_by}: $uq_name}}), "
            f"(b:{self.uqoutput.nodeType} {{{self.uqoutput.identified_by}: $uqoutput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "uq_name": self.uq.nodeProperties[self.uq.identified_by],
            "uqoutput_name": self.uqoutput.nodeProperties[self.uqoutput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class UQInput2Data():
    def __init__(self, uqinput, data, properties=None):
        self.uqinput = uqinput
        self.data = data
        self.properties = properties if properties else {}
        self.type = "has_data"
        
    def create_relationship(self, tx):
        if self.uqinput.node is None or self.data.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.uqinput.nodeType} {{{self.uqinput.identified_by}: $uqinput_name}}), "
            f"(b:{self.data.nodeType} {{{self.data.identified_by}: $data_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "uqinput_name": self.uqinput.nodeProperties[self.uqinput.identified_by],
            "data_name": self.data.nodeProperties[self.data.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class UQOutput2Data():
    def __init__(self, uqoutput, data, properties=None):
        self.uqoutput = uqoutput
        self.data = data
        self.properties = properties if properties else {}
        self.type = "has_data"
        
    def create_relationship(self, tx):
        if self.uqoutput.node is None or self.data.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.uqoutput.nodeType} {{{self.uqoutput.identified_by}: $uqoutput_name}}), "
            f"(b:{self.data.nodeType} {{{self.data.identified_by}: $data_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "uqoutput_name": self.uqoutput.nodeProperties[self.uqoutput.identified_by],
            "data_name": self.data.nodeProperties[self.data.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]
