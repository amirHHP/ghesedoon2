#!/usr/bin/env python3
"""One-off Fish Audio sample via Vercel AI Gateway. Do not commit secrets."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_audio import clean_story_text, parse_title  # noqa: E402

GATEWAY = "https://ai-gateway.vercel.sh/v4/ai/speech-model"
VOICE = "933563129e564b19a115bedd57b7406a"
STORY = ROOT / "content" / "posts" / "3.md"
OUT_DIR = ROOT / "static" / "fish-test"


def load_key() -> str:
    env_path = ROOT / ".env.local"
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("AI_GATEWAY_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("AI_GATEWAY_API_KEY missing from .env.local")


def story_text() -> str:
    raw = STORY.read_text(encoding="utf-8")
    return clean_story_text(raw, parse_title(raw))


def synthesize(model: str, text: str, dest: Path) -> None:
    payload = {
        "text": text,
        "voice": VOICE,
        "outputFormat": "mp3",
        "language": "fa",
        "instructions": (
            "Read as a warm Persian storyteller for young children. "
            "Natural pacing, gentle emotion, clear Farsi pronunciation."
        ),
    }
    req = urllib.request.Request(
        GATEWAY,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {load_key()}",
            "ai-model-id": model,
            "ai-gateway-protocol-version": "0.0.1",
            "ai-speech-model-specification-version": "4",
            "ai-gateway-auth-method": "api-key",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")[:2000]
        raise SystemExit(f"{model} HTTP {err.code}: {detail}") from err

    audio_b64 = body.get("audio")
    if not audio_b64:
        keys = sorted(body.keys())
        warnings = body.get("warnings")
        raise SystemExit(f"{model} no audio in response keys={keys} warnings={warnings}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(__import__("base64").b64decode(audio_b64))
    warnings = body.get("warnings") or []
    print(f"ok {model} bytes={dest.stat().st_size} warnings={warnings} -> {dest.name}")


def main() -> None:
    text = story_text()
    print(f"story chars={len(text)}")
    models = [
        ("fish-audio/s2-pro-free", "3.s2-pro.mp3"),
        ("fish-audio/s2.1-pro-free", "3.s2.1-pro.mp3"),
    ]
    failed = 0
    for model, filename in models:
        try:
            synthesize(model, text, OUT_DIR / filename)
        except SystemExit as err:
            failed += 1
            print(err, file=sys.stderr)
    if failed:
        raise SystemExit(failed)


if __name__ == "__main__":
    main()
