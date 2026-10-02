import json
from datetime import datetime
from pathlib import Path


SOURCE = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

WIDTH = 860
HEIGHT = 180

CELL = 11
GAP = 4
STEP = CELL + GAP

START_X = 48
START_Y = 48


def contribution_opacity(count):
    if count == 0:
        return None

    if count <= 2:
        return 0.28

    if count <= 5:
        return 0.48

    if count <= 9:
        return 0.72

    return 1.0


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"{SOURCE} does not exist."
        )

    data = json.loads(SOURCE.read_text(encoding="utf-8"))

    weeks = data.get("weeks", [])
    total = data.get("totalContributions", 0)

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
""",

        f"""
<text
    x="18"
    y="24"
    fill="#c9d1d9"
    font-family="monospace"
    font-size="12"
>
{total} contributions in the last year
</text>
""",
    ]

    # Weekday labels
    labels = {
        1: "Mon",
        3: "Wed",
        5: "Fri",
    }

    for weekday, label in labels.items():
        y = START_Y + weekday * STEP + 9

        svg.append(
            f"""
<text
    x="8"
    y="{y}"
    fill="#8b949e"
    font-family="monospace"
    font-size="9"
>{label}</text>
"""
        )

    last_month = None

    for week_index, week in enumerate(weeks):
        x = START_X + week_index * STEP

        first_day = week.get("firstDay")

        if first_day:
            date = datetime.strptime(first_day, "%Y-%m-%d")
            month = date.strftime("%b")

            if month != last_month:
                svg.append(
                    f"""
<text
    x="{x}"
    y="41"
    fill="#8b949e"
    font-family="monospace"
    font-size="9"
>{month}</text>
"""
                )

                last_month = month

        for day in week.get("contributionDays", []):
            weekday = day["weekday"]
            count = day["contributionCount"]
            date = day["date"]

            y = START_Y + weekday * STEP

            opacity = contribution_opacity(count)

            if opacity is None:
                fill = "#161b22"
                extra = ""
            else:
                fill = "#7ee787"
                extra = f'fill-opacity="{opacity}"'

            svg.append(
                f"""
<rect
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="2"
    fill="{fill}"
    stroke="#30363d"
    stroke-width="0.5"
    {extra}
>
    <title>{date}: {count} contributions</title>
</rect>
"""
            )

    svg.append(
        """
<text
    x="730"
    y="165"
    fill="#8b949e"
    font-family="monospace"
    font-size="9"
>
less
</text>

<rect x="760" y="156" width="9" height="9" rx="2"
fill="#161b22" stroke="#30363d"/>

<rect x="774" y="156" width="9" height="9" rx="2"
fill="#7ee787" fill-opacity="0.28"/>

<rect x="788" y="156" width="9" height="9" rx="2"
fill="#7ee787" fill-opacity="0.48"/>

<rect x="802" y="156" width="9" height="9" rx="2"
fill="#7ee787" fill-opacity="0.72"/>

<rect x="816" y="156" width="9" height="9" rx="2"
fill="#7ee787"/>

<text
    x="830"
    y="165"
    fill="#8b949e"
    font-family="monospace"
    font-size="9"
>
more
</text>
"""
    )

    svg.append("</svg>")

    OUTPUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
