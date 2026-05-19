from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.models.conversation import Conversation
from app.models.site import Site
from app.models.user import User
from app.models.visitor import Visitor
from app.models.workspace import Workspace, WorkspaceMember
from app.services.chat_service import create_agent_message, handle_visitor_message
from app.services.visitor_service import upsert_visitor
from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/widget/{site_key}/{visitor_uid}")
async def visitor_socket(websocket: WebSocket, site_key: str, visitor_uid: str) -> None:
    db = SessionLocal()
    site = db.scalar(select(Site).where(Site.site_key == site_key, Site.status == "active"))
    if not site:
        await websocket.close(code=4404)
        db.close()
        return
    workspace = db.get(Workspace, site.workspace_id)
    visitor = upsert_visitor(
        db,
        site=site,
        workspace=workspace,
        visitor_uid=visitor_uid,
        ip_address=websocket.client.host if websocket.client else None,
        user_agent=websocket.headers.get("user-agent"),
        is_online=True,
    )
    db.commit()
    await manager.connect_visitor(site_key, visitor_uid, websocket)
    await manager.broadcast_dashboard(site.id, {"type": "visitor_online", "visitor_uid": visitor_uid})
    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            if message_type == "ping":
                visitor.last_seen_at = datetime.now(timezone.utc)
                db.commit()
                await websocket.send_json({"type": "pong"})
            elif message_type == "message" and data.get("content"):
                await handle_visitor_message(db, workspace, site, visitor, data["content"], data.get("source_url"))
    except WebSocketDisconnect:
        manager.disconnect_visitor(site_key, visitor_uid, websocket)
        visitor.is_online = False
        db.commit()
        await manager.broadcast_dashboard(site.id, {"type": "visitor_offline", "visitor_uid": visitor_uid})
    finally:
        db.close()


@router.websocket("/ws/dashboard/{site_id}")
async def dashboard_socket(websocket: WebSocket, site_id: UUID) -> None:
    token = websocket.query_params.get("token")
    subject = decode_access_token(token) if token else None
    db = SessionLocal()
    user = db.get(User, UUID(subject)) if subject else None
    site = db.get(Site, site_id)
    membership = (
        db.scalar(
            select(WorkspaceMember).where(
                WorkspaceMember.user_id == user.id,
                WorkspaceMember.workspace_id == site.workspace_id,
            )
        )
        if user and site
        else None
    )
    if not user or not site or not membership:
        await websocket.close(code=4401)
        db.close()
        return

    await manager.connect_dashboard(site_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif data.get("type") == "agent_message" and data.get("conversation_id") and data.get("content"):
                conversation = db.scalar(
                    select(Conversation).where(
                        Conversation.id == UUID(data["conversation_id"]),
                        Conversation.site_id == site_id,
                    )
                )
                if conversation:
                    await create_agent_message(db, conversation, user, data["content"])
    except WebSocketDisconnect:
        manager.disconnect_dashboard(site_id, websocket)
    finally:
        db.close()
