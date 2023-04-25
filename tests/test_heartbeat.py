import requests

def test_route_heartbeat():
    response = requests.get("http://localhost:8080/")
    assert response.status_code == 200