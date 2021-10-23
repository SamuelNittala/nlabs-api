import requests, json

from requests.api import head

url = "http://localhost:5000/"
token = ""
headers = {"Content-Type": "application/json"}

def test_create_advisors():

    admin_create_request = requests.post(url+"admin", headers=headers)

    admin_data = {"username": "admin", "email": "admin@admin.com", "password": "admin"}

    admin_login_req = requests.post(url+"user/login", headers=headers, data=json.dumps(admin_data))
    token = admin_login_req.json()["token"]

    headers_auth = {"Content-Type": "application/json", "Authorization": "Bearer "+ token}

    data = {"username": "adfafa", "url": "afafa.com/afa.jpg"}
    advisor_create_req = requests.post(url+"/admin/advisor", data=json.dumps(data), headers=headers_auth)
    assert advisor_create_req.status_code == 201

    data = {"username": "rarafafa", "url": "rara.com/rfa.jpg"}
    advisor_create_req = requests.post(url+"/admin/advisor", data=json.dumps(data), headers=headers_auth)
    assert advisor_create_req.status_code == 201

    data = {"username": "rarafafa", "url": "rara.com/rfa.jpg"}
    advisor_create_req = requests.post(url+"/admin/advisor", data=json.dumps(data), headers=headers_auth)
    assert advisor_create_req.status_code == 202
