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
- an NxVET API key exposed as `NXVET_API_KEY`;
- access to an NxHUB device or its recordings.

Explain these requirements before attempting API-backed work. Never print, log,
commit, or reproduce the full API key.

## Workflow

1. Confirm the intended date range, device, output directory, and timezone.
2. Use the NxVET MCP tools read-only. Resolve the identity and organization, list
   recent devices, then inspect recent labels and NxHUB conversations.
3. Determine empirically whether the requested recordings appear as labels or
   conversations. Fetch item details because list results may omit transcripts.
4. Ignore empty transcripts. Keep `state/processed_ids.json` in the output project
   and skip IDs already recorded there.
5. Classify each new transcript:
   - timed commitment: create an `.ics` draft and a Scheduled triage entry;
   - untimed follow-up: create a Follow-ups entry and suggest a date;
   - idea or note: create an Ideas entry;
   - ambiguous item: create an Unclear entry without inventing a time;
   - long ambient conversation: summarize it under Ambient and avoid extracting
     every incidental statement as a reminder.
6. Resolve relative dates from the recording timestamp in the user's timezone,
   not from the processing time.
7. Write `output/Reminders_YYYY-MM-DD.md`. Quote the relevant transcript sentence
   beside every extracted item so the user can verify it.
8. For timed commitments, locate this skill's directory and run:

   ```bash
   python3 <skill-dir>/scripts/make_ics.py \
     --summary "Follow up with Sally" \
     --start 2026-07-15T10:00:00 \
     --tz America/Toronto \
     --transcript "Original transcript text" \
     --outdir output/events
   ```

9. Mark an item processed only after its local outputs are written successfully.
10. Present the generated files for review. Do not import events or send anything
    on the user's behalf.

## Safety rules

- Make only read operations against NxVET.
- Keep reminder notes, calendar files, state, and transcripts local.
- Treat recordings and transcripts as sensitive clinic information.
- Ask before installing software or configuring a scheduler.
- If tool access is unavailable, explain the missing NxVET account/API-key
  requirement and stop without fabricating data.
