import os
import sys

import pytest
import requests


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SQLI_DIR = os.path.join(ROOT_DIR, "vuln", "sqli")
XSS_DIR = os.path.join(ROOT_DIR, "vuln", "xss")

for path in (ROOT_DIR, SQLI_DIR, XSS_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)


def pytest_addoption(parser):
    parser.addoption(
        "--sqli-url",
        action="store",
        default=os.environ.get("SQLI_BASE_URL", ""),
        help="Base URL for SQLi app (e.g., http://127.0.0.1:1111).",
    )
    parser.addoption(
        "--xss-url",
        action="store",
        default=os.environ.get("XSS_BASE_URL", ""),
        help="Base URL for XSS app (e.g., http://127.0.0.1:1112).",
    )


class _ResponseAdapter:
    def __init__(self, response):
        self._response = response
        self.status_code = response.status_code
        self.data = response.content

    @property
    def text(self):
        return self._response.text


class _HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def get(self, path, query_string=None, follow_redirects=False, **kwargs):
        url = f"{self.base_url}{path}"
        resp = requests.get(url, params=query_string, allow_redirects=follow_redirects, **kwargs)
        return _ResponseAdapter(resp)

    def post(self, path, data=None, query_string=None, follow_redirects=False, **kwargs):
        url = f"{self.base_url}{path}"
        resp = requests.post(
            url,
            params=query_string,
            data=data,
            allow_redirects=follow_redirects,
            **kwargs,
        )
        return _ResponseAdapter(resp)


@pytest.fixture()
def xss_base_url(request):
    return request.config.getoption("--xss-url") or ""


@pytest.fixture()
def sqli_client(request):
    base_url = request.config.getoption("--sqli-url")
    if base_url:
        return _HttpClient(base_url)

    from vuln.sqli.app import create_app as create_sqli_app

    app = create_sqli_app()
    app.config["TESTING"] = True
    client = app.test_client()
    client.get("/reset")
    return client


@pytest.fixture()
def xss_client(request):
    base_url = request.config.getoption("--xss-url")
    if base_url:
        return _HttpClient(base_url)

    from vuln.xss.app import create_app as create_xss_app

    app = create_xss_app()
    app.config["TESTING"] = True
    client = app.test_client()
    client.get("/reset")
    return client
