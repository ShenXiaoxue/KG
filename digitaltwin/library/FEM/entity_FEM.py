# -*- coding: utf-8 -*-

class FEM:
    identified_by = 'fem_name'
    nodeType = "fem"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{fem_name: $fem_name}}) RETURN p"
        result = tx.run(query, fem_name=self.nodeProperties['fem_name'])
        self.node = result.single()[0]
        return self.node


class FEMAnalysis:
    identified_by = 'femanalysis_name'
    nodeType = "femanalysis"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{femanalysis_name: $femanalysis_name}}) RETURN p"
        result = tx.run(query, femanalysis_name=self.nodeProperties['femanalysis_name'])
        self.node = result.single()[0]
        return self.node


class FEMInput:
    identified_by = 'feminput_name'
    nodeType = "feminput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{feminput_name: $feminput_name}}) RETURN p"
        result = tx.run(query, feminput_name=self.nodeProperties['feminput_name'])
        self.node = result.single()[0]
        return self.node

    
class Mesh:
    identified_by = 'mesh_name'
    nodeType = "mesh"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name, data_path):
        self.nodeProperties = {}
        self.data_path = data_path
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{mesh_name: $mesh_name}}) RETURN p"
        result = tx.run(query, mesh_name=self.nodeProperties['mesh_name'])
        self.node = result.single()[0]
        return self.node

    def mesh(self):
        file_ = self.data_path + self.nodeProperties[self.identified_by] + ".xdmf"
        if os.path.exists(file_):
            self.mesh_ = file_  # xdmf.read_mesh(name="Grid")
        else:
            print("The file does not exist")
        #print(self.data_.shape)
        return self.mesh_


class BoundaryCondition:
    identified_by = 'boundarycondition_name'
    nodeType = "boundarycondition"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name, data_path):
        self.nodeProperties = {}
        self.data_path = data_path
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{boundarycondition_name: $boundarycondition_name}}) RETURN p"
        result = tx.run(query, boundarycondition_name=self.nodeProperties['boundarycondition_name'])
        self.node = result.single()[0]
        return self.node

    def boundarycondition(self):
        file_ = self.data_path + self.nodeProperties[self.identified_by] + ".xdmf"
        if os.path.exists(file_):
            self.boundarycondition_ = file_  # xdmf.read_mesh(name="Grid")
        else:
            print("The file does not exist")
        #print(self.data_.shape)
        return self.boundarycondition_


class Force:
    identified_by = 'force_name'
    nodeType = "force"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name, data_path):
        self.nodeProperties = {}
        self.data_path = data_path
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{force_name: $force_name}}) RETURN p"
        result = tx.run(query, force_name=self.nodeProperties['force_name'])
        self.node = result.single()[0]
        return self.node

    def boundarycondition(self):
        file_ = self.data_path + self.nodeProperties[self.identified_by] + ".xdmf"
        if os.path.exists(file_):
            self.force_ = file_  # xdmf.read_mesh(name="Grid")
        else:
            print("The file does not exist")
        #print(self.data_.shape)
        return self.force_


# Class for modal analysis
class FEMModelParameter:
    identified_by = 'FEMModelParameter_name'
    nodeType = "FEMModelParameter"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{FEMModelParameter_name: $FEMModelParameter_name}}) RETURN p"
        result = tx.run(query, FEMModelParameter_name=self.nodeProperties['FEMModelParameter_name'])
        self.node = result.single()[0]
        return self.node


class FEMOutput:
    identified_by = 'femoutput_name'
    nodeType = "femoutput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{femoutput_name: $femoutput_name}}) RETURN p"
        result = tx.run(query, femoutput_name=self.nodeProperties['femoutput_name'])
        self.node = result.single()[0]
        return self.node






