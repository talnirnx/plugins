---
name: clinic-activity-report
description: Generate a private local veterinary clinic activity report from NxVET data using read-only operations. Use when a clinic owner or manager asks for recording totals, per-device or time-of-day activity, week-over-week trends, silent-device checks, firmware status, or webhook health.
---

# Clinic activity report

Create a plain-English local report for a veterinary clinic owner or manager.
Read NxVET data without creating, editing, deleting, or sending anything.

## Prerequisites

Require an NxVET account and an API key exposed as `NXVET_API_KEY`. Confirm the
organization, reporting window, clinic timezone, and output directory. Never
print, log, commit, or reproduce the full API key.

## Workflow

1. Use the NxVET MCP tools read-only to resolve the identity and organization.
2. Collect activity for the requested window and the immediately preceding
   equal-length window.
3. Collect:
   - total recordings;
   - recording counts by hardware device;
   - counts by clinic-local weekday and hour;
   - hardware-device last-seen and firmware information;
   - recent webhook failures.
4. Do not infer missing numbers. State when comparison data or health data is
   unavailable.
5. Flag a hardware device as silent only when it has not reported for at least
   three days, unless the user selects another threshold. Do not apply this rule
   to web, mobile, or login sessions.
6. Flag firmware only when versions differ semantically. Treat trailing-zero
   variants such as `0.8.13` and `0.8.13.0` as equivalent.
7. Flag webhooks only when recent failed deliveries exist.
8. Write `output/ClinicReport_YYYY-Www.md` with:
   - At a glance;
   - Recordings by device;
   - Busiest days;
   - Busiest times;
   - Health check;
   - Data limitations.
9. Keep every figure traceable to tool results. Add a short interpretation, but
   never invent trends, causes, clinical conclusions, or operational advice.
10. Present the local report for review. Do not email, upload, or publish it.

## Safety rules

- Use only read operations against NxVET.
- Keep reports and retrieved clinic data local.
- Treat organization, device, recording, and webhook data as sensitive.
- Ask before installing software or configuring a recurring scheduler.
- If tool access is unavailable, explain the missing NxVET account/API-key
  requirement and stop without fabricating a report.
