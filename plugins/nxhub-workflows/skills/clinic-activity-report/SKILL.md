---
name: clinic-activity-report
description: Generate a private local veterinary clinic activity report from NxVET data using read-only operations. Use when a clinic owner or manager asks for recording totals, per-device or time-of-day activity, week-over-week trends, silent-device checks, firmware status, or webhook health.
---

# Clinic activity report

Create a plain-English local report for a veterinary clinic owner or manager.
Read NxVET data without creating, editing, deleting, or sending anything.

## Prerequisites

Require an NxVET account and an API key set locally as `NXVET_API_KEY` or in the
project `.env`. Confirm the organization, reporting window, clinic timezone, and
output directory. Never print, log, commit, transmit, or reproduce the full API
key. Ask the user to set the key locally; do not ask them to paste it into chat.

## Workflow

1. Create a local project directory. Ensure `.env`, `state/`, and `output/` are
   ignored if the project uses git.
2. Read `references/nxvet-api.md` and `references/security.md`. Use authenticated
   GET requests only to resolve the identity and organization, then save
   `organizationId`, `organizationName`, and timezone in `config.json`.
3. Locate this skill's directory and collect activity for the requested window
   and immediately preceding equal-length window:

   ```bash
   python3 <skill-dir>/scripts/collect_stats.py --days 7 > stats.json
   ```

4. The collector gathers:
   - total recordings;
   - recording counts by hardware device;
   - counts by clinic-local weekday and hour;
   - hardware-device last-seen and firmware information;
   - recent webhook failures.
5. Do not infer missing numbers. State when comparison data or health data is
   unavailable.
6. Flag a hardware device as silent only when it has not reported for at least
   three days, unless the user selects another threshold. Do not apply this rule
   to web, mobile, or login sessions.
7. Flag firmware only when versions differ semantically. Treat trailing-zero
   variants such as `0.8.13` and `0.8.13.0` as equivalent.
8. Flag webhooks only when recent failed deliveries exist.
9. Write `output/ClinicReport_YYYY-Www.md` with:
   - At a glance;
   - Recordings by device;
   - Busiest days;
   - Busiest times;
   - Health check;
   - Data limitations.
   For deterministic output, run:

   ```bash
   python3 <skill-dir>/scripts/write_report.py \
     --in stats.json \
     --out output/ClinicReport_YYYY-Www.md
   ```

10. Keep every figure traceable to collected data. Add a short interpretation, but
   never invent trends, causes, clinical conclusions, or operational advice.
11. Present the local report for review. Do not email, upload, or publish it.

## Safety rules

- Make only authenticated GET requests against NxVET.
- Keep reports and retrieved clinic data local.
- Treat organization, device, recording, and webhook data as sensitive.
- Ask before installing software or configuring a recurring scheduler.
- If API access is unavailable, explain the missing NxVET account/API-key
  requirement and stop without fabricating a report.

## References

- `references/nxvet-api.md` documents the read-only endpoints and response quirks.
- `references/security.md` defines secrets and local-data handling.
- `references/caching-and-state.md` defines local caching behavior.
- `references/good-practices.md` covers honest reporting and health flags.
