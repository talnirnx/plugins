#!/usr/bin/env python3
"""Write a deterministic iCalendar file for a timed commitment."""

import argparse
import hashlib
import os
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def _fold(line):
    """Fold content lines to the RFC 5545 limit."""
    output = []
    while len(line.encode("utf-8")) > 75:
        split_at = min(73, len(line))
        while len(line[:split_at].encode("utf-8")) > 73:
            split_at -= 1
        output.append(line[:split_at])
        line = " " + line[split_at:]
    output.append(line)
    return "\r\n".join(output)


def _escape(text):
    return (
        text.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\n", r"\n")
    )


def _slug(text, limit=40):
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (value[:limit] or "event").strip("-")


def _utc_stamp(value):
    return value.strftime("%Y%m%dT%H%M%SZ")


def build_ics(
    summary,
    start_local,
    timezone_name,
    duration_minutes=30,
    transcript="",
    reminder_minutes=15,
):
    """Return an RFC 5545 calendar event as text."""
    timezone = ZoneInfo(timezone_name)
    start = start_local.replace(tzinfo=timezone)
    end = start + timedelta(minutes=duration_minutes)
    uid_input = f"{summary}|{start.isoformat()}|{transcript}".encode()
    uid = hashlib.sha256(uid_input).hexdigest() + "@nxhub-workflows.local"
    stamp = _utc_stamp(start.astimezone(ZoneInfo("UTC")))
    description = _escape(transcript or summary)

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//NerveX//nxhub-workflows//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{stamp}",
        f"DTSTART;TZID={timezone_name}:{start.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND;TZID={timezone_name}:{end.strftime('%Y%m%dT%H%M%S')}",
        _fold(f"SUMMARY:{_escape(summary)}"),
        _fold(f"DESCRIPTION:{description}"),
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        _fold(f"DESCRIPTION:Reminder: {_escape(summary)}"),
        f"TRIGGER:-PT{int(reminder_minutes)}M",
        "END:VALARM",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    return "\r\n".join(lines) + "\r\n"


def write_event(
    summary,
    start_local,
    timezone_name,
    output_directory="output/events",
    duration_minutes=30,
    transcript="",
    reminder_minutes=15,
):
    """Write an event and return its local path."""
    os.makedirs(output_directory, exist_ok=True)
    filename = f"{start_local.strftime('%Y-%m-%d')}_{_slug(summary)}.ics"
    path = os.path.join(output_directory, filename)
    content = build_ics(
        summary,
        start_local,
        timezone_name,
        duration_minutes,
        transcript,
        reminder_minutes,
    )
    with open(path, "w", encoding="utf-8", newline="") as calendar_file:
        calendar_file.write(content)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument(
        "--start",
        required=True,
        help="Local ISO datetime, for example 2026-07-15T10:00:00",
    )
    parser.add_argument("--tz", default="America/New_York")
    parser.add_argument("--duration-min", type=int, default=30)
    parser.add_argument("--reminder-min", type=int, default=15)
    parser.add_argument("--transcript", default="")
    parser.add_argument("--outdir", default="output/events")
    arguments = parser.parse_args()

    path = write_event(
        arguments.summary,
        datetime.fromisoformat(arguments.start),
        arguments.tz,
        arguments.outdir,
        arguments.duration_min,
        arguments.transcript,
        arguments.reminder_min,
    )
    print(path)


if __name__ == "__main__":
    main()
