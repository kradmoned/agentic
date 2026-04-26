from google.genai import types
from functions.get_files_info import schema_get_files_info,get_files_info
from functions.get_file_content import schema_get_file_content,get_file_content
from functions.write_file import schema_write_file,write_file
from functions.run_python_file import schema_run_python_file ,run_python_file
from config import WORKING_DIRECTORY
# types.FunctionDeclaration -- describes a single function (its name, description, and parameters).
# types.Tool -- a container that holds a list of FunctionDeclaration objects (related functions grouped together).
available_functions = types.Tool(
    function_declarations=[
        schema_run_python_file,
        schema_get_file_content, schema_write_file, schema_get_files_info]
    )
def call_function(function_call: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    # Create a function map to dispacth function based on function_call.name
    function_map = {
        "get_files_info" : get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    # function_call.name can be none in that case we assign it ""
    function_name = function_call.name or ""
    # FUnction given by llm can not be from available functions thus we return an errorf
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts= types.Part.from_function_response(
                name=function_name,
                response={"error":f"Unknown function: {function_name}"}
            ),
            )
    # Create the copy of the args dictionary
    # The args is a dicitionary mapping keyworded arguments to value such as verbose=True
    # We create a  shallwcopy of this as we need to inject the working directory in to the args
    args = dict(function_call.args) if function_call.args else {}
    # Inject the working directory added to the arguments
    args["working_directory"] = WORKING_DIRECTORY
    # The ** operator automatically adds the dictionary arguments to the functions
    function_result: str = function_map[function_name](**args)
    # return the succesful result
    return types.Content(
        role="tool",
        parts= [types.Part.from_function_response(
            name=function_name,
            response={"result": function_result}
        )]
    )


        
