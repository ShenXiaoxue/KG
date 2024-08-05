class Product2Meshing():
    def __init__(self, product, meshing, properties=None):
        self.product = product
        self.meshing = meshing
        self.properties = properties if properties else {}
        self.type = "has_meshing"
        
    def create_relationship(self, tx):
        if self.product.node is None or self.meshing.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.product.nodeType} {{{self.product.identified_by}: $product_name}}), "
            f"(b:{self.meshing.nodeType} {{{self.meshing.identified_by}: $meshing_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "product_name": self.product.nodeProperties[self.product.identified_by],
            "meshing_name": self.meshing.nodeProperties[self.meshing.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Meshing2Input():
    def __init__(self, meshing, meshinginput, properties=None):
        self.meshing = meshing
        self.meshinginput = meshinginput
        self.properties = properties if properties else {}
        self.type = "has_input"
        
    def create_relationship(self, tx):
        if self.meshing.node is None or self.meshinginput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.meshing.nodeType} {{{self.meshing.identified_by}: $meshing_name}}), "
            f"(b:{self.meshinginput.nodeType} {{{self.meshinginput.identified_by}: $meshinginput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "meshing_name": self.meshing.nodeProperties[self.meshing.identified_by],
            "meshinginput_name": self.meshinginput.nodeProperties[self.meshinginput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Meshing2Output():
    def __init__(self, meshing, meshingoutput, properties=None):
        self.meshing = meshing
        self.meshingoutput = meshingoutput
        self.properties = properties if properties else {}
        self.type = "has_output"
        
    def create_relationship(self, tx):
        if self.meshing.node is None or self.meshingoutput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.meshing.nodeType} {{{self.meshing.identified_by}: $meshing_name}}), "
            f"(b:{self.meshingoutput.nodeType} {{{self.meshingoutput.identified_by}: $meshingoutput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "meshing_name": self.meshing.nodeProperties[self.meshing.identified_by],
            "meshingoutput_name": self.meshingoutput.nodeProperties[self.meshingoutput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]



class MeshingInput2Parameter():
    def __init__(self, meshinginput, parameter, properties=None):
        self.meshinginput = meshinginput
        self.parameter = parameter
        self.properties = properties if properties else {}
        self.type = "has_parameter"
        
    def create_relationship(self, tx):
        if self.meshinginput.node is None or self.parameter.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.meshinginput.nodeType} {{{self.meshinginput.identified_by}: $meshinginput_name}}), "
            f"(b:{self.parameter.nodeType} {{{self.parameter.identified_by}: $parameter_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "meshinginput_name": self.meshinginput.nodeProperties[self.meshinginput.identified_by],
            "parameter_name": self.parameter.nodeProperties[self.parameter.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]
