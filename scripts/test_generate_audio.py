#!/usr/bin/env python3
"""Tests for story text cleanup used by generate_audio.py."""

import unittest

from generate_audio import clean_story_text, parse_title, story_id, story_lang
from pathlib import Path


class CleanStoryTextTests(unittest.TestCase):
    def test_strips_front_matter_image_and_keeps_title(self) -> None:
        raw = """+++
title = 'پرواز آرزومند'
draft = false
+++
![bird](/3.bird.jpg)

روزی روزگاری پرنده‌ای بود.

پایان.
"""
        text = clean_story_text(raw, parse_title(raw))
        self.assertTrue(text.startswith("پرواز آرزومند."))
        self.assertIn("روزی روزگاری پرنده‌ای بود.", text)
        self.assertNotIn("+++", text)
        self.assertNotIn("/3.bird.jpg", text)
        self.assertIn("پایان.", text)

    def test_keeps_link_label(self) -> None:
        raw = "+++\ntitle = 'A'\n+++\nSee [the sea](/donate/).\n"
        self.assertEqual(clean_story_text(raw, "A"), "A.\n\nSee the sea.")

    def test_escaped_title_apostrophe(self) -> None:
        raw = "+++\ntitle = 'A child\\'s friend'\n+++\nHello.\n"
        self.assertEqual(parse_title(raw), "A child's friend")


class StoryPathTests(unittest.TestCase):
    def test_ids_and_langs(self) -> None:
        self.assertEqual(story_id(Path("3.md")), "3")
        self.assertEqual(story_id(Path("3.en.md")), "3")
        self.assertEqual(story_id(Path("adventureous-cat.en.md")), "adventureous-cat")
        self.assertEqual(story_lang(Path("3.md")), "fa")
        self.assertEqual(story_lang(Path("3.en.md")), "en")


if __name__ == "__main__":
    unittest.main()
