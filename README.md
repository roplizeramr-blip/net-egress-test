# net-egress-test

Minimal Docker app used to test outbound internet (egress) from a container
running on CranL.

- `GET /` runs DNS, raw TCP and HTTPS checks from inside the container and
  returns the results as JSON.
- `GET /healthz` returns `OK`.

Build: `docker build -t net-egress-test .`
Run: `docker run -p 3000:3000 net-egress-test`
