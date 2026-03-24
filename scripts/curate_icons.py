#!/usr/bin/env python3
"""Curate icon sets from Lucide and Octicons into the bundled icons directory.

This is a developer tool — not shipped with the package. Run it to update
the bundled icon set:

    python scripts/curate_icons.py

It clones the repos to a temp dir, copies selected SVGs, and generates manifest.json.
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ICONS_DIR = Path(__file__).parent.parent / "src" / "reifire" / "visualization" / "providers" / "icons"

# Lucide icons to include — broad general-purpose coverage
# https://lucide.dev/icons
LUCIDE_ICONS = [
    # Objects / things
    "package", "box", "archive", "gift", "cube",
    "file", "file-text", "file-code", "file-image", "file-video",
    "folder", "folder-open",
    "image", "camera", "video", "music", "mic",
    "book", "book-open", "notebook", "bookmark",
    "pen", "pencil", "brush", "palette", "paintbrush",
    "scissors", "paperclip", "pin",
    "key", "lock", "unlock", "shield", "shield-check",
    "heart", "star", "flag", "trophy", "award", "medal",
    "clock", "timer", "calendar", "alarm-clock",
    "map", "map-pin", "compass", "navigation", "globe",
    "home", "building", "building-2", "store", "warehouse",
    "car", "truck", "plane", "train", "bike", "ship", "rocket",
    "lamp", "lightbulb", "flashlight", "sun", "moon", "cloud",
    "umbrella", "thermometer", "flame", "droplet", "snowflake", "wind", "zap",
    "tree", "flower", "leaf", "sprout",
    "bug", "fish", "bird", "cat", "dog", "paw-print",
    "baby", "user", "users", "person-standing",
    "shirt", "glasses", "crown",
    "phone", "smartphone", "tablet", "laptop", "monitor", "tv",
    "printer", "scanner",
    "speaker", "headphones",
    "battery", "plug", "power",
    "wrench", "hammer", "screwdriver",
    "shopping-cart", "shopping-bag", "credit-card", "wallet", "receipt", "coins",
    "pill", "syringe", "stethoscope", "bandage",
    "dumbbell", "football", "tennis-ball",
    "utensils", "coffee", "wine", "beer", "pizza", "apple", "egg", "cake",
    "bed", "bath", "armchair", "sofa", "door",
    # Tech / data
    "database", "server", "hard-drive", "cpu", "memory-stick", "usb",
    "wifi", "bluetooth", "radio", "antenna", "satellite",
    "code", "terminal", "braces", "hash", "binary", "variable",
    "git-branch", "git-commit", "git-merge", "git-pull-request",
    "globe", "link", "unlink", "external-link",
    "download", "upload", "cloud-download", "cloud-upload",
    "search", "filter", "sort-asc", "sort-desc",
    "settings", "sliders", "toggle-left", "toggle-right",
    "maximize", "minimize", "expand", "shrink",
    # UI / layout
    "layout", "layout-grid", "layout-list", "layout-dashboard",
    "panel-left", "panel-right", "panel-top", "panel-bottom",
    "sidebar", "menu", "grip-vertical", "grip-horizontal",
    "table", "kanban", "calendar-days",
    "tabs",
    # Actions
    "play", "pause", "stop", "skip-forward", "skip-back",
    "rewind", "fast-forward", "repeat", "shuffle",
    "volume", "volume-1", "volume-2", "volume-x",
    "plus", "minus", "x", "check", "check-check",
    "arrow-up", "arrow-down", "arrow-left", "arrow-right",
    "chevron-up", "chevron-down", "chevron-left", "chevron-right",
    "rotate-cw", "rotate-ccw", "refresh-cw", "refresh-ccw",
    "undo", "redo",
    "copy", "clipboard", "paste",
    "trash", "trash-2", "eraser",
    "edit", "save", "send", "share", "share-2",
    "eye", "eye-off",
    "log-in", "log-out",
    "move", "grab",
    # Communication
    "mail", "inbox", "at-sign",
    "message-circle", "message-square", "messages-square",
    "bell", "bell-ring",
    "megaphone", "radio-tower",
    # Charts / data viz
    "bar-chart", "bar-chart-2", "bar-chart-3",
    "line-chart", "pie-chart", "area-chart",
    "trending-up", "trending-down", "activity",
    "gauge", "target",
    # Status / feedback
    "alert-circle", "alert-triangle", "info", "help-circle",
    "circle-check", "circle-x", "circle-dot",
    "loader", "hourglass",
    "thumbs-up", "thumbs-down",
    "smile", "frown", "meh",
    # Organization
    "tag", "tags", "label",
    "list", "list-ordered", "list-checks", "list-tree",
    "layers", "stack",
    "network", "workflow", "sitemap",
    "puzzle", "blocks",
    "milestone", "flag-triangle-right",
    # Security / auth
    "shield-alert", "shield-off",
    "fingerprint", "scan", "qr-code",
    "user-check", "user-plus", "user-minus", "user-x",
    # Math / science
    "calculator", "sigma", "infinity", "percent",
    "flask", "atom", "dna", "microscope", "telescope",
    "ruler", "protractor",
]

# Octicons to include — GitHub-flavored icons
# https://primer.style/foundations/icons
OCTICONS_ICONS = [
    "package-24", "repo-24", "code-24", "terminal-24",
    "git-branch-24", "git-commit-24", "git-merge-24", "git-pull-request-24",
    "issue-opened-24", "issue-closed-24", "comment-24", "comment-discussion-24",
    "database-24", "server-24", "cloud-24",
    "file-24", "file-code-24", "file-directory-24",
    "gear-24", "tools-24", "plug-24",
    "shield-24", "shield-lock-24", "shield-check-24", "key-24", "lock-24",
    "rocket-24", "zap-24", "flame-24",
    "graph-24", "pulse-24", "meter-24",
    "eye-24", "search-24", "filter-24",
    "bell-24", "inbox-24", "mail-24",
    "heart-24", "star-24", "bookmark-24",
    "person-24", "people-24", "organization-24",
    "tag-24", "milestone-24", "project-24",
    "check-24", "x-24", "plus-24", "dash-24",
    "alert-24", "info-24", "question-24", "stop-24",
    "arrow-up-24", "arrow-down-24", "arrow-left-24", "arrow-right-24",
    "link-24", "link-external-24", "download-24", "upload-24",
    "sync-24", "history-24", "clock-24",
    "pencil-24", "trash-24", "copy-24", "paste-24",
    "log-24", "note-24", "list-unordered-24", "list-ordered-24",
    "table-24", "rows-24", "columns-24",
    "image-24", "video-24", "browser-24",
    "desktop-download-24", "device-mobile-24",
    "cpu-24", "container-24",
    "home-24", "globe-24", "location-24",
    "megaphone-24", "broadcast-24",
    "workflow-24", "iterations-24",
    "beaker-24", "telescope-24",
    "trophy-24", "thumbsup-24", "thumbsdown-24",
    "sun-24", "moon-24",
    "hash-24", "number-24",
    "apps-24", "stack-24", "sidebar-expand-24",
    "paintbrush-24", "typography-24",
    "sign-out-24", "sign-in-24",
    "share-24", "share-android-24",
    "report-24", "verified-24", "unverified-24",
    "blocked-24", "skip-24",
    "strikethrough-24", "bold-24", "italic-24", "code-review-24",
    "diff-24", "diff-added-24", "diff-removed-24", "diff-modified-24",
    "tasklist-24", "checklist-24",
    "dependabot-24", "hubot-24",
    "north-star-24", "sparkle-fill-24",
    "cache-24", "codescan-24",
    "accessibility-24", "screen-full-24",
]


def clone_and_copy_lucide(tmp_dir: Path) -> dict:
    """Clone Lucide repo and copy selected icons."""
    print("Cloning Lucide icons...")
    lucide_dir = tmp_dir / "lucide"
    subprocess.run(
        ["git", "clone", "--depth", "1", "https://github.com/lucide-icons/lucide.git", str(lucide_dir)],
        check=True,
        capture_output=True,
    )

    # Load Lucide metadata for tags
    icons_src = lucide_dir / "icons"
    lucide_out = ICONS_DIR / "lucide"
    manifest_entries = {}
    copied = 0
    missing = []

    for icon_name in LUCIDE_ICONS:
        svg_path = icons_src / icon_name / f"{icon_name}.svg"
        if not svg_path.exists():
            # Try without the directory nesting (older Lucide structure)
            svg_path = icons_src / f"{icon_name}.svg"
        if not svg_path.exists():
            missing.append(icon_name)
            continue

        # Copy SVG
        dest = lucide_out / f"{icon_name}.svg"
        shutil.copy2(svg_path, dest)
        copied += 1

        # Load tags from info.json if it exists
        info_path = icons_src / icon_name / "info.json"
        tags = [icon_name]
        tags.extend(icon_name.split("-"))
        if info_path.exists():
            try:
                info = json.loads(info_path.read_text())
                tags.extend(info.get("tags", []))
                tags.extend(info.get("aliases", []))
            except (json.JSONDecodeError, KeyError):
                pass

        # Deduplicate tags
        tags = list(dict.fromkeys(t.lower() for t in tags if t))

        manifest_entries[f"lucide/{icon_name}"] = {
            "name": icon_name,
            "set": "lucide",
            "tags": tags,
            "file": f"lucide/{icon_name}.svg",
        }

    print(f"  Copied {copied} Lucide icons")
    if missing:
        print(f"  Missing: {', '.join(missing)}")

    return manifest_entries


def clone_and_copy_octicons(tmp_dir: Path) -> dict:
    """Clone Octicons repo and copy selected icons."""
    print("Cloning Octicons...")
    octicons_dir = tmp_dir / "octicons"
    subprocess.run(
        ["git", "clone", "--depth", "1", "https://github.com/primer/octicons.git", str(octicons_dir)],
        check=True,
        capture_output=True,
    )

    icons_src = octicons_dir / "icons"
    octicons_out = ICONS_DIR / "octicons"
    manifest_entries = {}
    copied = 0
    missing = []

    for icon_name in OCTICONS_ICONS:
        svg_path = icons_src / f"{icon_name}.svg"
        if not svg_path.exists():
            missing.append(icon_name)
            continue

        # Copy SVG
        dest = octicons_out / f"{icon_name}.svg"
        shutil.copy2(svg_path, dest)
        copied += 1

        # Build tags from name (strip size suffix)
        base_name = icon_name.rsplit("-", 1)[0] if icon_name.endswith("-24") else icon_name
        tags = [base_name]
        tags.extend(base_name.split("-"))
        tags = list(dict.fromkeys(t.lower() for t in tags if t))

        manifest_entries[f"octicons/{icon_name}"] = {
            "name": base_name,
            "set": "octicons",
            "tags": tags,
            "file": f"octicons/{icon_name}.svg",
        }

    print(f"  Copied {copied} Octicons")
    if missing:
        print(f"  Missing: {', '.join(missing)}")

    return manifest_entries


def build_term_index(manifest_entries: dict) -> dict:
    """Build a reverse index from search terms to icon IDs."""
    term_index: dict[str, list[str]] = {}
    for icon_id, entry in manifest_entries.items():
        for tag in entry["tags"]:
            if tag not in term_index:
                term_index[tag] = []
            if icon_id not in term_index[tag]:
                term_index[tag].append(icon_id)
    return term_index


def main() -> None:
    """Run the curation pipeline."""
    # Clean existing icons
    for subdir in ["lucide", "octicons"]:
        target = ICONS_DIR / subdir
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)

    all_entries = {}

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        all_entries.update(clone_and_copy_lucide(tmp_path))
        all_entries.update(clone_and_copy_octicons(tmp_path))

    # Build term index
    term_index = build_term_index(all_entries)

    # Write manifest
    manifest = {
        "icons": all_entries,
        "term_index": term_index,
    }
    manifest_path = ICONS_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"\nManifest written to {manifest_path}")
    print(f"Total icons: {len(all_entries)}")
    print(f"Total search terms: {len(term_index)}")


if __name__ == "__main__":
    main()
