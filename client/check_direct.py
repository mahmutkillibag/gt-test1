"""One credential-free direct HTTPS/ENet check; intended for a remote host."""
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))


def check():
    import auth
    import netguard
    import proxy_transport
    from enet import ENetClient
    from login import PROTOCOL, GAME_VERSION
    proxy_transport.configure(None)
    netguard.install()
    result = {"mode": "direct", "account_login_attempted": False,
              "server_data": False, "enet": False}
    client = None
    stage = "server_data"
    try:
        sd = auth.fetch_server_data(PROTOCOL, GAME_VERSION, timeout=12)
        result[stage] = True
        result["game_endpoint"] = [sd["server"], int(sd["port"])]
        stage = "enet"
        client = ENetClient(*result["game_endpoint"])
        client.connect()
        deadline = time.monotonic() + 12
        while not client.connected and time.monotonic() < deadline:
            client.service(0.05)
            time.sleep(0.01)
        result[stage] = client.connected
        result["accepted_enet_packets"] = client._rx
        if not client.connected:
            raise TimeoutError("no ENet VERIFY_CONNECT")
    except Exception as exc:
        result.update(failed_stage=stage, error="%s: %s" % (type(exc).__name__, str(exc)[:350]))
    finally:
        if client is not None:
            client.disconnect()
    return result


if __name__ == "__main__":
    # A completed diagnostic exits zero even when reachability fails, to avoid
    # platform restart-on-failure loops. Read the JSON enet/server_data fields.
    print(json.dumps(check(), indent=2), flush=True)
