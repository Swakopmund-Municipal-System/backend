from fastapi import Header, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from app.models.dto.models import AuthenticatedUserDTO

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

bearer_scheme = HTTPBearer()

RESOURCE_NAME = "activities-services"


async def check_user_permission(
    user_token: str, api_key: str, resource: str, sub_resource: str
):
    headers = {
        "Authorization": f"Token {user_token}",
        "x-api-key": api_key,
        "x-resource": resource,
        "x-sub-resource": sub_resource,
    }

    url = f"{AUTH_SERVICE_URL}/api/auth/user/check-user-permission/"

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

    url = f"{AUTH_SERVICE_URL}/api/auth/application/check_application_permission/"

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


def get_auth_headers(resource: str, sub_resource: str, method: str):
    def dependency():
        return {
            "X-RESOURCE": resource,
            "X-SUB-RESOURCE": sub_resource,
            "X-METHOD": method,
        }

    return dependency


def authenticate_request(_resource: str, _sub_resource: str, _method: str):
    async def dependency(
        request: Request, override_value: dict = Depends(authentication_override)
    ):
        if override_value is not None:
            return override_value

        api_key = request.headers.get("x-api-key")
        user_token = extract_user_token(request)
        resource = _resource
        sub_resource = _sub_resource

        print(f"API Key: {api_key}")
        print(f"User Token: {user_token}")
        print(f"Resource: {resource}")
        print(f"Sub Resource: {sub_resource}")

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

    return dependency


def authenticate_request_with_user(_resource: str, _sub_resource: str, _method: str):
    async def dependency(
        auth_data: dict = Depends(
            authenticate_request(_resource, _sub_resource, _method)
        ),
    ):
        if not auth_data.get("user") or not auth_data.get("user").get("user"):
            raise HTTPException(status_code=401, detail="User authentication required")

        if not auth_data["user"].get("status") == "authorised":
            raise HTTPException(status_code=401, detail="User authentication required")

        if not auth_data["user"]["user"]["id"] or auth_data["user"]["user"]["id"] == 0:
            raise HTTPException(status_code=401, detail="User authentication required")

        return auth_data

    return dependency


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
                f"{AUTH_SERVICE_URL}/api/auth/user/info",
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


def authentication_override():
    return None
