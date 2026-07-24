---
name: voice-notes-to-reminders
description: Turn NxHUB voice recordings into private local reminder notes and calendar (.ics) files. Use when a user asks to review recent NxHUB voice notes, extract commitments or follow-ups, build a daily triage note, or create calendar-event drafts without sending anything.
---

# Voice notes to reminders

Create reminder artifacts on the user's machine from NxHUB recordings. Keep the
workflow local after reading the recordings: never send email, messages, invites,
telemetry, or clinic data to another service.

## Prerequisites

Require:

- an NxVET account;
- an NxVET API key set locally as `NXVET_API_KEY` or in the project `.env`;
- access to an NxHUB device or its recordings.

Explain these requirements before attempting API-backed work. Never print, log,
commit, transmit, or reproduce the full API key. Ask the user to set the key
locally; do not ask them to paste it into chat.

## Workflow

1. Confirm the intended date range, device, output directory, and timezone.
2. Create a local project directory. Ensure `.env`, `state/`, and `output/` are
   ignored if the project uses git.
3. Read `references/nxvet-api.md` and `references/security.md`. Use authenticated
   GET requests only to resolve the identity and organization and identify the
   relevant device.
4. Determine empirically whether recordings appear as labels or NxHUB
   conversations, then save `organizationId`, device information, timezone, and
   source in `config.json`.
5. Locate this skill's directory and run the bundled GET-only poller:

   ```bash
   python3 <skill-dir>/scripts/nxvet_poll.py
   ```

6. Ignore empty transcripts. Keep `state/processed_ids.json` in the output project
   and skip IDs already recorded there.
7. Classify each new transcript:
   - timed commitment: create an `.ics` draft and a Scheduled triage entry;
   - untimed follow-up: create a Follow-ups entry and suggest a date;
   - idea or note: create an Ideas entry;
   - ambiguous item: create an Unclear entry without inventing a time;
   - long ambient conversation: summarize it under Ambient and avoid extracting
     every incidental statement as a reminder.
8. Resolve relative dates from the recording timestamp in the user's timezone,
   not from the processing time.
9. Write `output/Reminders_YYYY-MM-DD.md`. Quote the relevant transcript sentence
   beside every extracted item so the user can verify it.
10. For timed commitments, run:

   ```bash
   python3 <skill-dir>/scripts/make_ics.py \
     --summary "Follow up with Sally" \
     --start 2026-07-15T10:00:00 \
     --tz America/Toronto \
     --transcript "Original transcript text" \
     --outdir output/events
   ```

11. Mark an item processed only after its local outputs are written successfully:

    ```bash
    python3 <skill-dir>/scripts/nxvet_poll.py --mark <recording-id>
    ```

12. Present the generated files for review. Do not import events or send anything
    on the user's behalf.

## Safety rules

- Make only authenticated GET requests against NxVET.
- Keep reminder notes, calendar files, state, and transcripts local.
- Treat recordings and transcripts as sensitive clinic information.
- Ask before installing software or configuring a scheduler.
- If API access is unavailable, explain the missing NxVET account/API-key
  requirement and stop without fabricating data.

## References

- `references/nxvet-api.md` documents the read-only endpoints and response quirks.
- `references/security.md` defines secrets and local-data handling.
- `references/caching-and-state.md` defines idempotency and overlapping windows.
- `references/good-practices.md` covers error handling, timezones, and testing.
