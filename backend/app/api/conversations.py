from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_workspace
from app.models.conversation import Conversation
from app.models.site import Site
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.conversation import AssignConversationRequest, ConversationRead, ConversationWithMessages

router = APIRouter()


def get_workspace_conversation(db: Session, workspace: Workspace, conversation_id: UUID) -> Conversation:
    conversation = db.scalar(
        select(Conversation)
        .join(Site)
        .options(selectinload(Conversation.messages))
        .where(Conversation.id == conversation_id, Site.workspace_id == workspace.id)
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.get("", response_model=list[ConversationRead])
def list_conversations(
    site_id: UUID | None = None,
    status: str | None = None,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> list[Conversation]:
    query = select(Conversation).join(Site).where(Site.workspace_id == workspace.id)
    if site_id:
        query = query.where(Conversation.site_id == site_id)
    if status:
        query = query.where(Conversation.status == status)
    return list(db.scalars(query.order_by(Conversation.last_message_at.desc().nullslast()).limit(200)).all())


@router.get("/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Conversation:
    return get_workspace_conversation(db, workspace, conversation_id)


@router.post("/{conversation_id}/assign", response_model=ConversationRead)
def assign_conversation(
    conversation_id: UUID,
    payload: AssignConversationRequest,
    current_user: User = Depends(get_current_user),
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Conversation:
    conversation = get_workspace_conversation(db, workspace, conversation_id)
    conversation.assigned_agent_id = payload.agent_id or current_user.id
    conversation.status = "open"
    db.commit()
    return conversation


@router.post("/{conversation_id}/close", response_model=ConversationRead)
def close_conversation(
    conversation_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Conversation:
    conversation = get_workspace_conversation(db, workspace, conversation_id)
    conversation.status = "closed"
    conversation.closed_at = datetime.now(timezone.utc)
    db.commit()
    return conversation
