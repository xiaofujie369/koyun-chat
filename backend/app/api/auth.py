from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember
from app.schemas.auth import LoginRequest, MeResponse, RegisterRequest, TokenResponse
from app.services.billing_service import create_trial_subscription, ensure_default_plans

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    ensure_default_plans(db)
    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        name=payload.name,
        is_active=True,
    )
    db.add(user)
    db.flush()

    workspace = Workspace(
        name=payload.workspace_name or f"{payload.name}'s Workspace",
        owner_user_id=user.id,
    )
    db.add(workspace)
    db.flush()

    db.add(WorkspaceMember(workspace_id=workspace.id, user_id=user.id, role="owner"))
    create_trial_subscription(db, workspace)
    db.commit()

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, user=user, workspace_id=workspace.id)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is disabled")

    user.last_login_at = datetime.now(timezone.utc)
    membership = db.scalar(select(WorkspaceMember).where(WorkspaceMember.user_id == user.id))
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    db.commit()
    return TokenResponse(access_token=create_access_token(user.id), user=user, workspace_id=membership.workspace_id)


@router.get("/me", response_model=MeResponse)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> MeResponse:
    membership = db.scalar(select(WorkspaceMember).where(WorkspaceMember.user_id == current_user.id))
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    workspace = db.get(Workspace, membership.workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return MeResponse(
        user=current_user,
        workspace_id=workspace.id,
        workspace_name=workspace.name,
        role=membership.role,
    )


@router.post("/logout")
def logout() -> dict[str, str]:
    return {"message": "Logged out"}
