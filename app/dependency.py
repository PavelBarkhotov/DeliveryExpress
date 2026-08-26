import secrets
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from app.db.session import session_factory


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


async def get_user_session(request: Request, response: Response) -> str:
    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = secrets.token_urlsafe(24)
        response.set_cookie(
            key="session_id", value=session_id, httponly=True, samesite="lax"
        )

    return session_id
