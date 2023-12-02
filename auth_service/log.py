"""
manage application logs
"""
import datetime

def log(self, data):
    dt = datetime.datetime
    data = f'{dt} : {data}'
    print(data)