from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from .security import get_user_from_token

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
