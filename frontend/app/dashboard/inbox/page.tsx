"use client";

import { useEffect, useState } from "react";
import { Send, XCircle } from "lucide-react";
import { apiRequest } from "@/lib/api";
import type { Conversation, Message } from "@/lib/types";
import { Button, GhostButton, Panel, Textarea } from "@/components/ui";

export default function InboxPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [active, setActive] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [content, setContent] = useState("");

  async function loadConversations() {
    const rows = await apiRequest<Conversation[]>("/conversations").catch(() => []);
    setConversations(rows);
    if (!active && rows[0]) setActive(rows[0]);
  }

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (!active) return;
    apiRequest<Message[]>(`/conversations/${active.id}/messages`).then(setMessages).catch(() => setMessages([]));
  }, [active]);

  async function sendMessage(event: React.FormEvent) {
    event.preventDefault();
    if (!active || !content.trim()) return;
    const message = await apiRequest<Message>(`/conversations/${active.id}/messages`, {
      method: "POST",
      body: JSON.stringify({ content })
    });
    setMessages((prev) => [...prev, message]);
    setContent("");
  }

  async function closeConversation() {
    if (!active) return;
    await apiRequest<Conversation>(`/conversations/${active.id}/close`, { method: "POST" });
    loadConversations();
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold text-brand">Inbox</p>
        <h1 className="text-3xl font-bold">会话收件箱</h1>
      </div>
      <div className="grid gap-4 lg:grid-cols-[360px_1fr]">
        <Panel className="p-0">
          <div className="border-b border-line p-4 font-bold">会话列表</div>
          <div className="max-h-[680px] overflow-y-auto">
            {conversations.map((conversation) => (
              <button
                key={conversation.id}
                onClick={() => setActive(conversation)}
                className={`block w-full border-b border-line p-4 text-left text-sm transition hover:bg-mist ${
                  active?.id === conversation.id ? "bg-blue-50" : "bg-white"
                }`}
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="font-bold">#{conversation.id.slice(0, 8)}</span>
                  <span className="rounded-md bg-mist px-2 py-1 text-xs font-bold">{conversation.status}</span>
                </div>
                <p className="mt-2 text-slate-500">{conversation.last_message_at ? new Date(conversation.last_message_at).toLocaleString() : "新会话"}</p>
              </button>
            ))}
            {!conversations.length ? <p className="p-4 text-sm text-slate-500">还没有会话。</p> : null}
          </div>
        </Panel>
        <Panel className="flex min-h-[680px] flex-col p-0">
          <div className="flex items-center justify-between border-b border-line p-4">
            <div>
              <p className="font-bold">{active ? `会话 ${active.id.slice(0, 8)}` : "选择会话"}</p>
              <p className="text-sm text-slate-500">{active?.status || "等待消息"}</p>
            </div>
            <GhostButton onClick={closeConversation} disabled={!active}>
              <XCircle size={16} />
              关闭
            </GhostButton>
          </div>
          <div className="flex-1 space-y-3 overflow-y-auto bg-mist p-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`max-w-[78%] rounded-md p-3 text-sm ${
                  message.sender_type === "agent" ? "ml-auto bg-brand text-white" : "bg-white text-ink"
                }`}
              >
                <p className="text-xs font-bold opacity-70">{message.sender_type}</p>
                <p className="mt-1 whitespace-pre-wrap">{message.content}</p>
              </div>
            ))}
            {!messages.length ? <p className="text-sm text-slate-500">暂无消息。</p> : null}
          </div>
          <form onSubmit={sendMessage} className="border-t border-line bg-white p-4">
            <Textarea value={content} onChange={(event) => setContent(event.target.value)} placeholder="输入客服回复..." />
            <div className="mt-3 flex justify-end">
              <Button disabled={!active}>
                <Send size={16} />
                发送
              </Button>
            </div>
          </form>
        </Panel>
      </div>
    </div>
  );
}
