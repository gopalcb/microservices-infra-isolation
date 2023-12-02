"""
handle service routing
"""
import traceback
from log import Log
from data_processor import DataProcessor

class Routing:
    log = Log()
    processor = DataProcessor()

    def __init__(self, app) -> None:
        self.app = app

    def serve(self):
        """
        routes block
        """

        def prepare_return_object(status, payload=None):
            """
            prepare object to return from route
            """
            obj = {
                'status': status,
                'code': 200 if status else 500,
                'payload': payload
            }
            return obj
        

        @self.app.route('/', methods=['GET'])
        def index():
            return 'flask rest connected'
        

        @self.app.route('/save_registration_data', methods=['POST'])
        def save_registration_data():
            """
            """
            try:
                # set dynamodb table name to store data
                table = 'tenant'

                # process request data
                status = self.processor.process_request_data(table)
                return prepare_return_object(status)

            except Exception as e:
                self.log(str(traceback.format_exc))
                raise e
