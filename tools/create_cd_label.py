#!/usr/bin/env python3
"""Create a printable CD label PDF."""

from __future__ import annotations

from datetime import date
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch, mm
    from reportlab.pdfgen import canvas
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit(
        "Missing reportlab. Install it or use the bundled Codex Python runtime."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
PRINT_DIR = ROOT / "print"
OUTPUT = PRINT_DIR / "PJmaster-CD-label.pdf"


def draw_centered(pdf: canvas.Canvas, y: float, text: str, size: int, color=colors.black) -> None:
    width, _ = letter
    pdf.setFillColor(color)
    pdf.setFont("Helvetica-Bold" if size >= 16 else "Helvetica", size)
    pdf.drawCentredString(width / 2, y, text)


def main() -> int:
    PRINT_DIR.mkdir(exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter)
    width, height = letter

    pdf.setTitle("PJmaster CD Label")
    pdf.setAuthor("PJmaster")

    center_x = width / 2
    center_y = height / 2 + 0.4 * inch
    disc_radius = 60 * mm
    hub_radius = 7.5 * mm

    pdf.setFillColor(colors.HexColor("#F7F4EC"))
    pdf.rect(0, 0, width, height, stroke=0, fill=1)

    pdf.setStrokeColor(colors.HexColor("#2F3A3D"))
    pdf.setLineWidth(1.2)
    pdf.circle(center_x, center_y, disc_radius, stroke=1, fill=0)
    pdf.setStrokeColor(colors.HexColor("#8B8F91"))
    pdf.setDash(3, 3)
    pdf.circle(center_x, center_y, hub_radius, stroke=1, fill=0)
    pdf.setDash()

    draw_centered(pdf, center_y + 1.35 * inch, "PJmaster", 28, colors.HexColor("#1E2A2F"))
    draw_centered(pdf, center_y + 0.92 * inch, "Family Handoff Index", 14, colors.HexColor("#455054"))
    draw_centered(pdf, center_y + 0.48 * inch, "Public repo - no secrets", 11, colors.HexColor("#6A4D2E"))
    draw_centered(
        pdf,
        center_y - 0.48 * inch,
        "github.com/ChristFollower873461/PJmaster",
        9,
        colors.HexColor("#1E2A2F"),
    )
    draw_centered(pdf, center_y - 0.88 * inch, f"Printed package: {date.today().isoformat()}", 9)

    pdf.setStrokeColor(colors.HexColor("#C9BFAE"))
    pdf.line(center_x - 1.5 * inch, center_y + 0.15 * inch, center_x + 1.5 * inch, center_y + 0.15 * inch)
    pdf.line(center_x - 1.5 * inch, center_y - 0.15 * inch, center_x + 1.5 * inch, center_y - 0.15 * inch)

    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(colors.HexColor("#5C6265"))
    pdf.drawString(0.75 * inch, 0.65 * inch, "Print at 100 percent scale. This is an index, not the private vault.")

    pdf.showPage()
    pdf.save()
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
