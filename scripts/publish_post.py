#!/usr/bin/env python3
"""Publish or draft a WordPress.com post via REST API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


API_BASE = "https://public-api.wordpress.com/rest/v1.1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a post on WordPress.com via REST API."
    )
    parser.add_argument("--site", required=True, help="Site domain or numeric site ID.")
    parser.add_argument("--title", required=True, help="Post title.")
    parser.add_argument("--content", required=True, help="Post content (HTML or plain text).")
    parser.add_argument(
        "--status",
        default="publish",
        choices=["publish", "draft", "pending", "private", "future"],
        help="Post status. Defaults to publish.",
    )
    parser.add_argument("--excerpt", default="", help="Optional post excerpt.")
    parser.add_argument("--slug", default="", help="Optional URL slug.")
    parser.add_argument(
        "--categories",
        default="",
        help="Comma-separated categories (e.g. Blog,News).",
    )
    parser.add_argument(
        "--tags",
        default="",
        help="Comma-separated tags (e.g. ai,wordpress).",
    )
    parser.add_argument(
        "--access-token",
        default=os.environ.get("WPCOM_ACCESS_TOKEN", ""),
        help="OAuth bearer token. Defaults to WPCOM_ACCESS_TOKEN env var.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print endpoint and payload without sending the request.",
    )
    return parser.parse_args()


def normalize_csv(value: str) -> str:
    parts = [v.strip() for v in value.split(",") if v.strip()]
    return ",".join(parts)


def main() -> int:
    args = parse_args()

    endpoint = f"{API_BASE}/sites/{urllib.parse.quote(args.site, safe='')}/posts/new"
    payload = {
        "title": args.title,
        "content": args.content,
        "status": args.status,
    }
    if args.excerpt:
        payload["excerpt"] = args.excerpt
    if args.slug:
        payload["slug"] = args.slug
    categories = normalize_csv(args.categories)
    if categories:
        payload["categories"] = categories
    tags = normalize_csv(args.tags)
    if tags:
        payload["tags"] = tags

    if args.dry_run:
        print(json.dumps({"endpoint": endpoint, "payload": payload}, indent=2))
        return 0

    if not args.access_token:
        print(
            "error: missing access token. Pass --access-token or set WPCOM_ACCESS_TOKEN.",
            file=sys.stderr,
        )
        return 2

    body = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Authorization": f"Bearer {args.access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
            print(json.dumps(data, indent=2))
            return 0
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        print(f"HTTP {err.code}: {detail}", file=sys.stderr)
        return 1
    except urllib.error.URLError as err:
        print(f"network error: {err}", file=sys.stderr)
        return 1
    except json.JSONDecodeError:
        print("error: received non-JSON response from API.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
