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
