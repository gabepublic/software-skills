---
name: async-python-patterns
description: Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Prefer Asyncer (with FastAPI-aligned projects) or asyncio.to_thread for blocking-from-async bridges. Async HTTP examples use HTTPX (same default as the FastAPI toolchain). Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations.
---

# Async Python Patterns

Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.

**Python version baseline.** FastAPI-aligned projects target **Python 3.12** ([python-code-style](../python-code-style/SKILL.md), [python-type-safety](../python-type-safety/SKILL.md)). Feature-availability notes in this skill (e.g. "`asyncio.to_thread()` — Python 3.9+") are informational for supporting older runtimes; on 3.12 every pattern here works unchanged.

## When to Use This Skill

- Building async web APIs (FastAPI, Sanic, and similar; async HTTP examples use **HTTPX**)
- Implementing concurrent I/O operations (database, file, network)
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSocket servers, chat systems)
- Processing multiple independent tasks simultaneously
- Building microservices with async communication
- Optimizing I/O-bound workloads
- Implementing async background tasks and queues

## Sync vs Async Decision Guide

Before adopting async, consider whether it's the right choice for your use case.

| Use Case | Recommended Approach |
|----------|---------------------|
| Many concurrent network/DB calls | `asyncio` |
| CPU-bound computation | `multiprocessing` or thread pool |
| Mixed I/O + CPU | Offload blocking/sync work: prefer **`asyncer.asyncify`** ([FastAPI other-tools — Asyncer](../fastapi/references/other-tools.md)); otherwise **`asyncio.to_thread()`** (stdlib) |
| Simple scripts, few connections | Sync (simpler, easier to debug) |
| Web APIs with high concurrency | Async frameworks (e.g. FastAPI) + async HTTP client (**HTTPX**) |

**Key Rule:** Stay fully sync or fully async within a call path. Mixing creates hidden blocking and complexity.

**Sync ? async bridging:** When you must call **blocking** code from **`async def`** (or the reverse), the [Official FastAPI skill](../fastapi/SKILL.md) recommends **Asyncer** over ad-hoc **AnyIO** / **asyncio** patterns—see [Asyncer in other-tools](../fastapi/references/other-tools.md). This skill still documents **`asyncio.to_thread`** and **`run_in_executor`** for stdlib-only contexts.

## Core Concepts

### 1. Event Loop

The event loop is the heart of asyncio, managing and scheduling asynchronous tasks.

**Key characteristics:**

- Single-threaded cooperative multitasking
- Schedules coroutines for execution
- Handles I/O operations without blocking
- Manages callbacks and futures

### 2. Coroutines

Functions defined with `async def` that can be paused and resumed.

**Syntax:**

```python
async def my_coroutine():
    result = await some_async_operation()
    return result
```

### 3. Tasks

Scheduled coroutines that run concurrently on the event loop.

### 4. Futures

Low-level objects representing eventual results of async operations.

### 5. Async Context Managers

Resources that support `async with` for proper cleanup.

### 6. Async Iterators

Objects that support `async for` for iterating over async data sources.

## Quick Start

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Python 3.7+ (project baseline is 3.12)
asyncio.run(main())
```

## Fundamental Patterns

### Pattern 1: Basic Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Fetch data from URL asynchronously."""
    await asyncio.sleep(1)  # Simulate I/O
    return {"url": url, "data": "result"}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

### Pattern 2: Concurrent Execution with gather()

```python
import asyncio

async def fetch_user(user_id: int) -> dict:
    """Fetch user data."""
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"User {user_id}"}

async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    user_ids = [1, 2, 3, 4, 5]
    users = await fetch_all_users(user_ids)
    print(f"Fetched {len(users)} users")

asyncio.run(main())
```

### Pattern 3: Task Creation and Management

```python
import asyncio

async def background_task(name: str, delay: int):
    """Long-running background task."""
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} completed")
    return f"Result from {name}"

async def main():
    # Create tasks
    task1 = asyncio.create_task(background_task("Task 1", 2))
    task2 = asyncio.create_task(background_task("Task 2", 1))

    # Do other work
    print("Main: doing other work")
    await asyncio.sleep(0.5)

    # Wait for tasks
    result1 = await task1
    result2 = await task2

    print(f"Results: {result1}, {result2}")

asyncio.run(main())
```

### Pattern 4: Error Handling in Async Code

```python
import asyncio

async def risky_operation(item_id: int) -> dict:
    """Operation that might fail."""
    await asyncio.sleep(0.1)
    if item_id % 3 == 0:
        raise ValueError(f"Item {item_id} failed")
    return {"id": item_id, "status": "success"}

async def safe_operation(item_id: int) -> dict | None:
    """Wrapper with error handling."""
    try:
        return await risky_operation(item_id)
    except ValueError as e:
        print(f"Error: {e}")
        return None

async def process_items(item_ids: list[int]):
    """Process multiple items with error handling."""
    tasks = [safe_operation(iid) for iid in item_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out failures
    successful = [r for r in results if r is not None and not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]

    print(f"Success: {len(successful)}, Failed: {len(failed)}")
    return successful

asyncio.run(process_items([1, 2, 3, 4, 5, 6]))
```

### Pattern 5: Timeout Handling

```python
import asyncio

async def slow_operation(delay: int) -> str:
    """Operation that takes time."""
    await asyncio.sleep(delay)
    return f"Completed after {delay}s"

async def with_timeout():
    """Execute operation with timeout."""
    try:
        result = await asyncio.wait_for(slow_operation(5), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out")

asyncio.run(with_timeout())
```

## Advanced Patterns

### Pattern 6: Async Context Managers

```python
import asyncio

class AsyncDatabaseConnection:
    """Async database connection context manager."""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection: object | None = None

    async def __aenter__(self):
        print("Opening connection")
        await asyncio.sleep(0.1)  # Simulate connection
        self.connection = {"dsn": self.dsn, "connected": True}
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        await asyncio.sleep(0.1)  # Simulate cleanup
        self.connection = None

async def query_database():
    """Use async context manager."""
    async with AsyncDatabaseConnection("postgresql://localhost") as conn:
        print(f"Using connection: {conn}")
        await asyncio.sleep(0.2)  # Simulate query
        return {"rows": 10}

asyncio.run(query_database())
```

### Pattern 7: Async Iterators and Generators

```python
import asyncio
from collections.abc import AsyncIterator

async def async_range(start: int, end: int, delay: float = 0.1) -> AsyncIterator[int]:
    """Async generator that yields numbers with delay."""
    for i in range(start, end):
        await asyncio.sleep(delay)
        yield i

async def fetch_pages(url: str, max_pages: int) -> AsyncIterator[dict]:
    """Fetch paginated data asynchronously."""
    for page in range(1, max_pages + 1):
        await asyncio.sleep(0.2)  # Simulate API call
        yield {
            "page": page,
            "url": f"{url}?page={page}",
            "data": [f"item_{page}_{i}" for i in range(5)]
        }

async def consume_async_iterator():
    """Consume async iterator."""
    async for number in async_range(1, 5):
        print(f"Number: {number}")

    print("\nFetching pages:")
    async for page_data in fetch_pages("https://api.example.com/items", 3):
        print(f"Page {page_data['page']}: {len(page_data['data'])} items")

asyncio.run(consume_async_iterator())
```

### Pattern 8: Producer-Consumer Pattern

```python
import asyncio
from asyncio import Queue

async def producer(queue: Queue, producer_id: int, num_items: int):
    """Produce items and put them in queue."""
    for i in range(num_items):
        item = f"Item-{producer_id}-{i}"
        await queue.put(item)
        print(f"Producer {producer_id} produced: {item}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # Signal completion

async def consumer(queue: Queue, consumer_id: int):
    """Consume items from queue."""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break

        print(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(0.2)  # Simulate work
        queue.task_done()

async def producer_consumer_example():
    """Run producer-consumer pattern."""
    queue = Queue(maxsize=10)

    # Create tasks
    producers = [
        asyncio.create_task(producer(queue, i, 5))
        for i in range(2)
    ]

    consumers = [
        asyncio.create_task(consumer(queue, i))
        for i in range(3)
    ]

    # Wait for producers
    await asyncio.gather(*producers)

    # Wait for queue to be empty
    await queue.join()

    # Cancel consumers
    for c in consumers:
        c.cancel()

asyncio.run(producer_consumer_example())
```

### Pattern 9: Semaphore for Rate Limiting

```python
import asyncio

async def api_call(url: str, semaphore: asyncio.Semaphore) -> dict:
    """Make API call with rate limiting."""
    async with semaphore:
        print(f"Calling {url}")
        await asyncio.sleep(0.5)  # Simulate API call
        return {"url": url, "status": 200}

async def rate_limited_requests(urls: list[str], max_concurrent: int = 5):
    """Make multiple requests with rate limiting."""
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [api_call(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    urls = [f"https://api.example.com/item/{i}" for i in range(20)]
    results = await rate_limited_requests(urls, max_concurrent=3)
    print(f"Completed {len(results)} requests")

asyncio.run(main())
```

### Pattern 10: Async Locks and Synchronization

```python
import asyncio

class AsyncCounter:
    """Thread-safe async counter."""

    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        """Safely increment counter."""
        async with self.lock:
            current = self.value
            await asyncio.sleep(0.01)  # Simulate work
            self.value = current + 1

    async def get_value(self) -> int:
        """Get current value."""
        async with self.lock:
            return self.value

async def worker(counter: AsyncCounter, worker_id: int):
    """Worker that increments counter."""
    for _ in range(10):
        await counter.increment()
        print(f"Worker {worker_id} incremented")

async def test_counter():
    """Test concurrent counter."""
    counter = AsyncCounter()

    workers = [asyncio.create_task(worker(counter, i)) for i in range(5)]
    await asyncio.gather(*workers)

    final_value = await counter.get_value()
    print(f"Final counter value: {final_value}")

asyncio.run(test_counter())
```

## Real-World Applications

**Async HTTP in this skill:** Concurrent HTTP uses **HTTPX** (`httpx.AsyncClient`) so examples match the [FastAPI other-tools reference](../fastapi/references/other-tools.md) and the same default as [python-anti-patterns](../python-anti-patterns/SKILL.md) / [python-testing-patterns](../python-testing-patterns/SKILL.md). Other asyncio HTTP clients are fine where a stack already depends on them; in FastAPI-aligned repos, **default to HTTPX**.

### Concurrent HTTP / web-style fetching with HTTPX

```python
import asyncio

import httpx

async def fetch_url(client: httpx.AsyncClient, url: str) -> dict:
    """Fetch a single URL (scraping, polling, or fan-out style workloads)."""
    try:
        response = await client.get(url, timeout=10.0)
        text = response.text
        return {
            "url": url,
            "status": response.status_code,
            "length": len(text),
        }
    except Exception as e:
        return {"url": url, "error": str(e)}

async def fetch_many_urls(urls: list[str]) -> list[dict]:
    """Run many GETs concurrently over one pooled client."""
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]
        return await asyncio.gather(*tasks)

async def main() -> None:
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/status/404",
    ]

    results = await fetch_many_urls(urls)
    for result in results:
        print(result)

asyncio.run(main())
```

### Async Database Operations

```python
import asyncio

# Simulated async database client
class AsyncDB:
    """Simulated async database."""

    async def execute(self, query: str) -> list[dict]:
        """Execute query."""
        await asyncio.sleep(0.1)
        return [{"id": 1, "name": "Example"}]

    async def fetch_one(self, query: str) -> dict | None:
        """Fetch single row."""
        await asyncio.sleep(0.1)
        return {"id": 1, "name": "Example"}

async def get_user_data(db: AsyncDB, user_id: int) -> dict:
    """Fetch user and related data concurrently."""
    user_task = db.fetch_one(f"SELECT * FROM users WHERE id = {user_id}")
    orders_task = db.execute(f"SELECT * FROM orders WHERE user_id = {user_id}")
    profile_task = db.fetch_one(f"SELECT * FROM profiles WHERE user_id = {user_id}")

    user, orders, profile = await asyncio.gather(user_task, orders_task, profile_task)

    return {
        "user": user,
        "orders": orders,
        "profile": profile
    }

async def main():
    db = AsyncDB()
    user_data = await get_user_data(db, 1)
    print(user_data)

asyncio.run(main())
```

### WebSocket Server

```python
import asyncio

# Simulated WebSocket connection
class WebSocket:
    """Simulated WebSocket."""

    def __init__(self, client_id: str):
        self.client_id = client_id

    async def send(self, message: str):
        """Send message."""
        print(f"Sending to {self.client_id}: {message}")
        await asyncio.sleep(0.01)

    async def recv(self) -> str:
        """Receive message."""
        await asyncio.sleep(1)
        return f"Message from {self.client_id}"

class WebSocketServer:
    """Simple WebSocket server."""

    def __init__(self):
        self.clients: set[WebSocket] = set()

    async def register(self, websocket: WebSocket):
        """Register new client."""
        self.clients.add(websocket)
        print(f"Client {websocket.client_id} connected")

    async def unregister(self, websocket: WebSocket):
        """Unregister client."""
        self.clients.remove(websocket)
        print(f"Client {websocket.client_id} disconnected")

    async def broadcast(self, message: str):
        """Broadcast message to all clients."""
        if self.clients:
            tasks = [client.send(message) for client in self.clients]
            await asyncio.gather(*tasks)

    async def handle_client(self, websocket: WebSocket):
        """Handle individual client connection."""
        await self.register(websocket)
        try:
            async for message in self.message_iterator(websocket):
                await self.broadcast(f"{websocket.client_id}: {message}")
        finally:
            await self.unregister(websocket)

    async def message_iterator(self, websocket: WebSocket):
        """Iterate over messages from client."""
        for _ in range(3):  # Simulate 3 messages
            yield await websocket.recv()
```

## Performance Best Practices

### 1. Use connection limits (pooling) with HTTPX

HTTPX keeps connections alive inside `AsyncClient`; tune **limits** when you open many parallel requests.

```python
import asyncio

import httpx

async def with_connection_pool() -> list[httpx.Response]:
    """Many concurrent requests on one client with bounded pool size."""
    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)

    async with httpx.AsyncClient(limits=limits, timeout=30.0) as client:
        tasks = [client.get(f"https://api.example.com/item/{i}") for i in range(50)]
        return await asyncio.gather(*tasks)
```

### 2. Batch Operations

```python
async def batch_process(items: list[str], batch_size: int = 10):
    """Process items in batches."""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        tasks = [process_item(item) for item in batch]
        await asyncio.gather(*tasks)
        print(f"Processed batch {i // batch_size + 1}")

async def process_item(item: str):
    """Process single item."""
    await asyncio.sleep(0.1)
    return f"Processed: {item}"
```

### 3. Avoid Blocking Operations

Never block the event loop with synchronous operations. A single blocking call stalls all concurrent tasks.

```python
# BAD - blocks the entire event loop
async def fetch_data_bad(url: str) -> None:
    import time
    import requests

    time.sleep(1)  # Blocks!
    _response = requests.get(url, timeout=30)  # Also blocks the loop!

# GOOD - use async-native libraries (e.g., httpx for async HTTP)
import httpx

async def fetch_data_good(url: str):
    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
```

**Preferred (FastAPI toolchain): Asyncer**

[Asyncer](https://asyncer.tiangolo.com/) wraps blocking callables for `await` and is what the [FastAPI other-tools reference](../fastapi/references/other-tools.md) suggests **instead of** reaching for AnyIO or low-level asyncio first. Install with `uv add asyncer` (or your project’s package manager).

```python
from pathlib import Path

from asyncer import asyncify, syncify

def read_text_sync(path: str) -> str:
    """Blocking filesystem read."""
    return Path(path).read_text(encoding="utf-8")

async def read_file_async(path: str) -> str:
    """Await a blocking function without blocking the event loop."""
    return await asyncify(read_text_sync)(path)

async def work() -> str:
    return await read_file_async("config.toml")

def run_from_sync_entrypoint() -> str:
    """Call async code from a synchronous `def` (e.g. legacy callback)."""
    return syncify(work)()
```

Use **`asyncify`** when **`async def`** needs to invoke sync I/O or CPU work; use **`syncify`** when sync code must drive a coroutine (rarer; see the FastAPI `syncify` example in [other-tools](../fastapi/references/other-tools.md)).

**Standard library: `asyncio.to_thread()` (Python 3.9+)**

When Asyncer is not a dependency, offload blocking work to the default thread pool:

```python
import asyncio
from pathlib import Path

async def read_file_async(path: str) -> str:
    """Read file without blocking event loop."""
    # asyncio.to_thread() runs sync code in a thread pool
    return await asyncio.to_thread(Path(path).read_text)

async def call_sync_library(data: dict) -> dict:
    """Wrap a synchronous library call."""
    # Useful for sync database drivers, file I/O, CPU work
    return await asyncio.to_thread(sync_library.process, data)
```

**Lower-level: `run_in_executor()`**

```python
import asyncio
import concurrent.futures
from typing import Any

def blocking_operation(data: Any) -> Any:
    """CPU-intensive blocking operation."""
    import time
    time.sleep(1)
    return data * 2

async def run_in_executor(data: Any) -> Any:
    """Run blocking operation in thread pool."""
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_operation, data)
        return result

async def main():
    results = await asyncio.gather(*[run_in_executor(i) for i in range(5)])
    print(results)

asyncio.run(main())
```

## Common Pitfalls

### 1. Forgetting await

```python
# Wrong - returns coroutine object, doesn't execute
result = async_function()

# Correct
result = await async_function()
```

### 2. Blocking the Event Loop

```python
# Wrong - blocks event loop
import time
async def bad():
    time.sleep(1)  # Blocks!

# Correct
async def good():
    await asyncio.sleep(1)  # Non-blocking
```

### 3. Not Handling Cancellation

```python
async def cancelable_task():
    """Task that handles cancellation."""
    try:
        while True:
            await asyncio.sleep(1)
            print("Working...")
    except asyncio.CancelledError:
        print("Task cancelled, cleaning up...")
        # Perform cleanup
        raise  # Re-raise to propagate cancellation
```

### 4. Mixing Sync and Async Code

```python
# Wrong - can't call async from sync directly
def sync_function():
    result = await async_function()  # SyntaxError!

# Correct
def sync_function():
    result = asyncio.run(async_function())
```

## Testing Async Code

```python
import asyncio
import pytest

# Using pytest-asyncio
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await fetch_data("https://api.example.com")
    assert result is not None

@pytest.mark.asyncio
async def test_with_timeout():
    """Test with timeout."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(5), timeout=1.0)
```
