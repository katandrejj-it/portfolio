import asyncio
import json
import re
import socket
import os
import base64
import binascii
import logging
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SOURCE_URL = "https://raw.githubusercontent.com/SoliSpirit/mtproto/master/all_proxies.txt"

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "proxies.json"

PROXY_PATTERN = re.compile(r"https://t\.me/proxy\?[^\s,'\"]+")


def extract_proxies(text):
    proxies = []
    for match in PROXY_PATTERN.findall(text):
        raw_url = match.strip().rstrip('.,;')
        parsed = urlparse(raw_url)
        if parsed.scheme != "https" or parsed.netloc not in ("t.me", "telegram.me"):
            continue
        params = parse_qs(parsed.query)
        server = params.get("server", [None])[0]
        if server:
            server = server.rstrip('.')
        port = params.get("port", [None])[0]
        secret = params.get("secret", [None])[0]
        if not secret:
            continue
        try:
            if len(secret) in (32, 34, 64) and all(c in '0123456789abcdefABCDEF' for c in secret):
                bytes.fromhex(secret)
            else:
                base64.b64decode(secret, validate=True)
        except (ValueError, binascii.Error):
            continue

        try:
            port = int(port)
        except ValueError:
            continue
        if not (0 < port <= 65535):
            continue

        proxies.append({
            "url": raw_url,
            "server": server,
            "port": port,
            "secret": secret,
            "ping": None,
        })
    # deduplicate by full link
    unique = {}
    for p in proxies:
        unique[p["url"]] = p
    return list(unique.values())


async def fetch_source():
    async with aiohttp.ClientSession() as session:
        async with session.get(SOURCE_URL, timeout=30, ssl=False) as res:
            res.raise_for_status()
            return await res.text()


async def probe_proxy(server: str, port: int, secret: str, timeout_sec: float = 5.0):
    start = asyncio.get_event_loop().time()
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(server, port), timeout_sec)
        # MTProxy handshake
        if len(secret) in (32, 34, 64) and all(c in '0123456789abcdefABCDEF' for c in secret):
            secret_bytes = bytes.fromhex(secret)
        else:
            secret_bytes = base64.b64decode(secret, validate=True)
        handshake = b'\xef' + os.urandom(4) + secret_bytes
        writer.write(handshake)
        data = await asyncio.wait_for(reader.readexactly(1), timeout=5.0)
        if data == b'\xef':
            ping_ms = int((asyncio.get_event_loop().time() - start) * 1000)
            writer.close()
            await writer.wait_closed()
            return True, ping_ms
        else:
            writer.close()
            await writer.wait_closed()
            logger.warning(f"Proxy {server}:{port} failed handshake: wrong response {data}")
            return False, None
    except asyncio.TimeoutError:
        logger.warning(f"Proxy {server}:{port} failed: timeout")
        return False, None
    except OSError as e:
        logger.warning(f"Proxy {server}:{port} failed: OS error {e}")
        return False, None
    except socket.gaierror as e:
        logger.warning(f"Proxy {server}:{port} failed: DNS resolution error {e}")
        return False, None
    except asyncio.IncompleteReadError:
        logger.warning(f"Proxy {server}:{port} failed: incomplete read")
        return False, None


async def check_proxies(proxies):
    sem = asyncio.Semaphore(100)

    async def check_item(item):
        async with sem:
            ok, ping = await probe_proxy(item["server"], item["port"], item["secret"])
            if ok:
                item["ping"] = ping
                return item
            return None

    results = await asyncio.gather(*(check_item(p) for p in proxies))
    return [r for r in results if r is not None]


def save_results(working):
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(sorted(working, key=lambda x: x["ping"]), f, ensure_ascii=False, indent=2)


async def main():
    logger.info("Fetching proxy list from %s", SOURCE_URL)
    data = await fetch_source()
    proxies = extract_proxies(data)
    logger.info(f"Parsed {len(proxies)} proxy URLs")
    if not proxies:
        logger.warning("No proxies found; abort")
        return

    good = await check_proxies(proxies)
    logger.info(f"Working proxies: {len(good)}")

    save_results(good)
    logger.info("Saved %s", OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.run(main())
