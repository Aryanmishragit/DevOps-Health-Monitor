"""HTTP health-check logic."""
from time import perf_counter
import requests


def check_service(url: str, timeout: float = 5.0) -> dict:
    """Check a URL and return a normalized result.

    Any HTTP response below 500 is considered reachable (UP).
    Network errors and 5xx responses are considered DOWN.
    """
    started = perf_counter()
    checked_at = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc
    ).isoformat()
    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "DevOpsHealthMonitor/1.0"},
        )
        elapsed_ms = (perf_counter() - started) * 1000
        is_up = response.status_code < 500
        return {
            "status": "UP" if is_up else "DOWN",
            "http_status": response.status_code,
            "response_ms": round(elapsed_ms, 2),
            "message": f"HTTP {response.status_code}",
            "checked_at": checked_at,
        }
    except requests.RequestException as exc:
        elapsed_ms = (perf_counter() - started) * 1000
        return {
            "status": "DOWN",
            "http_status": None,
            "response_ms": round(elapsed_ms, 2),
            "message": str(exc)[:240],
            "checked_at": checked_at,
        }
