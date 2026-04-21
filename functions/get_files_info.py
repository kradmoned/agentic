import os
def get_files_info(working_directory, directory = "."):
    abs_working_directory = os.path.abspath(working_directory)
    # Getting the absolute path of target directory and normalizing it
    target_directory = os.path.normpath(os.path.join(abs_working_directory, directory))
    # Check whether the target directory is inside abs_working drectory to prevent the llm from going out of scope
    if os.path.commonpath([target_directory, abs_working_directory]) != abs_working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    try:
        # Each file property entry contains info about something in a directory
        file_properties = []
        # for each file in directory get its information
        for file in os.listdir(target_directory):
            file_path = os.path.join(target_directory,file)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            file_property = f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"
            file_properties.append(file_property)
        file_properties = "\n".join(file_properties)   
    except Exception as e:
        return f"Error:{e}"
    return file_properties
    
