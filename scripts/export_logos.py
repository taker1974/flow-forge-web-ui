#!/usr/bin/env python3
"""
Export logo panels from logo-company-01.html to vector SVG files.

Pipeline:
  HTML panel -> Chrome headless PDF -> pdftocairo SVG

Why this script exists:
  - Preserves browser layout more accurately than hand-written SVG
  - Waits for web fonts to load
  - Resolves CSS color vars to explicit HEX to avoid color loss in PDF->SVG
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent.parent
SOURCE_HTML = ROOT / "logo-company-01.html"
OUTPUT_DIR = ROOT / "images" / "svg"
TMP_DIR = OUTPUT_DIR / ".tmp_export"


# CSS vars used in logo-company-01.html that can break in PDF->SVG conversion.
COLOR_MAP = {
    "var(--c1)": "#003366",
    "var(--c2)": "#0055aa",
    "var(--c3)": "#007bff",
    "var(--c4)": "#00aeef",
}


def resolve_color_vars(html_fragment: str) -> str:
    out = html_fragment
    for key, value in COLOR_MAP.items():
        out = out.replace(key, value)
    return out


def panel_size(panel, label: str) -> tuple[int, int]:
    has_flowforge = panel.find("div", attrs={"aria-label": "FlowForge by TKSoft"}) is not None
    has_sub = panel.find("p") is not None
    is_futura = "futura" in label

    width = 227 if is_futura else 190
    if has_flowforge:
        height = 234
    elif has_sub:
        height = 253 if is_futura else 227
    else:
        height = 214
    return width, height


def render_panel_html(panel_html: str, width: int, height: int) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600&family=Jost:wght@600&family=Manrope:wght@600&family=Nunito+Sans:wght@600&family=Urbanist:wght@600&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800&display=swap" rel="stylesheet" />
  <style>
    @page {{ size: {width}px {height}px; margin: 0; }}
    html, body {{
      margin: 0;
      width: {width}px;
      height: {height}px;
      overflow: hidden;
      background: transparent;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}
    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}
  </style>
</head>
<body>
{panel_html}
</body>
</html>
"""


def run() -> None:
    if not SOURCE_HTML.exists():
        raise FileNotFoundError(f"Not found: {SOURCE_HTML}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    doc = SOURCE_HTML.read_text(encoding="utf-8")
    soup = BeautifulSoup(doc, "html.parser")
    container = soup.select_one("div.logo-variants")
    if container is None:
        raise RuntimeError("Could not find div.logo-variants in source HTML")

    panels = list(container.find_all("div", recursive=False))

    # Remove existing exports to avoid stale files.
    for old in OUTPUT_DIR.glob("*-export.svg"):
        old.unlink()

    for idx, panel in enumerate(panels, start=1):
        label = (panel.get("aria-label") or "").lower()
        width, height = panel_size(panel, label)

        panel_html = resolve_color_vars(str(panel))
        html_payload = render_panel_html(panel_html, width, height)

        html_file = TMP_DIR / f"{idx:02d}.html"
        pdf_file = TMP_DIR / f"{idx:02d}.pdf"
        svg_file = OUTPUT_DIR / f"{idx:02d}-export.svg"

        html_file.write_text(html_payload, encoding="utf-8")

        subprocess.run(
            [
                "google-chrome",
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--no-pdf-header-footer",
                "--virtual-time-budget=15000",
                f"--print-to-pdf={pdf_file}",
                f"file://{html_file}",
            ],
            check=True,
        )

        subprocess.run(
            ["pdftocairo", "-svg", str(pdf_file), str(svg_file)],
            check=True,
        )

    shutil.rmtree(TMP_DIR)
    print(f"Exported {len(panels)} panels to {OUTPUT_DIR}")


if __name__ == "__main__":
    run()
