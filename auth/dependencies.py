"""FastAPI dependencies for authentication."""

from typing import Optional

from fastapi import Header, HTTPException

from auth.firebase import VALID_ROLES, verify_id_token


async def get_current_user(
    authorization: Optional[str] = Header(None),
) -> Optional[dict]:
    """Optional auth — returns user dict or None."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[7:].strip()
    decoded = verify_id_token(token)
    if not decoded:
        return None
    role = (decoded.get("role") or "student").lower()
    return {
        "uid": decoded.get("uid"),
        "email": decoded.get("email"),
        "role": role if role in VALID_ROLES else "student",
    }


async def require_auth(
    authorization: Optional[str] = Header(None),
) -> dict:
    """Require valid Firebase ID token."""
    user = await get_current_user(authorization)
    if not user or not user.get("uid"):
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Sign in with Firebase.",
        )
    return user


async def require_role(*roles: str):
    """Factory for role-restricted endpoints."""

    async def _checker(authorization: Optional[str] = Header(None)) -> dict:
        user = await require_auth(authorization)
        if user["role"] not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Requires one of roles: {', '.join(roles)}",
            )
        return user

    return _checker
