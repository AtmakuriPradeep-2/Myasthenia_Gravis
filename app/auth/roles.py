from typing import List
from fastapi import Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.models.user import User


def get_normalized_role(user: User) -> str:
    return (user.role or "").strip().capitalize()


def require_admin(
    current_user: User = Depends(get_current_user)
):
    if get_normalized_role(current_user) != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


def require_clinician(
    current_user: User = Depends(get_current_user)
):
    if get_normalized_role(current_user) not in ["Admin", "Clinician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clinician privileges required"
        )
    return current_user


def require_researcher(
    current_user: User = Depends(get_current_user)
):
    if get_normalized_role(current_user) not in ["Admin", "Researcher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Researcher privileges required"
        )
    return current_user


def require_read_access(
    current_user: User = Depends(get_current_user)
):
    # Admin, Clinician, and Researcher all have permission to view patient data & clinical records
    if get_normalized_role(current_user) not in ["Admin", "Clinician", "Researcher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to access clinical records"
        )
    return current_user


def require_roles(allowed_roles: List[str]):
    normalized_allowed = [r.strip().capitalize() for r in allowed_roles]

    def role_checker(current_user: User = Depends(get_current_user)):
        if get_normalized_role(current_user) not in normalized_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Allowed roles: {', '.join(normalized_allowed)}"
            )
        return current_user

    return role_checker
 