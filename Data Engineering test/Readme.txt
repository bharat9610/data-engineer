Readme

How to execute your code:

Execute the batch file in the command prompt as below to output the dependency graph for the table name "games.nulls".
The output will be redirected to the output.log file in the current directory.

	execute_my_script.bat

To execute in command prompt,

python my_script.py "<json-file-directory>" "<table-name>" 

example:

python my_script.py ".\tables" "games.nulls"


 
Approach: 
 
1. The solution approach is to parse the JSON configuration files.
2. Extract the table names from the FROM clause of the SQL query from the json content using get_value_from_json.
3. Create a dictionary using the table names as keys and dependent table names as values.
		{
		"table_name":["dependency_table_1","dependency_table_2",...],
		...,
		}
4. The dictionary is then traversed in a Recursive manner to print out the table and its dependencies in required format.



Code Explanation:

1.build_table_graph

	build_table_graph function is responsible for reading the json content and building the table graph dictionary.

2. get_value_from_json 

	Recursive function to get "From" key values from a nested JSON object.


3. get_table_dependencies 

	The get_table_dependencies function takes a FROM clause and returns a list of all tables referenced in that clause.
	

4. print_table_dependencies 
    The print_table_dependencies function recursively prints out the dependencies of a given table in a hierarchical format


Assumptions:

1. This code assumes that all JSON configuration files are stored in a directory as will be given as input 1.
2. The schema_name.table_name parameter specifies the starting point for the dependency graph and it should be provided as input 2.
3. The solution assumes that each table is uniquely identified by its name and schema, which is in the format of "schema-name.table-name".



