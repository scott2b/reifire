"""Quick demo of the new icon provider system."""

import webbrowser
import tempfile
from pathlib import Path
from reifire.visualization.providers import ProviderChain


TERMS = [
    "cat", "dog", "rocket", "database", "star", "heart",
    "coffee", "code", "music", "shield", "globe", "camera",
    "mail", "search", "clock", "lock", "book", "cloud",
    "fire", "bug", "leaf", "gift", "key", "bell",
]


def main() -> None:
    chain = ProviderChain()
    print(f"Providers: {[p.name for p in chain.providers]}")

    rows = []
    for term in TERMS:
        results = chain.search(term, limit=1)
        if results:
            icon = results[0]
            rows.append(
                f'<div style="text-align:center;padding:12px">'
                f'<img src="{icon["image"]}" width="48" height="48" '
                f'style="filter:invert(0)">'
                f'<div style="font-size:12px;margin-top:4px;color:#555">{term}</div>'
                f'<div style="font-size:10px;color:#999">{icon["source"]}</div>'
                f'</div>'
            )

    html = f"""<!DOCTYPE html>
<html><head><title>Reifire Icon Providers</title></head>
<body style="font-family:system-ui;max-width:900px;margin:40px auto;padding:0 20px">
<h1>Reifire Bundled Icons</h1>
<p>Showing {len(rows)} icons from the provider chain</p>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:8px;
    border:1px solid #eee;border-radius:8px;padding:16px">
{''.join(rows)}
</div>
</body></html>"""

    out = Path(tempfile.mktemp(suffix=".html"))
    out.write_text(html)
    print(f"Opening {out}")
    webbrowser.open(f"file://{out}")


if __name__ == "__main__":
    main()
