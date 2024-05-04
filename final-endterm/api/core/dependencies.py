from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from .security import get_user_from_token
from .services.kwargs_searchers import get_region_by_kwargs
from database.models import Region

bearer = HTTPBearer(
    bearerFormat="JWT",
    scheme_name="JWTAuthentication",
    description="Value should be formatted: `<key>`. Without prefix",
)


async def jwt_authentication(
        auth: HTTPAuthorizationCredentials = Depends(bearer),
):
    token = auth.credentials
    user = get_user_from_token(token)
    return user


async def get_region_by_name(region_name: str) -> Region:
    kwargs = {"name": region_name}
    return await get_region_by_kwargs(**kwargs)


class RegionDependency:
    async def __call__(self, region_id: int) -> Region:
        kwargs = {"id": region_id}
        return await get_region_by_kwargs(**kwargs)
