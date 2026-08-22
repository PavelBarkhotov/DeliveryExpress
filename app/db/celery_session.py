from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings


celery_engine = create_async_engine(settings.database_url, poolclass=NullPool)

celery_session_factory = async_sessionmaker(celery_engine, expire_on_commit=False)
