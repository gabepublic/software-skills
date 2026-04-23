# Choosing `def` vs `async def`

Two skills: [fastapi](../../fastapi/SKILL.md) and [async-python-patterns](../../async-python-patterns/SKILL.md), provide guidances for the `def` vs `async def`. They are **aligned**, not opposed. The following provides further guidance so an agent never has to pick between them arbitrarily.

## When to use this skill

- Choosing `def` vs `async def` for path operations, dependencies, or lifespan hooks
- Calling blocking libraries from async code (or the reverse)
- Writing concurrent async logic (gather, queues, timeouts) inside a FastAPI app
- Reviewing whether “stay sync or async on a call path” conflicts with FastAPI guidance

## Single rule (both skills agree)

**Do not block the asyncio event loop.** Use the right execution context for the work: async-native I/O on the loop, blocking work off the loop (thread pool, subprocess, or a plain synchronous call path).

FastAPI’s recommendation to use plain `def` handlers for blocking or uncertain code is one way to keep blocking work **off** the loop: those handlers run in a **thread pool**, so they are not the same as `time.sleep()` inside an `async def` coroutine.

## Practical precedence (layering)

| Layer | Lead skill | Apply |
|-------|------------|--------|
| Route shape: `def` vs `async def` | **fastapi** | Use `async def` when the body `await`s async APIs; use `def` when work is blocking or you are unsure (thread pool). |
| Dependencies, routers, `yield` cleanup, framework tools (e.g. Asyncer) | **fastapi** | Follow FastAPI’s dependency and router patterns; use Asyncer when the docs point you there for mixing async and blocking code. |
| Lifespan, startup/shutdown, background tasks | **fastapi** first, **async-python-patterns** for asyncio details | Keep framework lifecycle APIs correct; use asyncio patterns for scheduling, cancellation, and timeouts inside async portions. |
| Concurrent async work, locks, queues, semaphores, async context managers | **async-python-patterns** | `gather`, `wait_for`, `create_task`, async iteration, producer/consumer queues, etc. |
| Offloading blocking code from async contexts | **async-python-patterns** | `asyncio.to_thread`, executors, choosing async-native clients (`httpx.AsyncClient`, async DB drivers). |
| Testing async code | **async-python-patterns** (+ **python-testing-patterns** if loaded) | `pytest.mark.asyncio`, async fixtures, not forgetting `await`. |

**Short form:** **fastapi** owns the **HTTP/framework surface** (how the app runs your code). **async-python-patterns** owns **asyncio usage** inside async stacks and any generic async Python outside that surface.

## Resolving the “fully sync or fully async per call path” phrase

[async-python-patterns](../../async-python-patterns/SKILL.md) warns against **mixing blocking synchronous calls into an `async def` coroutine** that runs on the event loop. That is still correct in FastAPI apps.

A **`def` path operation** is not a violation of that rule: its body runs in a **worker thread**, not on the main event loop. Treat it as a **deliberate synchronous call path** the framework schedules for you.

An **`async def` path operation`** must not call blocking sync APIs directly; use async libraries, or offload (`asyncio.to_thread`, Asyncer per FastAPI references, etc.).

## Checklist before merging async + FastAPI changes

- [ ] Blocking or CPU-heavy work is **not** inside a bare `async def` handler without offload.
- [ ] `async def` handlers only `await` async-safe operations.
- [ ] `def` handlers are used where appropriate; understood that they run in a thread pool.
- [ ] Shared async primitives (locks, queues) are not accidentally used from thread-pool `def` code without thread-safe bridges (prefer keeping such state in async layers).
- [ ] Tests that exercise async routes or clients use async test patterns.

## Related skills

- [fastapi](../../fastapi/SKILL.md)
- [async-python-patterns](../../async-python-patterns/SKILL.md)
- [python-resource-management](../../python-resource-management/SKILL.md) — async context managers, streaming cleanup
- [python-testing-patterns](../../python-testing-patterns/SKILL.md) — pytest structure and fixtures


