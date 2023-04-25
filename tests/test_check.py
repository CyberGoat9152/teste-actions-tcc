import requests

def test_route_check_405():
    response = requests.get("http://localhost:8080/check")
    assert response.status_code == 405
def test_route_check_401():
    response = requests.post("http://localhost:8080/check")
    assert response.status_code ==  401
def test_route_check_401_response():
    response = requests.post("http://localhost:8080/check")
    assert response.text == '{"msg":"You are unauthorized."}'

def test_route_check_401_response():
    response = requests.post("http://localhost:8080/check")
    assert response.text == '{"msg":"You are unauthorized."}'

def test_route_check_400_missing_file():
    
    url = "http://localhost:8080/check"

    payload={
        'user': '67369147-5f12-4c10-941d-827a7056682d',
        'apitoken': '32491fab-80cb-472e-92ca-8289672ce75b'
    }
    files=[]
    
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 400
    
def test_route_check_400_wrong_file():
    
    url = "http://localhost:8080/check"

    payload={
        'user': '67369147-5f12-4c10-941d-827a7056682d',
        'apitoken': '32491fab-80cb-472e-92ca-8289672ce75b'
    }
    files=[    
       ('img',('mock_wrong.webp',open('./tests/mock_wrong.webp','rb'),'image/webp'))
    ]
    
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 400
    
def test_route_check_200_wrong_file():
    
    url = "http://localhost:8080/check"

    payload={
        'user': '67369147-5f12-4c10-941d-827a7056682d',
        'apitoken': '32491fab-80cb-472e-92ca-8289672ce75b'}
    files=[    
       ('img',('mock.jpeg',open('./tests/mock.jpeg','rb'),'image/jpeg'))
    ]
    
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 200