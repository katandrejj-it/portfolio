import asyncio
import pytest
import base64
import os
from unittest.mock import patch, AsyncMock
from main import extract_proxies, probe_proxy


class TestExtractProxies:
    def test_extract_valid_proxies(self):
        text = """
        Some text https://t.me/proxy?server=example.com&port=443&secret=dd1234567890abcdef1234567890abcdef
        Another https://t.me/proxy?server=test.org.&port=80&secret=YWJjZGVmZ2hpams=
        Invalid https://t.me/proxy?server=invalid.&port=abc&secret=invalid
        """
        proxies = extract_proxies(text)
        assert len(proxies) == 2
        assert proxies[0]['server'] == 'example.com'
        assert proxies[0]['port'] == 443
        assert proxies[1]['server'] == 'test.org'
        assert proxies[1]['port'] == 80

    def test_strip_trailing_dot(self):
        text = "https://t.me/proxy?server=domain.com.&port=443&secret=dd1234567890abcdef1234567890abcdef"
        proxies = extract_proxies(text)
        assert proxies[0]['server'] == 'domain.com'

    def test_invalid_secret(self):
        text = "https://t.me/proxy?server=example.com&port=443&secret=invalid"
        proxies = extract_proxies(text)
        assert len(proxies) == 0

    def test_invalid_port(self):
        text = "https://t.me/proxy?server=example.com&port=99999&secret=dd1234567890abcdef1234567890abcdef"
        proxies = extract_proxies(text)
        assert len(proxies) == 0


class TestProbeProxy:
    @pytest.mark.asyncio
    async def test_successful_handshake(self):
        with patch('asyncio.open_connection', new_callable=AsyncMock) as mock_conn:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_conn.return_value = (mock_reader, mock_writer)
            mock_reader.readexactly.return_value = b'\xef'

            success, ping = await probe_proxy('example.com', 443, 'dd1234567890abcdef1234567890abcdef')
            assert success is True
            assert ping is not None

    @pytest.mark.asyncio
    async def test_wrong_response(self):
        with patch('asyncio.open_connection', new_callable=AsyncMock) as mock_conn:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_conn.return_value = (mock_reader, mock_writer)
            mock_reader.readexactly.return_value = b'\x00'

            success, ping = await probe_proxy('example.com', 443, 'dd1234567890abcdef1234567890abcdef')
            assert success is False
            assert ping is None

    @pytest.mark.asyncio
    async def test_timeout(self):
        with patch('asyncio.open_connection', side_effect=asyncio.TimeoutError):
            success, ping = await probe_proxy('example.com', 443, 'dd1234567890abcdef1234567890abcdef')
            assert success is False
            assert ping is None