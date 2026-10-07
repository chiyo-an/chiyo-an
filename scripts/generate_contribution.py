import json
from datetime import date, timedelta
from svg import GRAY, ROOT, command, reveal, save, text


def render(payload):
    days = payload["days"]
    palette = ["#20252d", "#49515c", "#7d8794", "#b6bec9", "#7195c8"]
    parsed = []
    for day in days:
        stamp = date.fromisoformat(day["date"])
        if type(day["level"]) is not int or not 0 <= day["level"] <= 4:
            raise ValueError("Invalid activity level")
        if type(day["count"]) is not int or day["count"] < 0:
            raise ValueError("Invalid activity count")
        parsed.append((stamp, day))
    parsed.sort(key=lambda item: item[0])
    if len({stamp for stamp,_ in parsed}) != len(parsed):
        raise ValueError("Duplicate dates")
    end = parsed[-1][0] if parsed else date.today()
    last_sunday = end - timedelta(days=(end.weekday()+1) % 7)
    start = last_sunday - timedelta(weeks=52)
    lookup = {stamp:day for stamp,day in parsed}
    if parsed and any(not start <= stamp <= end for stamp,_ in parsed):
        raise ValueError("Data exceeds 53-week canvas")
    parts = command("./activity.sh")
    total = sum(day["count"] for _,day in parsed)
    parts += text(28,88,f"{total:,} contributions" if parsed else "Activity data unavailable",14)
    parts += text(28,114,f"{start:%b %d, %Y} — {end:%b %d, %Y}" if parsed else "Run the activity fetch to populate this calendar.",14,GRAY)
    last_month = None
    for week in range(53):
        sunday = start+timedelta(weeks=week)
        if sunday.month != last_month:
            parts += text(50+week*15,147,sunday.strftime("%b"),10,GRAY)
            last_month = sunday.month
        cells = ""
        for row in range(7):
            stamp = sunday+timedelta(days=row)
            day = lookup.get(stamp)
            color = palette[day["level"]] if day else "#11151b"
            label = f"{stamp.isoformat()}: {day['count']} contributions" if day else f"{stamp.isoformat()}: no data"
            cells += f'<rect x="{50+week*15}" y="{162+row*15}" width="11" height="11" rx="2" fill="{color}"><title>{label}</title></rect>'
        parts += reveal(cells,round(week*.012,3))
    for row,label in [(1,"M"),(3,"W"),(5,"F")]:
        parts += text(28,171+row*15,label,10,GRAY)
    parts += text(28,299,"53 weeks / one day at a time",11,GRAY)
    parts += text(673,299,"Less",10,GRAY)
    for i,color in enumerate(palette):
        parts += f'<rect x="{711+i*16}" y="289" width="11" height="11" rx="2" fill="{color}"/>'
    parts += text(801,299,"More",10,GRAY)
    save("contribution.svg",880,330,f"GitHub contribution calendar for {payload['username']}: {total:,} contributions across 53 weeks" if parsed else "GitHub contribution calendar: data unavailable",parts)


if __name__ == "__main__":
    render(json.loads((ROOT / "data/contributions.json").read_text()))
