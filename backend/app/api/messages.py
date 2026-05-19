from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_workspace
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.site import Site
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.message import MessageCreate, MessageRead
from app.services.chat_service import create_agent_message

router = APIRouter()


def get_scoped_conversation(db: Session, workspace: Workspace, conversation_id: UUID) -> Conversation:
    conversation = db.scalar(
        select(Conversation).join(Site).where(Conversation.id == conversation_id, Site.workspace_id == workspace.id)
    )
    if not conversation:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.get("/{conversation_id}/messages", response_model=list[MessageRead])
def list_messages(
    conversation_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> list[Message]:
    conversation = get_scoped_conversation(db, workspace, conversation_id)
    return list(db.scalars(select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc())).all())


@router.post("/{conversation_id}/messages", response_model=MessageRead)
async def send_agent_message(
    conversation_id: UUID,
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Message:
    conversation = get_scoped_conversation(db, workspace, conversation_id)
    return await create_agent_message(db, conversation, current_user, payload.content)
