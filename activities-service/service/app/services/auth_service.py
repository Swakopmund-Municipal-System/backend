from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from app.models.dto.models import AuthenticatedUserDTO

AUTH_SERVER_URL = os.getenv("AUTH_SERVER_URL")

bearer_scheme = HTTPBearer()


async def check_user_permission(
    user_token: str, api_key: str, resource: str, sub_resource: str
):
    headers = {
        "Authorization": f"Token {user_token}",
        "x-api-key": api_key,
        "x-resource": resource,
        "x-sub-resource": sub_resource,
    }

    url = f"{AUTH_SERVER_URL}/api/auth/user/check-user-permission/"

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.post(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=response.json().get("error", "Permission denied"),
            )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=response.json().get("error", "Authentication failed"),
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Auth service timeout"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=f"Auth service error: {str(e)}"
        )


async def check_application_permission(api_key: str, resource: str):
    headers = {"x-api-key": api_key, "x-resource": resource}

    url = f"{AUTH_SERVER_URL}/api/auth/application/check_application_permission/"

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.post(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=response.json().get("error", "Application permission denied"),
            )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=response.json().get(
                    "error", "Application authentication failed"
                ),
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Auth service timeout"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=f"Auth service error: {str(e)}"
        )


async def authenticate_request(request: Request):
    api_key = request.headers.get("x-api-key")
    user_token = extract_user_token(request)
    resource = request.headers.get("x-resource")
    sub_resource = request.headers.get("x-sub-resource")

    app_auth = None
    user_auth = None

    if api_key and resource:
        try:
            app_auth = await check_application_permission(api_key, resource)
        except HTTPException:
            if not user_token:
                raise

    if user_token and resource and sub_resource:
        try:
            user_auth = await check_user_permission(
                user_token, api_key, resource, sub_resource
            )
        except HTTPException:
            if not app_auth:
                raise

    if not app_auth and not user_auth:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return {"app": app_auth, "user": user_auth}


def extract_user_token(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "token":
        return parts[1]
    return None


async def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> AuthenticatedUserDTO:
    token = credentials.credentials
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVER_URL}/api/auth/user/info",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0,
            )

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_data = response.json()

        return AuthenticatedUserDTO(
            id=user_data["id"],
            email=user_data["email"],
            is_staff=user_data.get("is_staff", False),
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail="Auth server unreachable")
