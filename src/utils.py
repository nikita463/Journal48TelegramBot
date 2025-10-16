import asyncio
from datetime import datetime

async def run_at(run_time: datetime, coro, *args, **kwargs):
    now = datetime.now()
    delay = (run_time - now).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)
    try:
        return await coro(*args, **kwargs)
    except Exception as exp:
        print("[ERROR] run_every()" + str(exp))
        return None

async def run_every(interval: float, coro, *args, **kwargs):
    while True:
        try:
            await coro(*args, **kwargs)
        except Exception as exp:
            print("[ERROR] run_every()" + str(exp))
        await asyncio.sleep(interval)
