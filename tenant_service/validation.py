"""
validate schema and data
"""
from log import Log

class Validation:
    log = Log()

    def __init__(self) -> None:
        pass

    def validate(self, reg_data_dict_list: list) -> set(bool, list):
        """
        """
        if not reg_data_dict_list: # check empty list
            self.log('empty data list')
            return False, []

        for data_dict in reg_data_dict_list:
            if list(data_dict.keys()).sort() != ['key', 'value']: # check for required keys
                return False, []
            
            # strip to remove leading or trailling spaces
            data_dict['key'] = data_dict['key'].strip()
            data_dict['value'] = data_dict['value'].strip()

            # required value checks
            if data_dict['key'] in ['', None] or data_dict['value'] in ['', None]:
                return False, []
        
        # otherwise validation success
        return True, reg_data_dict_list
    

    def validate_data_ref():
        pass

