from google.genai import types
from functions.get_files_info import schema_get_files_info
# types.FunctionDeclaration -- describes a single function (its name, description, and parameters).
# types.Tool -- a container that holds a list of FunctionDeclaration objects (related functions grouped together).
available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
    )