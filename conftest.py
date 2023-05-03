import pytest
import requests


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="http://localhost:3000/",
        help="This is base request url"
    )

    parser.addoption(
        "--method",
        default="get",
        choices=["get", "post", "path", "delete", "post"],
        help="method to execute"
    )

    parser.addoption(
        "--encoding",
        default=["utf-8"],
        choices=["utf-8"],
        help="encoding to execute"
    )

    parser.addoption(
        "--content-type",
        default="application/json; charset=utf-8",
        help="Expected Content-Type header value"
    )


@pytest.fixture
def api_url_military_rank_list(request):
    base_url = request.config.getoption("--url")
    return f"{base_url}resources/personnel/military_rank_list/"


@pytest.fixture
def api_url_resources_personnel_positions(request):
    base_url = request.config.getoption("--url")
    return f"{base_url}resources/personnel/positions/"


@pytest.fixture
def api_url_resources_personnel(request):
    base_url = request.config.getoption("--url")
    return f"{base_url}resources/personnel/"


@pytest.fixture
def api_url_resources(request):
    base_url = request.config.getoption("--url")
    return f"{base_url}resources"


@pytest.fixture
def api_url_works(request):
    base_url = request.config.getoption("--url")
    return f"{base_url}works"


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def request_method(request):
    return getattr(requests, request.config.getoption("--method"))


@pytest.fixture
def code():
    return 200
