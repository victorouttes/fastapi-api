async def init_db():
    from src.models.settings.db_connection_handler import db_connection_handler
    from sqlmodel import SQLModel

    async with db_connection_handler.get_engine().begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
