from unittest.mock import Mock, patch
import requests
from monitor import check_service


@patch("monitor.requests.get")
def test_successful_response_is_up(mock_get):
    response = Mock()
    response.status_code = 200
    mock_get.return_value = response

    result = check_service("https://example.com")

    assert result["status"] == "UP"
    assert result["http_status"] == 200
    assert result["response_ms"] >= 0


@patch("monitor.requests.get")
def test_server_error_is_down(mock_get):
    response = Mock()
    response.status_code = 503
    mock_get.return_value = response

    result = check_service("https://example.com")

    assert result["status"] == "DOWN"
    assert result["http_status"] == 503


@patch("monitor.requests.get", side_effect=requests.Timeout("timed out"))
def test_timeout_is_down(mock_get):
    result = check_service("https://example.com", timeout=0.01)

    assert result["status"] == "DOWN"
    assert "timed out" in result["message"]
