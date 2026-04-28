---
name: greet-helloname-withdatetime
description: Emit a name-aware greeting when the user's request begins with "Hi".
allowed-tools:
---

Use this skill only when the user's message starts with `Hi` (case-insensitive).

Follow these steps:

1. Run `python datetime.py` and capture its output as the timestamp.
2. Ensure the timestamp is in this exact format: `YYYY-MM-DD-HHMMSS`.
3. If an actual name is available in earlier context, reply with exactly: `YYYY-MM-DD-HHMMSS: Hello, <actualname>` using the timestamp from step 1.
4. If no actual name is available in earlier context, reply with exactly: `YYYY-MM-DD-HHMMSS: Hello, there` using the timestamp from step 1.
5. Then continue and fulfill the user's request normally.