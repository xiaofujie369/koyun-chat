from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.lead import Lead
from app.models.message import Message
from app.models.site import Site
from app.models.user import User
from app.models.visitor import Visitor
from app.models.workspace import Workspace
from app.services.ai_service import generate_ai_reply
from app.services.usage_service import assert_can_use_ai, increment_usage
from app.websocket.manager import manager

OPEN_CONVERSATION_STATUSES = ("open", "pending", "ai", "offline")


def get_or_create_open_conversation(db: Session, site: Site, visitor: Visitor) -> Conversation:
    conversation = db.scalar(
        select(Conversation)
        .where(
            Conversation.site_id == site.id,
            Conversation.visitor_id == visitor.id,
            Conversation.status.in_(OPEN_CONVERSATION_STATUSES),
        )
        .order_by(Conversation.last_message_at.desc().nullslast(), Conversation.created_at.desc())
    )
    if conversation:
        return conversation
    conversation = Conversation(
        site_id=site.id,
        visitor_id=visitor.id,
        status="ai" if site.ai_enabled else "open",
        channel="widget",
        last_message_at=datetime.now(timezone.utc),
    )
    db.add(conversation)
    db.flush()
    return conversation


def create_lead_from_payload(
    db: Session,
    site: Site,
    visitor: Visitor,
    conversation: Conversation,
    source_url: str | None,
    lead_payload: dict[str, Any] | None,
) -> Lead | None:
    if not lead_payload:
        return None
    useful_keys = ("name", "email", "phone", "telegram", "whatsapp", "message")
    if not any(lead_payload.get(key) for key in useful_keys):
        return None
    lead = Lead(
        site_id=site.id,
        visitor_id=visitor.id,
        conversation_id=conversation.id,
        name=lead_payload.get("name"),
        email=lead_payload.get("email"),
        phone=lead_payload.get("phone"),
        telegram=lead_payload.get("telegram"),
        whatsapp=lead_payload.get("whatsapp"),
        message=lead_payload.get("message"),
        source_url=source_url,
        status="new",
    )
    db.add(lead)
    db.flush()
    return lead


async def handle_visitor_message(
    db: Session,
    workspace: Workspace,
    site: Site,
    visitor: Visitor,
    content: str,
    source_url: str | None = None,
    lead_payload: dict[str, Any] | None = None,
) -> tuple[Conversation, list[Message]]:
    conversation = get_or_create_open_conversation(db, site, visitor)
    now = datetime.now(timezone.utc)
    visitor_message = Message(
        conversation_id=conversation.id,
        sender_type="visitor",
        content=content,
        meta={"source_url": source_url} if source_url else {},
    )
    conversation.last_message_at = now
    db.add(visitor_message)
    create_lead_from_payload(db, site, visitor, conversation, source_url, lead_payload)
    increment_usage(db, workspace.id, "message", site_id=site.id)
    db.flush()

    await manager.broadcast_dashboard(
        site.id,
        {
            "type": "visitor_message",
            "conversation_id": str(conversation.id),
            "visitor_uid": visitor.visitor_uid,
            "content": content,
            "created_at": visitor_message.created_at.isoformat() if visitor_message.created_at else None,
        },
    )

    messages = [visitor_message]
    if site.ai_enabled and conversation.assigned_agent_id is None:
        assert_can_use_ai(db, workspace)
        ai_content = await generate_ai_reply(db, site, content)
        ai_message = Message(
            conversation_id=conversation.id,
            sender_type="ai",
            content=ai_content,
            meta={"model": "openai-compatible"},
        )
        conversation.status = "ai"
        conversation.last_message_at = datetime.now(timezone.utc)
        db.add(ai_message)
        increment_usage(db, workspace.id, "ai_message", site_id=site.id)
        db.flush()
        messages.append(ai_message)

        payload = {
            "type": "message",
            "conversation_id": str(conversation.id),
            "sender_type": "ai",
            "content": ai_content,
            "created_at": ai_message.created_at.isoformat() if ai_message.created_at else None,
        }
        await manager.send_to_visitor(site.site_key, visitor.visitor_uid, payload)
        await manager.broadcast_dashboard(site.id, payload)

    db.commit()
    return conversation, messages


async def create_agent_message(
    db: Session,
    conversation: Conversation,
    sender_user: User,
    content: str,
) -> Message:
    if conversation.status == "closed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Conversation is closed")
    message = Message(
        conversation_id=conversation.id,
        sender_type="agent",
        sender_user_id=sender_user.id,
        content=content,
        meta={},
    )
    conversation.assigned_agent_id = conversation.assigned_agent_id or sender_user.id
    conversation.status = "open"
    conversation.last_message_at = datetime.now(timezone.utc)
    db.add(message)
    increment_usage(db, conversation.site.workspace_id, "message", site_id=conversation.site_id)
    db.flush()
    await manager.send_to_visitor(
        conversation.site.site_key,
        conversation.visitor.visitor_uid,
        {
            "type": "message",
            "conversation_id": str(conversation.id),
            "sender_type": "agent",
            "content": content,
            "created_at": message.created_at.isoformat() if message.created_at else None,
        },
    )
    await manager.broadcast_dashboard(
        conversation.site_id,
        {
            "type": "agent_message",
            "conversation_id": str(conversation.id),
            "sender_type": "agent",
            "content": content,
        },
    )
    db.commit()
    return message
