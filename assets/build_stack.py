"""Build the two-row stack icon strip shown on the profile README.

skillicons.dev has no Airflow, Spark, Databricks, dbt or BigQuery, so those are
drawn here as tiles with skillicons' own geometry and colours, and both rows are
written into one static SVG per theme. The README then depends on no live icon
service, and the custom tiles cannot drift out of line with the stock ones.

Run after editing ROWS:

    python3 assets/build_stack.py

Writes assets/stack-dark.svg and assets/stack-light.svg. Standard library only.
"""

from __future__ import annotations

import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path

OUT = Path(__file__).resolve().parent

# skillicons.dev geometry: a 256-unit tile on a 300-unit stride, 48 px tall on the page.
TILE, STRIDE, PX = 256, 300, 48
TILE_FILL = {"dark": "#242938", "light": "#F4F2ED"}
GLYPH = 184  # side of the box a custom logo is fitted into; skillicons' own glyphs run 190-200

SIMPLE_ICONS = "https://cdn.jsdelivr.net/npm/simple-icons@16.33.0/icons/{}.svg"
DEVICON = "https://cdn.jsdelivr.net/npm/devicon@2.17.0/icons/{0}/{0}-original.svg"
DBT_BIT = (
    "https://raw.githubusercontent.com/dbt-labs/docs.getdbt.com/"
    "a864cf0264e76e6f258f623d9b8a6b9756b60806/website/static/img/icons/dbt-bit.svg"
)

@dataclass(frozen=True)
class Logo:
    """A logo skillicons.dev does not have, drawn onto a tile of the same shape."""

    url: str
    fill: str | None = None  # colours a single-colour glyph; None keeps the logo's own colours
    view_box: str | None = None  # crops to the glyph when the source pads it
    paths: int | None = None  # keep only the first N paths, dropping marks such as (R)


# A plain string is a skillicons.dev id.
ROWS: list[list[str | Logo]] = [
    # Languages, ML and the software around it
    ["python", "pytorch", "rust", "ts", "react", "fastapi",
     "docker", "kubernetes", "linux", "git", "githubactions"],
    # Data engineering
    ["gcp",
     Logo(SIMPLE_ICONS.format("googlebigquery"), fill="#669DF6"),
     # The second path is the (R) mark, a one-pixel speck at 48 px, and the source
     # pads the glyph to make room for it: the box below is the glyph's own bbox.
     Logo(DBT_BIT, fill="#F16122", view_box="10.66 4.5 80.99 81", paths=1),
     Logo(DEVICON.format("apacheairflow")),
     Logo(DEVICON.format("apachespark")),
     Logo(SIMPLE_ICONS.format("databricks"), fill="#FF3621"),
     "kafka", "terraform", "postgres"],
]


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "profile-stack-builder"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def skillicon(icon_id: str, theme: str) -> str:
    """The inner 256x256 tile skillicons.dev nests inside its row wrapper."""
    row = fetch(f"https://skillicons.dev/icons?i={icon_id}&theme={theme}")
    match = re.search(r"<g transform=\"translate\(0, 0\)\">\s*(<svg.*</svg>)\s*</g>", row, re.S)
    if not match or "undefined" in row:
        raise SystemExit(f"skillicons.dev has no icon {icon_id!r}")
    return match.group(1)


def custom_tile(logo: Logo, theme: str) -> str:
    """A skillicons-shaped tile with an external logo fitted into its centre."""
    source = fetch(logo.url)
    if re.search(r"<script|\son[a-z]+\s*=", source, re.I):
        raise SystemExit(f"refusing an SVG with script in it: {logo.url}")
    view_box = logo.view_box or re.search(r"viewBox=\"([^\"]+)\"", source).group(1)
    body = re.search(r"<svg[^>]*>(.*)</svg>", source, re.S).group(1)
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S).strip()
    if logo.paths:
        body = "".join(re.findall(r"<path\b[^>]*/>", body)[: logo.paths])
    if logo.fill:
        body = f'<g fill="{logo.fill}">{body}</g>'
    offset = (TILE - GLYPH) // 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{TILE}" height="{TILE}" '
        f'viewBox="0 0 {TILE} {TILE}" fill="none">'
        f'<rect width="{TILE}" height="{TILE}" fill="{TILE_FILL[theme]}" rx="60"/>'
        f'<svg x="{offset}" y="{offset}" width="{GLYPH}" height="{GLYPH}" '
        f'viewBox="{view_box}">{body}</svg></svg>'
    )


def build(theme: str) -> str:
    widest = max(len(row) for row in ROWS)
    width = widest * STRIDE - (STRIDE - TILE)
    height = len(ROWS) * STRIDE - (STRIDE - TILE)
    tiles = []
    for y, row in enumerate(ROWS):
        indent = (widest - len(row)) * STRIDE // 2  # centre a shorter row
        for x, icon in enumerate(row):
            tile = skillicon(icon, theme) if isinstance(icon, str) else custom_tile(icon, theme)
            tiles.append(f'<g transform="translate({indent + x * STRIDE}, {y * STRIDE})">{tile}</g>')
    scale = PX / TILE
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * scale:g}" '
        f'height="{height * scale:g}" viewBox="0 0 {width} {height}" fill="none">\n'
        + "\n".join(tiles)
        + "\n</svg>\n"
    )


def main() -> None:
    for theme in ("dark", "light"):
        svg = build(theme)
        ids = re.findall(r'\bid="([^"]+)"', svg)
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        if duplicates:
            raise SystemExit(f"duplicate ids would cross-wire gradients: {duplicates}")
        path = OUT / f"stack-{theme}.svg"
        path.write_text(svg)
        print(f"{path.name}: {len(svg):,} bytes")


if __name__ == "__main__":
    main()
