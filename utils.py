import os
import dotenv
import json

def get_env_var(filename: str, varname: str="documentation"):
    """Gets envirnonment variables from .env files in the directory

    Parameters
    ----------
    filename : str
        name of the file, or path to the file respective of the current directory 
    varname : type
        name of the variable inside of the actual .env file

    Returns
    -------
    variable type of variable in .env file
        the environment variable
    """

    CUR_DIR = __file__.rpartition('\\')[0]
    env_path = f"{CUR_DIR}\\{filename}"
    dotenv.load_dotenv(env_path)
    return os.getenv(varname)


def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["emp_details"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

    # python object to be appended

