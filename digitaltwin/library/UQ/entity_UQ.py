# -*- coding: utf-8 -*-

import numpy as np
import os

class UQ:
    identified_by = 'uq_name'
    nodeType = "uq"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, uq_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = uq_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{uq_name: $uq_name}}) RETURN p"
        result = tx.run(query, uq_name=self.nodeProperties['uq_name'])
        self.node = result.single()[0]
        return self.node

class UQInput:
    identified_by = 'uqinput_name'
    nodeType = "uqinput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, uqinput_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = uqinput_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{uqinput_name: $uqinput_name}}) RETURN p"
        result = tx.run(query, uqinput_name=self.nodeProperties['uqinput_name'])
        self.node = result.single()[0]
        return self.node


class UQOutput:
    identified_by = 'uqoutput_name'
    nodeType = "uqoutput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, uqoutput_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = uqoutput_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{uqoutput_name: $uqoutput_name}}) RETURN p"
        result = tx.run(query, uqoutput_name=self.nodeProperties['uqoutput_name'])
        self.node = result.single()[0]
        return self.node


class Data:
    identified_by = 'data_name'
    nodeType = "data"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, data_name, data_path):
        self.nodeProperties = {}
        self.data_path = data_path
        self.nodeProperties[self.identified_by] = data_name
        #self.nodeProperties[self.data_path] = data_path
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{data_name: $data_name}}) RETURN p"
        result = tx.run(query, data_name=self.nodeProperties['data_name'])
        self.node = result.single()[0]
        return self.node

    def data(self):
        file_ = self.data_path + self.nodeProperties[self.identified_by] + ".npy"
        if os.path.exists(file_):
            self.data_ = np.load(file_)
        else:
            print("The file does not exist")
        #print(self.data_.shape)
        return self.data_



