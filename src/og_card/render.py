from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
FONT_CANDIDATES = (
    "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/Arial.ttf",
)


def load_font(size: int, font_path: Path | None = None) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = ([font_path] if font_path else []) + [Path(p) for p in FONT_CANDIDATES]
    for candidate in candidates:
        if candidate and candidate.is_file():
            try:
                return ImageFont.truetype(str(candidate), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    """Wrap at word boundaries using actual font metrics."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and font.getlength(candidate) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [""]


def create_card(title: str, author: str, category: str, output: Path,
                font_path: Path | None = None) -> Path:
    if not title.strip():
        raise ValueError("title cannot be empty")
    image = Image.new("RGB", (WIDTH, HEIGHT), "#10182d")
    draw = ImageDraw.Draw(image)
    # A subtle navy-to-indigo vertical gradient, drawn without extra dependencies.
    start, end = (14, 23, 43), (45, 42, 101)
    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        color = tuple(round(a + (b - a) * ratio) for a, b in zip(start, end))
        draw.line((0, y, WIDTH, y), fill=color)
    draw.rounded_rectangle((64, 56, 1136, 574), radius=34, outline="#55658b", width=2)
    draw.ellipse((930, -160, 1310, 220), fill="#4d52a5")
    draw.ellipse((1010, -110, 1280, 160), fill="#10182d")
    draw.rounded_rectangle((104, 104, 330, 148), radius=20, fill="#273a5c")
    draw.text((124, 113), category.strip().upper()[:24] or "ARTICLE", font=load_font(19, font_path), fill="#b7c9ff")

    font_size = 58
    title_font = load_font(font_size, font_path)
    lines = wrap_text(title.strip(), title_font, 930)
    while (len(lines) > 4 or sum(title_font.getbbox(line)[3] - title_font.getbbox(line)[1] + 13 for line in lines) > 300) and font_size > 30:
        font_size -= 2
        title_font = load_font(font_size, font_path)
        lines = wrap_text(title.strip(), title_font, 930)
    y = 205
    for line in lines[:5]:
        draw.text((104, y), line, font=title_font, fill="#f5f7ff")
        box = title_font.getbbox(line)
        y += (box[3] - box[1]) + 14
    draw.line((104, 493, 1096, 493), fill="#68779b", width=2)
    draw.text((104, 520), f"By {author.strip() or 'Author'}", font=load_font(22, font_path), fill="#d2dbf1")
    draw.text((960, 520), "READ · THINK · BUILD", font=load_font(14, font_path), fill="#a8b5d2")
    output = output.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)
    return output
