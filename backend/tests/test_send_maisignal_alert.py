"""Tests for send_maisignal_alert module."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from send_maisignal_alert import (
    build_payload,
    fetch_recipients,
    load_config,
    load_snowflake_config,
    load_template,
    main,
    send_alert,
)

# ── load_config ──────────────────────────────────────────────────────


class TestLoadConfig:
    def test_success_with_env_file(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("ECOMAIL_API_KEY=secret-key-123\n")
        monkeypatch.delenv("ECOMAIL_API_KEY", raising=False)

        result = load_config(env_file)

        assert result == "secret-key-123"

    def test_success_without_env_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("ECOMAIL_API_KEY", "env-var-key")
        missing = tmp_path / "nonexistent" / ".env"

        result = load_config(missing)

        assert result == "env-var-key"

    def test_missing_api_key_raises(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("OTHER_VAR=value\n")
        monkeypatch.delenv("ECOMAIL_API_KEY", raising=False)

        with pytest.raises(ValueError, match="ECOMAIL_API_KEY is not set"):
            load_config(env_file)


# ── load_template ────────────────────────────────────────────────────


class TestLoadTemplate:
    def test_success(self, tmp_path):
        html_file = tmp_path / "template.html"
        html_file.write_text("<html>Test</html>", encoding="utf-8")

        result = load_template(html_file)

        assert result == "<html>Test</html>"

    def test_missing_file_raises(self, tmp_path):
        missing = tmp_path / "missing.html"

        with pytest.raises(FileNotFoundError, match="HTML template not found"):
            load_template(missing)


# ── build_payload ────────────────────────────────────────────────────


class TestBuildPayload:
    def test_structure(self, sample_html, sample_recipient):
        payload = build_payload(sample_html, sample_recipient)

        assert "message" in payload
        msg = payload["message"]
        assert "subject" in msg
        assert "from_name" in msg
        assert "from_email" in msg
        assert "to" in msg
        assert "html" in msg
        assert "text" in msg
        assert "options" in msg

    def test_html_content_included(self, sample_html, sample_recipient):
        payload = build_payload(sample_html, sample_recipient)

        assert payload["message"]["html"] == sample_html

    def test_tracking_options_enabled(self, sample_html, sample_recipient):
        payload = build_payload(sample_html, sample_recipient)
        options = payload["message"]["options"]

        assert options["click_tracking"] is True
        assert options["open_tracking"] is True

    def test_recipient(self, sample_html, sample_recipient):
        payload = build_payload(sample_html, sample_recipient)
        recipients = payload["message"]["to"]

        assert len(recipients) == 1
        assert recipients[0]["email"] == sample_recipient["email"]
        assert recipients[0]["name"] == sample_recipient["name"]


# ── send_alert ───────────────────────────────────────────────────────


class TestSendAlert:
    @patch("send_maisignal_alert.requests.post")
    def test_success(self, mock_post, sample_payload, sample_api_key):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.ok = True
        mock_post.return_value = mock_response

        response = send_alert(sample_payload, sample_api_key)

        assert response.status_code == 200
        mock_post.assert_called_once()

    @patch("send_maisignal_alert.requests.post")
    def test_api_error(self, mock_post, sample_payload, sample_api_key):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 401
        mock_response.ok = False
        mock_post.return_value = mock_response

        response = send_alert(sample_payload, sample_api_key)

        assert response.status_code == 401
        assert not response.ok

    @patch("send_maisignal_alert.requests.post")
    def test_network_error(self, mock_post, sample_payload, sample_api_key):
        mock_post.side_effect = requests.ConnectionError("Connection refused")

        with pytest.raises(requests.ConnectionError):
            send_alert(sample_payload, sample_api_key)

    @patch("send_maisignal_alert.requests.post")
    def test_headers(self, mock_post, sample_payload, sample_api_key):
        mock_post.return_value = MagicMock(spec=requests.Response)

        send_alert(sample_payload, sample_api_key)

        call_kwargs = mock_post.call_args
        headers = call_kwargs.kwargs["headers"]
        assert headers["Content-Type"] == "application/json"
        assert headers["key"] == sample_api_key

    @patch("send_maisignal_alert.requests.post")
    def test_timeout(self, mock_post, sample_payload, sample_api_key):
        mock_post.return_value = MagicMock(spec=requests.Response)

        send_alert(sample_payload, sample_api_key)

        call_kwargs = mock_post.call_args
        assert call_kwargs.kwargs["timeout"] == 30


# ── main ─────────────────────────────────────────────────────────────


# ── load_snowflake_config ────────────────────────────────────────────


class TestLoadSnowflakeConfig:
    def test_success(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text(
            "SNOWFLAKE_ACCOUNT=acct\n"
            "SNOWFLAKE_USER=usr\n"
            "SNOWFLAKE_PASSWORD=pwd\n"
            "SNOWFLAKE_ROLE=role\n"
            "SNOWFLAKE_WAREHOUSE=wh\n"
        )
        monkeypatch.delenv("SNOWFLAKE_ACCOUNT", raising=False)
        monkeypatch.delenv("SNOWFLAKE_USER", raising=False)
        monkeypatch.delenv("SNOWFLAKE_PASSWORD", raising=False)
        monkeypatch.delenv("SNOWFLAKE_ROLE", raising=False)
        monkeypatch.delenv("SNOWFLAKE_WAREHOUSE", raising=False)

        result = load_snowflake_config(env_file)

        assert result["account"] == "acct"
        assert result["user"] == "usr"
        assert result["password"] == "pwd"  # pragma: allowlist secret
        assert result["role"] == "role"
        assert result["warehouse"] == "wh"

    def test_missing_vars_raises(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("")
        monkeypatch.delenv("SNOWFLAKE_ACCOUNT", raising=False)
        monkeypatch.delenv("SNOWFLAKE_USER", raising=False)
        monkeypatch.delenv("SNOWFLAKE_PASSWORD", raising=False)
        monkeypatch.delenv("SNOWFLAKE_ROLE", raising=False)
        monkeypatch.delenv("SNOWFLAKE_WAREHOUSE", raising=False)

        with pytest.raises(ValueError, match="Missing Snowflake env vars"):
            load_snowflake_config(env_file)


# ── fetch_recipients ─────────────────────────────────────────────────


class TestFetchRecipients:
    @patch("send_maisignal_alert.snowflake.connector.connect")
    def test_success(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("a@example.com", "Company A"),
            ("b@example.com", "Company B"),
        ]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = fetch_recipients({"account": "acct"})

        assert len(result) == 2
        assert result[0] == {"email": "a@example.com", "name": "Company A"}
        assert result[1] == {"email": "b@example.com", "name": "Company B"}
        mock_conn.close.assert_called_once()

    @patch("send_maisignal_alert.snowflake.connector.connect")
    def test_empty_result_raises(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        with pytest.raises(RuntimeError, match="No recipients found"):
            fetch_recipients({"account": "acct"})

        mock_conn.close.assert_called_once()


# ── main ─────────────────────────────────────────────────────────────


class TestMain:
    @patch("send_maisignal_alert.send_alert")
    @patch("send_maisignal_alert.fetch_recipients")
    @patch("send_maisignal_alert.load_snowflake_config")
    @patch("send_maisignal_alert.load_template")
    @patch("send_maisignal_alert.load_config")
    def test_success(
        self, mock_config, mock_template, mock_sf, mock_fetch, mock_send
    ):
        mock_config.return_value = "test-key"
        mock_template.return_value = "<html>ok</html>"
        mock_sf.return_value = {"account": "acct"}
        mock_fetch.return_value = [
            {"email": "a@example.com", "name": "Company A"},
        ]
        mock_response = MagicMock(spec=requests.Response)
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_send.return_value = mock_response

        main()

        mock_config.assert_called_once()
        mock_template.assert_called_once()
        mock_sf.assert_called_once()
        mock_fetch.assert_called_once()
        mock_send.assert_called_once()

    @patch("send_maisignal_alert.load_config")
    def test_config_error_exits(self, mock_config):
        mock_config.side_effect = ValueError("ECOMAIL_API_KEY is not set.")

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("send_maisignal_alert.load_template")
    @patch("send_maisignal_alert.load_config")
    def test_template_error_exits(self, mock_config, mock_template):
        mock_config.return_value = "test-key"
        mock_template.side_effect = FileNotFoundError("HTML template not found")

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("send_maisignal_alert.load_snowflake_config")
    @patch("send_maisignal_alert.load_template")
    @patch("send_maisignal_alert.load_config")
    def test_snowflake_config_error_exits(
        self, mock_config, mock_template, mock_sf
    ):
        mock_config.return_value = "test-key"
        mock_template.return_value = "<html>ok</html>"
        mock_sf.side_effect = ValueError("Missing Snowflake env vars")

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("send_maisignal_alert.fetch_recipients")
    @patch("send_maisignal_alert.load_snowflake_config")
    @patch("send_maisignal_alert.load_template")
    @patch("send_maisignal_alert.load_config")
    def test_no_recipients_exits(
        self, mock_config, mock_template, mock_sf, mock_fetch
    ):
        mock_config.return_value = "test-key"
        mock_template.return_value = "<html>ok</html>"
        mock_sf.return_value = {"account": "acct"}
        mock_fetch.side_effect = RuntimeError("No recipients found")

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("send_maisignal_alert.send_alert")
    @patch("send_maisignal_alert.fetch_recipients")
    @patch("send_maisignal_alert.load_snowflake_config")
    @patch("send_maisignal_alert.load_template")
    @patch("send_maisignal_alert.load_config")
    def test_api_error_exits(
        self, mock_config, mock_template, mock_sf, mock_fetch, mock_send
    ):
        mock_config.return_value = "test-key"
        mock_template.return_value = "<html>ok</html>"
        mock_sf.return_value = {"account": "acct"}
        mock_fetch.return_value = [
            {"email": "a@example.com", "name": "Company A"},
        ]
        mock_response = MagicMock(spec=requests.Response)
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_send.return_value = mock_response

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("send_maisignal_alert.send_alert")
    @patch("send_maisignal_alert.fetch_recipients")
    @patch("send_maisignal_alert.load_snowflake_config")
    @patch("send_maisignal_alert.load_template")
    @patch("send_maisignal_alert.load_config")
    def test_network_error_exits(
        self, mock_config, mock_template, mock_sf, mock_fetch, mock_send
    ):
        mock_config.return_value = "test-key"
        mock_template.return_value = "<html>ok</html>"
        mock_sf.return_value = {"account": "acct"}
        mock_fetch.return_value = [
            {"email": "a@example.com", "name": "Company A"},
        ]
        mock_send.side_effect = requests.ConnectionError("timeout")

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("send_maisignal_alert.send_alert")
    @patch("send_maisignal_alert.fetch_recipients")
    @patch("send_maisignal_alert.load_snowflake_config")
    @patch("send_maisignal_alert.load_template")
    @patch("send_maisignal_alert.load_config")
    def test_multiple_recipients(
        self, mock_config, mock_template, mock_sf, mock_fetch, mock_send
    ):
        mock_config.return_value = "test-key"
        mock_template.return_value = "<html>ok</html>"
        mock_sf.return_value = {"account": "acct"}
        mock_fetch.return_value = [
            {"email": "a@example.com", "name": "Company A"},
            {"email": "b@example.com", "name": "Company B"},
        ]
        mock_response = MagicMock(spec=requests.Response)
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_send.return_value = mock_response

        main()

        assert mock_send.call_count == 2
