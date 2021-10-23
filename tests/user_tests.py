import requests, json

from requests.api import head

url = "http://localhost:5000/"
token = ""
headers = {"Content-Type": "application/json"}

def test_user_register():
    data = { "username": "samuel", "email": "sam@gmail.com", "password": "12345"}
    r = requests.post(url+"user/register", data= json.dumps(data), headers = headers)
    assert r.status_code == 201

    #try to re-register
    r = requests.post(url+"user/register", data= json.dumps(data), headers = headers)
    assert r.status_code == 202

def test_user_login():
    data = {"email": "sam@gmail.com", "password": "12345"}
    r = requests.post(url+"user/login", data=json.dumps(data), headers=headers)
    token = r.json()["token"]
    assert r.status_code == 201

    #invalid-details
    data = {"email": "sam@gmail.com", "password": "123456"}
    r = requests.post(url+"user/login", data=json.dumps(data), headers=headers)
    assert r.status_code == 401

def test_get_advisors():
    data = {"email": "sam@gmail.com", "password": "12345"}
    r = requests.post(url+"user/login", data=json.dumps(data), headers=headers)
    token = r.json()["token"]

    headers_auth = {"Content-Type": "application/json", "Authorization": "Bearer " + token}

    r = requests.get(url+"user/2/advisor", headers=headers_auth)
    assert r.status_code == 201

