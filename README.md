# Railway connectivity test (no credentials)

This package runs one HTTPS server-discovery and ENet handshake check directly
from Railway. It does not load config.json, submit account credentials, or join
a world. No public port, HTTP server, domain, health check or volume is needed.

1. Confirm your account has a Full Trial. Limited Trial outbound-port restrictions
   may prevent game connections and make a failed ENet result inconclusive.
2. Extract this ZIP into a fresh folder, create a GitHub repository containing
   ONLY these extracted files, and connect that repository to a Railway service.
   Keep Dockerfile at the repository root. Do not upload your main sentry folder
   or config.json. No environment variables or secrets are required.
3. Use the Dockerfile start command (no override). Set the service restart policy
   to Never. Do not configure a public domain or HTTP health check.
4. Deploy once and copy the JSON from deployment logs. `server_data: true` plus
   `enet: true` indicates transport reachability, not proven account login.
5. The process exits after the check (normally under a minute); a stopped or
   completed service is expected. Stop/delete the test service afterward.

The completed diagnostic exits zero even if reachability failed, avoiding
restart-on-failure loops. The JSON fields, not exit status, show test success.

The image uses only Python's standard library. Package installation is not
needed. Direct Growtopia traffic originates from Railway's IP, not your home IP.

This is a trial experiment, not a promise of indefinitely free hosting. Railway
documents $5/up to 30 days followed by a Free plan with $1 monthly credit. Actual
24/7 affordability must be measured after a working sentry deployment.

References checked 2026-11-08:
- https://docs.railway.com/pricing/free-trial
- https://docs.railway.com/networking/outbound-networking

No railway.json is included: Railway currently says new services cannot opt into
the deprecated Config as Code format. Configure the few settings above in the UI.
