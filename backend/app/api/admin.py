from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_platform_admin
from app.models.site import Site
from app.models.subscription import Subscription
from app.models.user import User
from app.models.workspace import Workspace

router = APIRouter(dependencies=[Depends(require_platform_admin)])


@router.get("/stats")
def stats(db: Session = Depends(get_db)) -> dict[str, int]:
    return {
        "users": int(db.scalar(select(func.count(User.id))) or 0),
        "workspaces": int(db.scalar(select(func.count(Workspace.id))) or 0),
        "sites": int(db.scalar(select(func.count(Site.id))) or 0),
        "subscriptions": int(db.scalar(select(func.count(Subscription.id))) or 0),
    }


@router.get("/users")
def users(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(User).order_by(User.created_at.desc()).limit(200)).all()
    return [{"id": str(user.id), "email": user.email, "name": user.name, "created_at": user.created_at} for user in rows]


@router.get("/workspaces")
def workspaces(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(Workspace).order_by(Workspace.created_at.desc()).limit(200)).all()
    return [{"id": str(item.id), "name": item.name, "owner_user_id": str(item.owner_user_id)} for item in rows]


@router.get("/sites")
def sites(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(Site).order_by(Site.created_at.desc()).limit(200)).all()
    return [{"id": str(site.id), "name": site.name, "site_key": site.site_key, "status": site.status} for site in rows]


@router.get("/subscriptions")
def subscriptions(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(Subscription).order_by(Subscription.created_at.desc()).limit(200)).all()
    return [
        {
            "id": str(item.id),
            "workspace_id": str(item.workspace_id),
            "plan_id": str(item.plan_id),
            "status": item.status,
        }
        for item in rows
    ]
