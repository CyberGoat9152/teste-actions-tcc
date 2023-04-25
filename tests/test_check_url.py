import requests
import json

def test_route_check_url_405():
    response = requests.get("http://localhost:8080/check-url")
    assert response.status_code == 405
def test_route_check_url_401():
    response = requests.post("http://localhost:8080/check-url")
    assert response.status_code ==  401
def test_route_check_url_401_response():
    response = requests.post("http://localhost:8080/check-url")
    assert response.text == '{"msg":"You are unauthorized."}'

def test_route_check_url_400_missing_file():
    url="http://localhost:8080/check-url"
    payload = json.dumps({
	"auth": {
            "apitoken": "32491fab-80cb-472e-92ca-8289672ce75b",
            "user": "0a7016a0-fbae-4175-ab85-e9c02259cb6e"
    	}
    })
    files=[]
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 400
 
def test_route_check_url_200_wrong_file():
    url="http://localhost:8080/check-url"
    payload = json.dumps({
        "auth": {
            "apitoken": "32491fab-80cb-472e-92ca-8289672ce75b",
            "user": "0a7016a0-fbae-4175-ab85-e9c02259cb6e"
    },
         "url": "https://img.freepik.com/fotos-gratis/comunidade-de-pessoas-adultas-torcendo-juntas_23-2148431414.jpg"
    })
    files=[]
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 200
