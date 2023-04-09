import json
import os,sys


def get_table_dependencies(query: str) -> list:
    """
    input : From clause
    output: list of table names without duplicates
    Split the FROM clause by JOIN keyword from query snd returns the list of table name
    """
    query = query.lower()
    join_clauses = query.split('join')
    # Extract table names from each JOIN clause
    table_names = []
    for clause in join_clauses:
        clause = clause.strip()
        table_name = clause.split(' ')[0]
        table_names.append(table_name)
    return list(set(table_names))
    

def get_value_from_json(json_data: dict, key = "from") -> dict: 
    """
    input : source json content
    output: From key value from the input json content 
    Recursive function to get value for a given key from a nested JSON object
    """
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                return v
            else:
                value = get_value_from_json(v, key)
                if value is not None:
                    return value
    elif isinstance(json_data, list):
        for item in json_data:
            value = get_value_from_json(item, key)
            if value is not None:
                return value   
    


def build_table_graph(config_files: list ) -> dict:
    """
    input : file path
    output: table dependency dictionary 
    This function takes a file path as input and parses the corresponding JSON configuration file. It extracts all FROM clauses 
    and constructs a dictionary of dependencies between tables. 
    """

    # Initialize an empty dictionary to store the graph
    table_graph = {}
    
    # Loop through each config file
    for file_name in config_files:
        with open(file_name) as f:
            config_data = json.load(f)
        
        # Extract the FROM clause from the query
        from_value = get_value_from_json(config_data)
        query = from_value['S']
        #query = config_data['query']['L'][0]['M']['from']['S']
        
        # Get the table dependencies from the query
        table_dependencies = get_table_dependencies(query)
        
        # Add the table to the graph if it doesn't exist
        table_name = config_data['schema']['S'] + '.' + config_data['table']['S']
        if table_name not in table_graph:
            table_graph[table_name] = []
        
        # Add the dependencies to the graph
        for dependency in table_dependencies:
            dependency_name = dependency.strip()
            if dependency_name != '':
                if dependency_name not in table_graph:
                    table_graph[dependency_name] = []
                table_graph[table_name].append(dependency_name)
    return table_graph
    

def print_table_graph(table_graph: dict , table_name: str, indent_level=0) -> str:
    """
    input : table dependency dictionary
    output: table dependency structure 
    """
    # Print the table name at the current indent level
    print(('   ' * indent_level) + table_name)
    
    # Recursively print the table's dependencies
    for dependency in table_graph[table_name]:
        print_table_graph(table_graph, dependency, indent_level + 1)
        

if __name__ == "__main__":

    path = sys.argv[1]
    table_name = sys.argv[2]
    config_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.json')]
    table_graph = build_table_graph(config_files)
    print_table_graph(table_graph, table_name)
