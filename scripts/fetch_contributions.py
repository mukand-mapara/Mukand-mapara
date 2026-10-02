import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests


USERNAME = "mukand-mapara"
OUTPUT = Path("data/contributions.json")

API_URL = "https://api.github.com/graphql"


QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          firstDay
          contributionDays {
            date
            contributionCount
            weekday
          }
        }
      }
    }
  }
}
"""


def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

    if not token:
        raise RuntimeError(
            "GitHub token missing. Set GH_TOKEN or GITHUB_TOKEN."
        )

    now = datetime.now(timezone.utc)
    start = now - timedelta(days=364)

    variables = {
        "login": USERNAME,
        "from": start.isoformat().replace("+00:00", "Z"),
        "to": now.isoformat().replace("+00:00", "Z"),
    }

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "query": QUERY,
            "variables": variables,
        },
        timeout=30,
    )

    response.raise_for_status()

    payload = response.json()

    if payload.get("errors"):
        raise RuntimeError(payload["errors"])

    user = payload.get("data", {}).get("user")

    if not user:
        raise RuntimeError(f"GitHub user '{USERNAME}' was not found.")

    calendar = user["contributionsCollection"]["contributionCalendar"]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(calendar, indent=2),
        encoding="utf-8",
    )

    print(
        f"Fetched {calendar['totalContributions']} contributions."
    )


if __name__ == "__main__":
    main()
