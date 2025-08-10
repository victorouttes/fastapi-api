from contextlib import asynccontextmanager

import fastapi
import uvicorn
from loguru import logger

from src.models.settings.db_init import init_db
from src.routes.book_routes import book_router
from src.routes.user_routes import user_router


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    await init_db()
    yield

app = fastapi.FastAPI(lifespan=lifespan, title="Template REST API", version="1.0.0")

app.include_router(book_router)
app.include_router(user_router)

if __name__ == '__main__':
    logger.info("Starting server...")
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
