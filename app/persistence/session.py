from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    future=True,
    # echo=True,,
)
async_session = async_sessionmaker(bind=engine, expire_on_commit=True)


async def get_session():
    async with async_session() as session:
        yield session
