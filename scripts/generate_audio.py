#!/usr/bin/env python3
"""Generate spoken versions of Ghesedoon stories with edge-tts."""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "content" / "posts"
AUDIO = ROOT / "static" / "audio"

VOICES = {
    "fa": "fa-IR-DilaraNeural",
    "en": "en-US-AriaNeural",
}

FRONT_MATTER_RE = re.compile(r"^(\+\+\+|---)\n.*?\n\1\n?", re.S)
IMAGE_RE = re.compile(r"!\[.*?\]\([^)]+\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
TITLE_RE = re.compile(r"^title\s*=\s*(?:'((?:\\'|[^'])*)'|\"((?:\\\"|[^\"])*)\")\s*$", re.M)


def story_id(path: Path) -> str:
    name = path.name
    if name.endswith(".en.md"):
        return name[: -len(".en.md")]
    return path.stem


def story_lang(path: Path) -> str:
    return "en" if path.name.endswith(".en.md") else "fa"


def parse_title(text: str) -> str:
    match = TITLE_RE.search(text)
    if not match:
        return ""
    return (match.group(1) or match.group(2) or "").replace("\\'", "'").replace('\\"', '"')


def clean_story_text(raw: str, title: str = "") -> str:
    body = FRONT_MATTER_RE.sub("", raw, count=1)
    body = IMAGE_RE.sub("", body)
    body = LINK_RE.sub(r"\1", body)
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    if title:
        return f"{title}.\n\n{body}" if body else f"{title}."
    return body


def iter_story_files(lang: str | None = None) -> list[Path]:
    files = []
    for path in sorted(POSTS.glob("*.md")):
        if path.name.startswith("_"):
            continue
        if lang and story_lang(path) != lang:
            continue
        files.append(path)
    return files


async def synthesize(text: str, voice: str, dest: Path, rate: str) -> None:
    import edge_tts

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".tmp.mp3")
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(tmp))
    tmp.replace(dest)


async def generate_one(path: Path, force: bool, rate: str) -> str:
    lang = story_lang(path)
    sid = story_id(path)
    dest = AUDIO / lang / f"{sid}.mp3"
    if dest.exists() and dest.stat().st_size > 0 and not force:
        return "skip"

    raw = path.read_text(encoding="utf-8")
    text = clean_story_text(raw, parse_title(raw))
    if len(text) < 40:
        return "empty"

    last_error = None
    for attempt in range(4):
        try:
            await synthesize(text, VOICES[lang], dest, rate)
            return "ok"
        except Exception as exc:  # noqa: BLE001 — TTS network errors vary
            last_error = exc
            await asyncio.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{path.name}: {last_error}") from last_error


async def generate_all(paths: list[Path], force: bool, rate: str, pause: float) -> None:
    ok = skip = empty = 0
    for index, path in enumerate(paths, start=1):
        status = await generate_one(path, force=force, rate=rate)
        if status == "ok":
            ok += 1
            print(f"[{index}/{len(paths)}] {story_lang(path)}/{story_id(path)}.mp3", flush=True)
            if pause:
                await asyncio.sleep(pause)
        elif status == "skip":
            skip += 1
        else:
            empty += 1
            print(f"[{index}/{len(paths)}] empty {path.name}", flush=True)
    print(f"done ok={ok} skip={skip} empty={empty}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", choices=("fa", "en"), help="Only this language")
    parser.add_argument("--only", help="Comma-separated story ids, e.g. 3,100,165")
    parser.add_argument("--force", action="store_true", help="Rebuild existing files")
    parser.add_argument("--rate", default="-5%", help="edge-tts speaking rate")
    parser.add_argument("--pause", type=float, default=0.8, help="Seconds between requests")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = iter_story_files(args.lang)
    if args.only:
        wanted = {item.strip() for item in args.only.split(",") if item.strip()}
        paths = [path for path in paths if story_id(path) in wanted]
        missing = wanted - {story_id(path) for path in paths}
        if missing:
            print("unknown ids:", ", ".join(sorted(missing)), file=sys.stderr)
            return 2
    if not paths:
        print("no stories matched", file=sys.stderr)
        return 2
    asyncio.run(generate_all(paths, force=args.force, rate=args.rate, pause=args.pause))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
