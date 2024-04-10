print("hello worl")


import os
import dotenv

CUR_DIR = __file__.rpartition('\\')[0]

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
    env_path = f"{CUR_DIR}\\{filename}"
    dotenv.load_dotenv(env_path)
    return os.getenv(varname)