import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def verify_recaptcha(token: str, secret_key: str) -> bool:
    """Verify reCAPTCHA token with Google's API."""
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": secret_key, "response": token}
    data = urlencode(payload).encode("utf-8")

    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urlopen(request) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        result = json.loads(response.read().decode(charset))
        return bool(result.get("success", False))
