#!/usr/bin/env python3
"""Verify image coverage for a card set in data/cards.json.

Default usage checks the Hercules set and prints missing file paths in the
expected repository filename format (assets/cache/<id>.jpg).
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_set(cards_path: Path, set_key: str) -> list[dict[str, Any]]:
    data = json.loads(cards_path.read_text(encoding="utf-8"))
    if set_key not in data:
        available = ", ".join(sorted(k for k, v in data.items() if isinstance(v, list)))
        raise KeyError(f"set key '{set_key}' not found. Available list keys: {available}")

    set_cards = data[set_key]
    if not isinstance(set_cards, list):
        raise TypeError(f"set key '{set_key}' is not a list")

    return [c for c in set_cards if isinstance(c, dict) and c.get("card_id")]


def existing_image_stems(*dirs: Path) -> set[str]:
    stems: set[str] = set()
    for base in dirs:
        if not base.exists():
            continue
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
            stems.update(path.stem for path in base.glob(ext))
    return stems


def resolved_image_id(card: dict[str, Any]) -> str:
    # Priority: explicit pic_id, then full_link redirect, else card_id.
    return str(card.get("pic_id") or card.get("full_link") or card["card_id"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify card image coverage for a set")
    parser.add_argument("--set", dest="set_key", default="hercules", help="Top-level cards.json key to audit")
    parser.add_argument("--cards", dest="cards_path", default="data/cards.json", help="Path to cards.json")
    parser.add_argument("--cache-dir", dest="cache_dir", default="assets/cache", help="Primary image directory")
    parser.add_argument("--pics-dir", dest="pics_dir", default="assets/pics", help="Secondary image directory")
    parser.add_argument(
        "--write-missing-paths",
        dest="write_missing_paths",
        default="",
        help="Optional output file path for missing real-card image paths",
    )
    parser.add_argument(
        "--write-csv",
        dest="write_csv",
        default="",
        help="Optional output CSV path with columns: card_id,resolved_image_id,status",
    )
    args = parser.parse_args()

    cards_path = Path(args.cards_path)
    cache_dir = Path(args.cache_dir)
    pics_dir = Path(args.pics_dir)

    cards = load_set(cards_path, args.set_key)
    existing = existing_image_stems(cache_dir, pics_dir)

    real_cards: list[dict[str, Any]] = []
    linked_cards: list[dict[str, Any]] = []
    missing_resolved: list[str] = []
    missing_real_card_files: list[str] = []

    for card in cards:
        if "full_link" in card:
            linked_cards.append(card)
        else:
            real_cards.append(card)

        image_id = resolved_image_id(card)
        if image_id not in existing:
            missing_resolved.append(str(card["card_id"]))

        # Repo convention for standalone card art uses card_id.jpg in cache.
        if "full_link" not in card and str(card["card_id"]) not in existing:
            missing_real_card_files.append(str(card["card_id"]))

    print(f"set_key={args.set_key}")
    print(f"entries={len(cards)}")
    print(f"real_cards={len(real_cards)}")
    print(f"full_link_cards={len(linked_cards)}")
    print(f"missing_resolved_images={len(missing_resolved)}")

    if missing_resolved:
        print("missing_resolved_card_ids=" + ",".join(missing_resolved))
    else:
        print("missing_resolved_card_ids=-")

    print(f"missing_real_card_files={len(missing_real_card_files)}")
    if missing_real_card_files:
        print("missing_real_paths:")
        for card_id in missing_real_card_files:
            print(f"assets/cache/{card_id}.jpg")
    else:
        print("missing_real_paths:-")

    if args.write_missing_paths:
        output_path = Path(args.write_missing_paths)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = "\n".join(f"assets/cache/{card_id}.jpg" for card_id in missing_real_card_files)
        if payload:
            payload += "\n"
        output_path.write_text(payload, encoding="utf-8")
        print(f"wrote_missing_paths_file={output_path.as_posix()}")

    if args.write_csv:
        csv_path = Path(args.write_csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(["card_id", "resolved_image_id", "status"])
            for card in cards:
                card_id = str(card["card_id"])
                image_id = resolved_image_id(card)
                status = "OK" if image_id in existing else "MISSING"
                writer.writerow([card_id, image_id, status])
        print(f"wrote_csv_file={csv_path.as_posix()}")

    if linked_cards:
        print("full_link_map:")
        for card in linked_cards:
            card_id = str(card["card_id"])
            full_link = str(card.get("full_link"))
            state = "OK" if full_link in existing else "MISSING_TARGET_IMAGE"
            print(f"{card_id} -> {full_link} [{state}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
