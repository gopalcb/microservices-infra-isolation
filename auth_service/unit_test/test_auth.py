"""
pytest - to test the auth module
items to test - 
    flask connected
    test signup
    test failed login
    test success login
"""
import pytest
import requests
import json


class TestAuth:
    def __init__(self) -> None:
        pass

    def test_rest_connected(self):
        """
        test if flask rest is connected
        """
        url = 'http://localhost:2000/'
        resp = requests.get(url)
        
        assert resp.text == 'flask rest connected'


    def test_signup(self):
        """
        test success signup
        """
        url = 'http://localhost:2000/signup'
        myobj = {
            'name': 'Test User',
            'email': 'test@gmail.com',
            'password': 'test123'
        }

        resp = requests.post(url, json = myobj)
        actual_status = json.loads(resp.text)['status']

        assert actual_status == True


    def test_failed_login(self):
        """
        test failed login
        status in response should be false
        """
        url = 'http://localhost:2000/login'
        myobj = {
            'email': 'test1@gmail.com',
            'password': 'test123-'
        }

        resp = requests.post(url, json = myobj)
        actual_status = json.loads(resp.text)['status']

        assert actual_status == False


    def test_success_login(self):
        """
        test success login
        status in response should be true
        """
        url = 'http://localhost:2000/login'
        myobj = {
            'email': 'test@gmail.com',
            'password': 'test123'
        }

        resp = requests.post(url, json = myobj)
        actual_status = json.loads(resp.text)['status']

        assert actual_status == True
