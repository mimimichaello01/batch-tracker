from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

import os
from dotenv import load_dotenv

from settings.config import DATABASE_URL

load_dotenv()



engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    session: AsyncSession = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
