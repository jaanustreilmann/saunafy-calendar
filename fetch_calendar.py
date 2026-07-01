import requests
from icalendar import Calendar
import json
import os
from datetime import date

ICAL_URL = os.environ["AIRBNB_ICAL_URL"]

resp = requests.get(ICAL_URL, timeout=20)
cal = Calendar.from_ical(resp.text)

busy = []
for component in cal.walk():
    if component.name == "VEVENT":
        start = component.get("dtstart").dt
        end = component.get("dtend").dt
        if isinstance(start, date):
            busy.append({"start": start.isoformat(), "end": end.isoformat()})

with open("availability.json", "w") as f:
    json.dump({"busy": busy, "updated": date.today().isoformat()}, f)
