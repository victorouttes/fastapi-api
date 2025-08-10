from contextlib import asynccontextmanager

import fastapi
import uvicorn

from src.models.settings.db_init import init_db
from src.routes.book_routes import book_router


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    await init_db()
    yield

app = fastapi.FastAPI(lifespan=lifespan)

app.include_router(book_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
