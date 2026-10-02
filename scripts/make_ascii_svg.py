from pathlib import Path
from html import escape

from PIL import Image


SOURCE = Path("data/profile-prepped.png")
OUTPUT = Path("ascii-portrait.svg")

ASCII_CHARS = "@%#*+=-:. "


def pixel_to_ascii(pixel):
    index = int(pixel / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"{SOURCE} not found. Run prep_photo.py first."
        )

    image = Image.open(SOURCE).convert("L")

    width = 45
    height = 32

    image = image.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    )

    lines = []

    for y in range(height):
        line = ""

        for x in range(width):
            pixel = image.getpixel((x, y))
            line += pixel_to_ascii(pixel)

        lines.append(line.rstrip())

    svg_width = 420
    svg_height = 430

    start_x = 18
    start_y = 58
    line_height = 11

    svg = [
        f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">''',

        """
<rect
    width="100%"
    height="100%"
    rx="10"
    fill="#0d1117"
    stroke="#30363d"
/>

<circle cx="18" cy="18" r="4" fill="#8b949e"/>
<circle cx="32" cy="18" r="4" fill="#8b949e"/>
<circle cx="46" cy="18" r="4" fill="#8b949e"/>

<text
    x="64"
    y="22"
    fill="#8b949e"
    font-family="monospace"
    font-size="11"
>
mukand-mapara@github
</text>

<text
    x="18"
    y="43"
    fill="#7ee787"
    font-family="monospace"
    font-size="11"
>
$ cat mukand.txt
</text>
""",
    ]

    # Create animated clipping masks.
    svg.append("<defs>")

    for index in range(len(lines)):
        y = start_y + index * line_height

        begin = index * 0.055

        svg.append(
            f"""
<clipPath id="line-{index}">
    <rect
        x="{start_x}"
        y="{y - 10}"
        width="0"
        height="{line_height + 2}"
    >
        <animate
            attributeName="width"
            from="0"
            to="390"
            dur="0.55s"
            begin="{begin:.2f}s"
            fill="freeze"
        />
    </rect>
</clipPath>
"""
        )

    svg.append("</defs>")

    for index, line in enumerate(lines):
        y = start_y + index * line_height

        svg.append(
            f"""
<text
    x="{start_x}"
    y="{y}"
    fill="#c9d1d9"
    font-family="'Courier New', monospace"
    font-size="9.5"
    xml:space="preserve"
    clip-path="url(#line-{index})"
>{escape(line)}</text>
"""
        )

    svg.append(
        """
<rect
    x="18"
    y="410"
    width="7"
    height="12"
    fill="#58a6ff"
>
    <animate
        attributeName="opacity"
        values="1;0;1"
        dur="1s"
        repeatCount="indefinite"
    />
</rect>
"""
    )

    svg.append("</svg>")

    OUTPUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
