import jsonschema
import pytest
import requests


# Check request status code
@pytest.mark.regres
@pytest.mark.parametrize("code", [200])
def test_url_status(base_url, code, request_method):
    target = base_url + "works"
    response = request_method(url=target)
    assert response.status_code == code


# Check request Encoding and Content-Type
@pytest.mark.regres
def test_url_content_type(base_url, request_method, pytestconfig):
    target = base_url + "works"
    response = request_method(url=target)
    expected_content_type = pytestconfig.getoption("content_type")
    assert response.headers["Content-Type"] == expected_content_type


# Check validate schema from answer
@pytest.mark.regres
def test_api_json_schema(base_url):
    res = requests.get(base_url + "works")

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "headers": {"type": "object"},
                "id": {"type": "integer"},
                "projectId": {"type": "integer"},
                "text": {"type": "string"},
                "duration": {"type": "integer"},
                "progress": {"type": "string"},
                "parent": {"type": "integer"},
                "typeId": {"type": "integer"},
            },
            "required": ["id", "projectId", "text"]
        }
    }

    jsonschema.validate(instance=res.json(), schema=schema)
