---
name: greet-helloname-withdatetime
description: Emit a name-aware greeting when the user's request begins with "Hi".
allowed-tools:
---

Use this skill only when the user's message starts with `Hi` (case-insensitive).

Follow these steps:

1. If an actual name is available in earlier context, reply with exactly: `Hello, <actual-name>`
2. If no actual name is available in earlier context, reply with exactly: `Hello, there`
3. Then continue and fulfill the user's request normally.