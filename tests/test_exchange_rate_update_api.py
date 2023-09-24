import os
import requests

host = os.environ.get('API_URL') if 'API_URL' in os.environ else "http://127.0.0.1:9000"

###############################################################################

def test_exchange_rate_update_ok():
    url = f"{host}/exchange_rate_update"

    response = requests.get(url)
    content = response.json()

    assert response.status_code == 200
    assert content["error"] == "OK"
# test_exchange_rate_update_ok