"""
read request params and data
"""
from flask import request
from log import Log
from validation import Validation
from dynamo_db import DynamoDB

class DataProcessor:
    log = Log()
    validation = Validation()
    dynamodb = DynamoDB()
    data_dict = {}

    def __init__(self) -> None:
        self.data_dict = request.json

    def read_tenant_info(self):
        """
        post data structure:

        request.json['tenant_signup']
        [{key, value}]
        """
        data_key = 'tenant_signup'
        if data_key not in self.data_dict.keys():
            self.log(f'missing {data_key} in json request')
            return False, {}

        return self.validation(self.data_dict[data_key]) # data param validation
    
    def process_request_data(self, table):
        """
        process http request data-
        read params data, validate and store into dynamodb table

        params:
            table: str
        return:
            status: bool
        """
        status, data_list = self.read_tenant_info()
        if not status:
            self.log('error during data reading')
            return False
        
        # prepare item object for dynamodb
        item = self.dynamodb.prepare_data_item(data_list)
        # save data into dynamodb table
        status, result = self.dynamodb.save(table, item)

        if not status:
            self.log('failed saving data')
            return False
        
        self.log('data save success')
        return True
    