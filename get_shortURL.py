"""Simple CLI utility to shorten URLs via Weibo short URL API.

Usage:
    python get_shortURL.py --url https://example.com
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import requests

API_ENDPOINT = "https://api.weibo.com/2/short_url/shorten.json"
DEFAULT_SOURCE = "2849184197"


def shorten_url(long_url: str, source: str = DEFAULT_SOURCE, timeout: int = 10) -> str:
    """Call Weibo API and return a short URL string.

    Raises:
        RuntimeError: if API request fails or response format is unexpected.
    """
    response = requests.get(
        API_ENDPOINT,
        params={"source": source, "url_long": long_url},
        timeout=timeout,
    )

    if response.status_code != 200:
        raise RuntimeError(f"API request failed: {response.status_code} {response.text}")

    data: dict[str, Any] = response.json()
    urls = data.get("urls")
    if not urls or not isinstance(urls, list):
        raise RuntimeError(f"Unexpected API response: {data}")

    short_url = urls[0].get("url_short")
    if not short_url:
        raise RuntimeError(f"Short URL missing in response: {data}")

    return short_url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Shorten long URL by using Weibo API")
    parser.add_argument("--url", required=True, help="The long URL to shorten")
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        help="Weibo application source key (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        print(shorten_url(args.url, args.source))
        return 0
    except requests.RequestException as exc:
        print(f"Network error: {exc}", file=sys.stderr)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
