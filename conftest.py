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
        choices=["get", "post", "path", "delete"],
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
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def request_method(request):
    return getattr(requests, request.config.getoption("--method"))
