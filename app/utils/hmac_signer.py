import hmac, hashlib, base64, time
from app.core.config import settings

def now_ts() -> str:
    return str(int(time.time()))

def sign(method: str, path: str, body: bytes, ts: str, secret: str) -> str:
    msg = f"{method.upper()}|{path}|{ts}|".encode() + body
    mac = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
    return base64.b64encode(mac).decode()

def verify_signature(method: str, path: str, body: bytes, ts: str, signature: str, secret: str) -> bool:
    try:
        if abs(int(time.time()) - int(ts)) > settings.CLOCK_SKEW_SECONDS:
            return False
    except Exception:
        return False
    expected = sign(method, path, body, ts, secret)
    return hmac.compare_digest(expected, signature)