from sqlalchemy import select
from sqlalchemy.orm import Session
import httpx

from app.core.config import settings
from app.models.knowledge import KnowledgeBase
from app.models.site import Site

SYSTEM_PROMPT = """你是该网站的在线客服。
你只能根据商家提供的知识库回答问题。
如果知识库没有答案，不要编造。
如果无法确定答案，请引导访客留下联系方式。
回复要简短、友好、自然。
你的目标是帮助商家获得有效客户线索。"""


def build_knowledge_context(db: Session, site: Site) -> str:
    entries = db.scalars(
        select(KnowledgeBase)
        .where(KnowledgeBase.site_id == site.id, KnowledgeBase.is_active.is_(True))
        .order_by(KnowledgeBase.updated_at.desc())
        .limit(20)
    ).all()
    if not entries:
        return "当前商家还没有配置知识库。"
    return "\n\n".join(f"标题：{entry.title}\n内容：{entry.content}" for entry in entries)


async def generate_ai_reply(db: Session, site: Site, user_message: str) -> str:
    knowledge_context = build_knowledge_context(db, site)
    if not settings.openai_api_key:
        return "我暂时无法确认答案，请留下您的联系方式，稍后我们会安排客服回复您。"

    endpoint = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\n商家知识库：\n{knowledge_context}"},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.2,
    }
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError:
        return "我现在连接知识库助手失败了，请留下联系方式，客服会尽快回复您。"

    content = data.get("choices", [{}])[0].get("message", {}).get("content")
    if not content:
        return "我暂时无法确认答案，请留下您的联系方式，稍后我们会安排客服回复您。"
    return content.strip()
