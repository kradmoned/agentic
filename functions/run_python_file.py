import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args : list[str] | None = None):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.normcase(os.path.abspath(os.path.join(abs_working_directory, file_path)))
    if os.path.commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    command: list[str] = ["python", abs_file_path]
    # If there were any additional arguments then add them to the command list
    if args:
        command.extend(args)
    try:
        completed_process = subprocess.run(
            command, # THe command we are running
            cwd=abs_working_directory, # The command will be run from our working directory, if not used it will then inherits the parent working directory may break program and functionality
            capture_output= True, # Capture both std.out and std_errr
            text= True, # Format the output from bytes to string
            timeout= 30 # A timer of 30 seconds is set so it doesnt run forever
            )
        output_string: str = ""
        if completed_process.returncode != 0:
            output_string = f"Process exited with code {completed_process.returncode}\n"
        if not completed_process.stdout and not completed_process.stderr :
            output_string += "No output produced\n"
        else:
            output_string += f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name= "run_python_file",
    description= "Run python file in a specified path relative to the working directory, optionally take arguments in the form of a list of strings, returns stdout and stderr if they occurred",
    parameters= types.Schema(
        type= types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type= types.Type.STRING,
                description= "Path of a python file relative to the working directory"
            ),
            "args" : types.Schema(
                type= types.Type.ARRAY,
                description= "A list of optional command line string arguments to be passed to python program",
                items= types.Schema(
                    type= types.Type.STRING,
                    description= "A single string argument"
                )
            ),

        },
        required=["file_path"]
    )
)