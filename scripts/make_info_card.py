from pathlib import Path
from html import escape


OUTPUT = Path("info-card.svg")

WIDTH = 520
HEIGHT = 430


LINES = [
    ("Name", "Mukand Mapara"),
    ("Role", "Frontend Developer"),
    ("Focus", "Scalable, high-performance web apps"),
    ("Frontend", "React.js / Next.js / TypeScript"),
    ("Styling", "Tailwind CSS / Bootstrap / CSS3"),
    ("State", "Redux"),
    ("Backend", "Firebase"),
    ("Tools", "Git / GitHub / npm / VS Code"),
    ("Portfolio", "mukand-mapara.vercel.app"),
    ("LinkedIn", "linkedin.com/in/mukand-kirshana"),
    ("Email", "mukandkirshana1606@gmail.com"),
]


def main():
    svg = [
        f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">''',

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
neofetch
</text>

<text
    x="22"
    y="54"
    fill="#58a6ff"
    font-family="monospace"
    font-weight="bold"
    font-size="15"
>
mukand-mapara@github
</text>

<line
    x1="22"
    y1="65"
    x2="490"
    y2="65"
    stroke="#30363d"
/>
"""
    ]

    start_y = 92
    spacing = 28

    for index, (label, value) in enumerate(LINES):
        y = start_y + index * spacing
        begin = 0.15 + index * 0.12

        svg.append(
            f"""
<g opacity="0">
    <animate
        attributeName="opacity"
        from="0"
        to="1"
        dur="0.25s"
        begin="{begin:.2f}s"
        fill="freeze"
    />

    <text
        x="22"
        y="{y}"
        fill="#7ee787"
        font-family="monospace"
        font-size="12"
        font-weight="bold"
    >{escape(label)}:</text>

    <text
        x="115"
        y="{y}"
        fill="#c9d1d9"
        font-family="monospace"
        font-size="12"
    >{escape(value)}</text>
</g>
"""
        )

    svg.append(
        """
<text
    x="22"
    y="410"
    fill="#58a6ff"
    font-family="monospace"
    font-size="12"
>
$
</text>

<rect
    x="34"
    y="399"
    width="7"
    height="13"
    fill="#c9d1d9"
>
    <animate
        attributeName="opacity"
        values="1;0;1"
        dur="1s"
        repeatCount="indefinite"
    />
</rect>

</svg>
"""
    )

    OUTPUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
