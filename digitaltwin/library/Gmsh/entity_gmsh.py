class Meshing:
    identified_by = 'meshing_name'
    nodeType = "meshing"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{meshing_name: $meshing_name}}) RETURN p"
        result = tx.run(query, meshing_name=self.nodeProperties['meshing_name'])
        self.node = result.single()[0]
        return self.node


class MeshingInput:
    identified_by = 'meshinginput_name'
    nodeType = "meshinginput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, meshinginput_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = meshinginput_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{meshinginput_name: $meshinginput_name}}) RETURN p"
        result = tx.run(query, meshinginput_name=self.nodeProperties['meshinginput_name'])
        self.node = result.single()[0]
        return self.node


class MeshingOutput:
    identified_by = 'meshingoutput_name'
    nodeType = "meshingoutput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, meshingoutput_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = meshingoutput_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{meshingoutput_name: $meshingoutput_name}}) RETURN p"
        result = tx.run(query, meshingoutput_name=self.nodeProperties['meshingoutput_name'])
        self.node = result.single()[0]
        return self.node
