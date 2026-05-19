"use client";

import { useEffect, useState } from "react";
import { Bot, Inbox, Radio, UsersRound } from "lucide-react";
import { apiRequest } from "@/lib/api";
import type { Conversation, Lead, Visitor } from "@/lib/types";
import { Panel, StatCard } from "@/components/ui";

export default function DashboardPage() {
  const [visitors, setVisitors] = useState<Visitor[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);

  useEffect(() => {
    Promise.all([
      apiRequest<Visitor[]>("/visitors").catch(() => []),
      apiRequest<Conversation[]>("/conversations").catch(() => []),
      apiRequest<Lead[]>("/leads").catch(() => [])
    ]).then(([visitorRows, conversationRows, leadRows]) => {
      setVisitors(visitorRows);
      setConversations(conversationRows);
      setLeads(leadRows);
    });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold text-brand">Dashboard</p>
        <h1 className="text-3xl font-bold">工作台概览</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <StatCard label="今日访客数" value={String(visitors.length)} />
        <StatCard label="在线访客数" value={String(visitors.filter((item) => item.is_online).length)} tone="text-leaf" />
        <StatCard label="今日会话数" value={String(conversations.length)} />
        <StatCard label="新线索数" value={String(leads.filter((item) => item.status === "new").length)} tone="text-sun" />
        <StatCard label="AI 消息用量" value="按套餐统计" />
      </div>
      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <Panel>
          <div className="flex items-center gap-2">
            <Inbox size={18} className="text-brand" />
            <h2 className="font-bold">最近会话</h2>
          </div>
          <div className="mt-4 divide-y divide-line">
            {conversations.slice(0, 8).map((conversation) => (
              <div key={conversation.id} className="flex items-center justify-between py-3 text-sm">
                <div>
                  <p className="font-semibold">Conversation {conversation.id.slice(0, 8)}</p>
                  <p className="text-slate-500">{conversation.channel} · {conversation.status}</p>
                </div>
                <span className="rounded-md bg-mist px-2 py-1 text-xs font-bold text-slate-600">
                  {conversation.last_message_at ? new Date(conversation.last_message_at).toLocaleString() : "new"}
                </span>
              </div>
            ))}
            {!conversations.length ? <p className="py-8 text-sm text-slate-500">还没有会话。</p> : null}
          </div>
        </Panel>
        <Panel>
          <h2 className="font-bold">运营状态</h2>
          <div className="mt-4 grid gap-3">
            {[
              { icon: Radio, title: "访客在线状态", text: "WebSocket 已支持实时更新" },
              { icon: Bot, title: "AI 接待", text: "基于知识库自动回复" },
              { icon: UsersRound, title: "线索收集", text: "离线和不确定答案时引导留资" }
            ].map((item) => {
              const TypedIcon = item.icon;
              return (
                <div key={item.title} className="flex gap-3 rounded-md border border-line p-3">
                  <TypedIcon size={18} className="mt-1 text-brand" />
                  <div>
                    <p className="text-sm font-bold">{item.title}</p>
                    <p className="text-sm text-slate-500">{item.text}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </Panel>
      </div>
    </div>
  );
}
