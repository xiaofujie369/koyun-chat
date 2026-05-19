"use client";

import { useEffect, useState } from "react";
import { BookPlus, Trash2 } from "lucide-react";
import { apiRequest } from "@/lib/api";
import type { Knowledge, Site } from "@/lib/types";
import { Button, GhostButton, Input, Panel, Textarea } from "@/components/ui";

export default function KnowledgePage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [items, setItems] = useState<Knowledge[]>([]);
  const [form, setForm] = useState({ site_id: "", title: "", category: "", content: "" });

  async function load() {
    const [siteRows, knowledgeRows] = await Promise.all([
      apiRequest<Site[]>("/sites").catch(() => []),
      apiRequest<Knowledge[]>("/knowledge").catch(() => [])
    ]);
    setSites(siteRows);
    setItems(knowledgeRows);
    if (!form.site_id && siteRows[0]) setForm((prev) => ({ ...prev, site_id: siteRows[0].id }));
  }

  useEffect(() => {
    load();
  }, []);

  async function createItem(event: React.FormEvent) {
    event.preventDefault();
    if (!form.site_id) return;
    await apiRequest<Knowledge>("/knowledge", {
      method: "POST",
      body: JSON.stringify({ ...form, is_active: true })
    });
    setForm({ ...form, title: "", category: "", content: "" });
    load();
  }

  async function removeItem(id: string) {
    await apiRequest<void>(`/knowledge/${id}`, { method: "DELETE" });
    load();
  }

  async function toggleItem(item: Knowledge) {
    await apiRequest<Knowledge>(`/knowledge/${item.id}`, {
      method: "PUT",
      body: JSON.stringify({ is_active: !item.is_active })
    });
    load();
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold text-brand">Knowledge</p>
        <h1 className="text-3xl font-bold">知识库</h1>
      </div>
      <Panel>
        <form onSubmit={createItem} className="grid gap-3">
          <select className="h-10 rounded-md border border-line bg-white px-3 text-sm" value={form.site_id} onChange={(event) => setForm({ ...form, site_id: event.target.value })}>
            {sites.map((site) => <option key={site.id} value={site.id}>{site.name}</option>)}
          </select>
          <div className="grid gap-3 md:grid-cols-2">
            <Input placeholder="标题" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} required />
            <Input placeholder="分类" value={form.category} onChange={(event) => setForm({ ...form, category: event.target.value })} />
          </div>
          <Textarea placeholder="知识内容" value={form.content} onChange={(event) => setForm({ ...form, content: event.target.value })} required />
          <Button className="w-fit">
            <BookPlus size={17} />
            新增知识
          </Button>
        </form>
      </Panel>
      <div className="grid gap-4 md:grid-cols-2">
        {items.map((item) => (
          <Panel key={item.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="font-bold">{item.title}</h2>
                <p className="text-sm text-slate-500">{item.category || "未分类"} · {item.is_active ? "启用" : "停用"}</p>
              </div>
              <div className="flex gap-2">
                <GhostButton onClick={() => toggleItem(item)}>{item.is_active ? "停用" : "启用"}</GhostButton>
                <GhostButton onClick={() => removeItem(item.id)} aria-label="删除知识">
                  <Trash2 size={16} />
                </GhostButton>
              </div>
            </div>
            <p className="mt-4 line-clamp-5 whitespace-pre-wrap text-sm leading-6 text-slate-600">{item.content}</p>
          </Panel>
        ))}
      </div>
    </div>
  );
}
