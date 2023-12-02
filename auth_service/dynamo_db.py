"""
perform db transactions
"""
import logging
import boto3
from botocore.exceptions import ClientError
import traceback
from log import Log

logger = logging.getLogger(__name__)

class DynamoDB:
    log = Log()
    dyn_resource = None

    def __init__(self) -> None:
        self.dyn_resource = boto3.client('dynamodb', region_name='us-east-1')

    def create_table():
        pass

    def prepare_data_item(self, data_dict_list):
        """
        format the param data into dynamodb item object
        example:
            item = {
                'key1': 'value',
                'key2': 'value'
            }
        """
        item = {}
        for data_dict in data_dict_list:
            # make key-value pair
            item[data_dict['key']] = data_dict['value']

        return item

    def save(self, table, item):
        try:
            """
            store item object into dynamodb table
            """
            response = self.dyn_resource.put_item(
                Item=item,
                TableName=table
            )
            return True, response

        except ClientError as e:
            self.log(f'Error: {e.response["Error"]["Code"]}, {e.response["Error"]["Message"]}')
            trace = traceback.format_exc()
            self.log(f'Trace: {str(trace)}')
            return False, {}

        except Exception as e:
            self.log(f'Exc: {str(e)}')
            trace = traceback.format_exc()
            self.log(f'Trace: {str(trace)}')
            return False, {}


    def get_single_item(self, table, fetch_key):
        """
        fetch_key={
            'artist': {'S': 'Arturus Ardvarkian'},
            'song': {'S': 'Carrot Eton'}
        }
        """
        try:
            response = self.dyn_resource.get_item(
                TableName=table,
                Key=fetch_key
            )
            print(response['Item'])
            return response['Item']

        except ClientError as e:
            self.log(f'Error: {e.response["Error"]["Code"]}, {e.response["Error"]["Message"]}')
            trace = traceback.format_exc()
            self.log(f'Trace: {str(trace)}')
            return False, {}

        except Exception as e:
            self.log(f'Exc: {str(e)}')
            trace = traceback.format_exc()
            self.log(f'Trace: {str(trace)}')
            return False, {}
