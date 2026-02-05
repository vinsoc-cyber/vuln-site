# VULN WEB

Theme: Blue Holographic / Sci-Fi theme

## Docker

Build and run all three labs:

```bash
docker compose up --build
```

Note: `docker-compose.yml` overrides the image `CMD` to run each lab.

Ports:
- SQLi: http://localhost:1111
- XSS: http://localhost:1112
- SSTI: http://localhost:1113

## Run locally (no Docker)

Install dependencies:

```bash
pip install -r requirements.txt
```

Start each lab in a separate terminal:

```bash
# SQLi
python vuln/sqli/vuln_sqli.py

# XSS
python vuln/xss/vuln_xss.py

# SSTI
python vuln/ssti/vuln_ssti.py
```

## Tests

Run all tests:

```bash
pytest -v
```

Run SQLi tests against local server:

```bash
pytest tests/test_sqli.py -v --sqli-url http://127.0.0.1:1111
```

Run XSS tests against local server:

```bash
pytest tests/test_xss.py -v --xss-url http://127.0.0.1:1112
```

You can also set environment variables instead of passing flags:

```bash
SQLI_BASE_URL=http://127.0.0.1:1111
XSS_BASE_URL=http://127.0.0.1:1112
```

## Playwright setup (browser tests)

For XSS browser-based tests, install Playwright and browsers:

```bash
pip install -r requirements.txt
python -m playwright install
```
