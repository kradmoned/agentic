import os
from config import MAX_CHARS
def get_file_content(working_directory, file_path):
    # get the absolute path of working directory
    abs_working_directory  = os.path.abspath(working_directory)
    # Get the absolute path of file
    abs_file_path = os.path.normcase(os.path.abspath(os.path.join(abs_working_directory,file_path)))
    # Check if file is actually inside the directory
    if os.path.commonpath([abs_file_path,abs_working_directory]) != abs_working_directory:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try: 
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        # IF f.read(1) return any non empty string then there is additional things located in file    
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e} occured"
    return file_content_string