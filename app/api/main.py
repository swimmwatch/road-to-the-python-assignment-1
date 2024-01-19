import asyncio
import typing
from concurrent.futures.process import ProcessPoolExecutor
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pillow_heif import register_heif_opener

from .routers import router


def make_run_in_process(app: FastAPI) -> typing.Callable:
    async def run_in_process(fn: typing.Callable, *args):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(app.state.executor, fn, *args)

    return run_in_process


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_heif_opener()

    app.state.executor = ProcessPoolExecutor(max_workers=1)
    app.state.run_in_process = make_run_in_process(app)

    yield

    app.state.executor.shutdown()


app = FastAPI(lifespan=lifespan)


app.include_router(router)
