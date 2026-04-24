import os
from google.genai import types
# it is a method that writes content to a file in directory
def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath((os.path.abspath(os.path.join(working_directory,file_path))))
    if os.path.commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(abs_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    # If the directory of the file doesnt exist then create it
    os.makedirs(os.path.dirname(abs_file_path), exist_ok= True)
    try:
        # Open the file in write mode
        with open(abs_file_path, mode= "w") as f:
            f.write(content) 
    except Exception as e:
        # Incase of any errors return an error string
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content in write mode to a file path relative to working directory, create directories if file directory does not already exist, return success message of file written to and its length of content written",
    parameters= types.Schema(
        type= types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type= types.Type.STRING,
                description="path to the file to write, relative to working directory",
              
            ),
            "content": types.Schema(
                description="Content to be written to a file",
                type= types.Type.STRING
            ),

        },
        required=["file_path","content"]
    )
)