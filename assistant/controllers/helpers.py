
import traceback
from assistant.controllers import get_logger
import os
import json
import yaml
import pandas as pd
class HELPER:
    """
    A class to manage helper functions.
    """
    def __init__(self, log_folder:str,log_filename:str):
        self.logger = get_logger.get_logger_object(__name__,log_folder, log_filename)

    def error_handling(self,err):
        traceback_info = traceback.format_exc()
        self.logger.error(f"Internal server exception occured: {str(err)}", exc_info=True)
        api_response = {
            "error": f"Internal server exception occured.",
            "message": "Retry the request. If the error persists check the logs.",
            "traceback": traceback_info,
            "status_code" : 500
        }

        return api_response


    def get_file_extension(self,file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension

    def file_handler(self,filepath):
        file_extension = self.get_file_extension(filepath)
        try:
            if file_extension in ['.json','.yaml']:
                with open(filepath,"r") as file:
                    data = json.load(file) if file_extension ==".json" else yaml.safe_load(file)
            elif file_extension in ['.csv','.xlsx']:
                data = pd.read_excel(filepath) if file_extension ==".xlsx" else pd.read_csv(filepath,low_memory=False)
            self.logger.info(f"File: '{filepath}' is loaded")
        except Exception as err:
            raise
        return data

    def check_boolean_param(self,param):
        if param.lower() == "false":
            return False
        elif param.lower() == "true":
            return True
        else:
            raise Exception("Only boolean is allowed")
