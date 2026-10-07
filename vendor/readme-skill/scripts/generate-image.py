#!/usr/bin/env python3
"""Generate an image through an OpenAI-compatible Images API."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1536x1024"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an image using an OpenAI-compatible Images API."
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("IMAGE_API_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or os.environ.get("OPENAI_API_URL"),
        help="Images generations endpoint or API base URL (or IMAGE_API_URL).",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("IMAGE_API_KEY") or os.environ.get("OPENAI_API_KEY"),
        help="API key (or IMAGE_API_KEY / OPENAI_API_KEY).",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("IMAGE_MODEL", DEFAULT_MODEL),
        help=f"Image model (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument("--prompt", required=True, help="Prompt for image generation.")
    parser.add_argument(
        "--size",
        default=os.environ.get("IMAGE_SIZE", DEFAULT_SIZE),
        help=f"Image size (default: {DEFAULT_SIZE}).",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path where the generated PNG/JPEG should be saved.",
    )
    parser.add_argument(
        "--timeout",
        default=300,
        type=int,
        help="HTTP timeout in seconds (default: 300).",
    )
    return parser.parse_args()


def generations_endpoint(value: str) -> str:
    endpoint = value.rstrip("/")
    if endpoint.endswith("/images/generations"):
        return endpoint
    if endpoint.endswith("/v1"):
        return f"{endpoint}/images/generations"
    return f"{endpoint}/v1/images/generations"


def error_message(exc: HTTPError) -> str:
    try:
        body = exc.read().decode("utf-8", errors="replace")
    except OSError:
        body = "<response body unavailable>"
    return f"Image API returned HTTP {exc.code}: {body[:1000]}"


def save_response(response: dict, output: Path, timeout: int) -> None:
    data = response.get("data")
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise ValueError("Image API response does not contain a valid data[0] object")

    image = data[0]
    output.parent.mkdir(parents=True, exist_ok=True)

    encoded = image.get("b64_json")
    if isinstance(encoded, str) and encoded:
        output.write_bytes(base64.b64decode(encoded, validate=True))
        return

    image_url = image.get("url")
    if isinstance(image_url, str) and image_url:
        request = Request(image_url, headers={"User-Agent": "readme-skill-image-generator"})
        with urlopen(request, timeout=timeout) as image_response:
            output.write_bytes(image_response.read())
        return

    raise ValueError("Image API response contains neither b64_json nor url")


def main() -> int:
    args = parse_args()
    if not args.endpoint:
        print("error: provide --endpoint or IMAGE_API_URL", file=sys.stderr)
        return 2
    if not args.api_key:
        print("error: provide --api-key or IMAGE_API_KEY", file=sys.stderr)
        return 2

    endpoint = generations_endpoint(args.endpoint)
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
    }
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {args.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "readme-skill-image-generator",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=args.timeout) as response:
            body = response.read()
        parsed = json.loads(body.decode("utf-8"))
        save_response(parsed, args.output, args.timeout)
    except HTTPError as exc:
        print(f"error: {error_message(exc)}", file=sys.stderr)
        return 1
    except (URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError, base64.binascii.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved generated image to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
