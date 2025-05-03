from asyncio import Semaphore, gather
from typing import Any, Awaitable


async def run_with_semaphore(semaphore: Semaphore, coro: Awaitable) -> Any:
    async with semaphore:
        return await coro


async def safe_gather(
    *coros_or_futures: Awaitable,
    parallelism_size: int = 10,
    return_exceptions: bool = False,
) -> list[Any | BaseException]:
    semaphore = Semaphore(value=parallelism_size)
    coroutines = [run_with_semaphore(semaphore, task) for task in coros_or_futures]
    return await gather(*coroutines, return_exceptions=return_exceptions)
