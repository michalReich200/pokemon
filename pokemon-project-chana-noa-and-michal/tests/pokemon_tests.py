import pytest
import requests

server_url = "localhost:5000/"


def test_update_types():
    url = f'{server_url}/update_types/a'
    res = requests.get(url=url)
    assert res == "no data"
