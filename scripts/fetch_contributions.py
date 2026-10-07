import argparse
import json
import re
import sys
import time
from datetime import date
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from svg import ROOT


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tooltips = {}
        self.target = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("td", "rect") and "data-date" in attrs:
            day = date.fromisoformat(attrs["data-date"])
            level = int(attrs["data-level"])
            if not 0 <= level <= 4 or day.isoformat() in self.cells:
                raise ValueError("Invalid or duplicate contribution cell")
            self.cells[day.isoformat()] = {"date": day.isoformat(), "level": level, "id": attrs.get("id")}
        if tag == "tool-tip":
            self.target = attrs.get("for")
            if self.target:
                self.tooltips[self.target] = ""

    def handle_data(self, data):
        if self.target:
            self.tooltips[self.target] += data

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self.target = None


def parse_calendar(html):
    parser = CalendarParser()
    parser.feed(html)
    days = []
    for cell in sorted(parser.cells.values(), key=lambda c: c["date"]):
        tooltip = parser.tooltips.get(cell["id"], "").strip()
        match = re.match(r"([\d,]+) contributions?\b", tooltip)
        if tooltip.startswith("No contributions"):
            count = 0
        elif match:
            count = int(match[1].replace(",", ""))
        else:
            raise ValueError(f"Missing contribution count for {cell['date']}; GitHub HTML may have changed")
        if (count == 0) != (cell["level"] == 0):
            raise ValueError("Contribution count and level disagree")
        days.append({"date": cell["date"], "level": cell["level"], "count": count})
    if not 365 <= len(days) <= 371:
        raise ValueError(f"Expected a full calendar, received {len(days)} days")
    dates = [date.fromisoformat(d["date"]) for d in days]
    if any((b-a).days != 1 for a,b in zip(dates,dates[1:])):
        raise ValueError("Contribution dates are not consecutive")
    if not 0 <= (date.today()-dates[-1]).days <= 2:
        raise ValueError("Contribution calendar is stale or in the future")
    return days


def fetch(username):
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", username):
        raise ValueError("Invalid GitHub username")
    request = Request(f"https://github.com/users/{username}/contributions", headers={"User-Agent": "chiyo-profile-generator", "Accept": "text/html"})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=25) as response:
                if "text/html" not in response.headers.get("Content-Type", ""):
                    raise ValueError("GitHub returned non-HTML data")
                return parse_calendar(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--username", default="chiyo-an")
    username = args.parse_args().username
    try:
        days = fetch(username)
        payload = {"username": username, "days": days}
        path = ROOT / "data/contributions.json"
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, indent=2) + "\n")
        temporary.replace(path)
        print(f"Fetched {len(days)} real contribution days for {username}")
    except (ValueError, KeyError, URLError, TimeoutError, OSError) as error:
        print(f"Activity fetch failed; existing data preserved: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
