# -*- coding: utf-8 -*-

class Analytical:
    identified_by = 'analytical_name'
    nodeType = "analytical"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, analytical_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = analytical_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{analytical_name: $analytical_name}}) RETURN p"
        result = tx.run(query, analytical_name=self.nodeProperties['analytical_name'])
        self.node = result.single()[0]
        return self.node


class AnalyticalInput:
    identified_by = 'analyticalinput_name'
    nodeType = "analyticalinput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, analyticalinput_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = analyticalinput_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{analyticalinput_name: $analyticalinput_name}}) RETURN p"
        result = tx.run(query, analyticalinput_name=self.nodeProperties['analyticalinput_name'])
        self.node = result.single()[0]
        return self.node


class Parameter:
    identified_by = 'parameter_name'
    nodeType = "parameter"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, parameter_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = parameter_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{parameter_name: $parameter_name}}) RETURN p"
        result = tx.run(query, parameter_name=self.nodeProperties['parameter_name'])
        self.node = result.single()[0]
        return self.node


class ParameterValue:
    identified_by = 'parameter_value'
    nodeType = "parameter_value"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, parameter_value, parameter_label=None):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = parameter_value
        if parameter_label is not None:
            self.nodeProperties['label'] = parameter_label
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        # query = f"CREATE (p:{self.nodeType} {{parameter_value: $parameter_value"
        # if 'label' in self.nodeProperties:
        #     query += ", label: $parameter_label"
        # query += "}}) RETURN p"

        # params = {'parameter_value': self.nodeProperties[self.identified_by]}
        # if 'label' in self.nodeProperties:
        #     params['parameter_label'] = self.nodeProperties['label']
        if 'label' in self.nodeProperties:
            query = f"CREATE (p:{self.nodeType} {{parameter_value: $parameter_value, label: $parameter_label}}) RETURN p"
            params = {
                'parameter_value': self.nodeProperties[self.identified_by],
                'parameter_label': self.nodeProperties['label']
            }
        else:
            query = f"CREATE (p:{self.nodeType} {{parameter_value: $parameter_value}}) RETURN p"
            params = {'parameter_value': self.nodeProperties[self.identified_by]}
        
        result = tx.run(query, **params)
        self.node = result.single()[0]
        return self.node


class ParameterUnit:
    identified_by = 'parameter_unit'
    nodeType = "parameter_unit"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, parameter_unit):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = parameter_unit
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{parameter_unit: $parameter_unit}}) RETURN p"
        result = tx.run(query, parameter_unit=self.nodeProperties['parameter_unit'])
        self.node = result.single()[0]
        return self.node


class AnalyticalOutput:
    identified_by = 'analyticaloutput_name'
    nodeType = "analyticaloutput"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, analyticaloutput_name):
        self.nodeProperties = {}
        self.nodeProperties[self.identified_by] = analyticaloutput_name
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{analyticaloutput_name: $analyticaloutput_name}}) RETURN p"
        result = tx.run(query, analyticaloutput_name=self.nodeProperties['analyticaloutput_name'])
        self.node = result.single()[0]
        return self.node


class AnalyticalData:
    identified_by = 'analyticaldata_name'
    nodeType = "analyticaldata"
    equivalence = ["produce", "manufacture", "aftermath"]
    
    def __init__(self, analyticaldata_name, data_path):
        self.nodeProperties = {}
        self.data_path = data_path
        self.nodeProperties[self.identified_by] = analyticaldata_name
        self.nodeProperties[self.data_path] = data_path
        self.node = None  # Placeholder for a Node instance, if needed
        
    def create_node(self, tx):
        # Use a transaction to create a node in the database
        query = f"CREATE (p:{self.nodeType} {{analyticaldata_name: $analyticaldata_name}}) RETURN p"
        result = tx.run(query, analyticaldata_name=self.nodeProperties['analyticaldata_name'])
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

