"use client";

import { useEffect, useState } from "react";
import { Clipboard, Globe2, Plus } from "lucide-react";
import { apiRequest } from "@/lib/api";
import type { Site } from "@/lib/types";
import { Button, GhostButton, Input, Panel } from "@/components/ui";

export default function SitesPage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [name, setName] = useState("");
  const [domain, setDomain] = useState("");
  const [embedCodes, setEmbedCodes] = useState<Record<string, string>>({});
  const [error, setError] = useState("");

  async function load() {
    setSites(await apiRequest<Site[]>("/sites").catch(() => []));
  }

  useEffect(() => {
    load();
  }, []);

  async function createSite(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    try {
      await apiRequest<Site>("/sites", {
        method: "POST",
        body: JSON.stringify({
          name,
          domain,
          allowed_domains: domain ? [domain] : [],
          widget_color: "#2563eb",
          widget_position: "bottom-right",
          welcome_message: "您好，我是在线客服，有什么可以帮您？",
          offline_message: "当前客服不在线，请留下联系方式，我们会尽快回复。",
          ai_enabled: true,
          human_chat_enabled: true,
          show_branding: true,
          status: "active"
        })
      });
      setName("");
      setDomain("");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "创建失败");
    }
  }

  async function showEmbed(site: Site) {
    const data = await apiRequest<{ embed_code: string }>(`/sites/${site.id}/embed-code`);
    setEmbedCodes((prev) => ({ ...prev, [site.id]: data.embed_code }));
  }

  async function toggleStatus(site: Site) {
    await apiRequest<Site>(`/sites/${site.id}`, {
      method: "PUT",
      body: JSON.stringify({ status: site.status === "active" ? "paused" : "active" })
    });
    load();
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold text-brand">Sites</p>
        <h1 className="text-3xl font-bold">网站管理</h1>
      </div>
      <Panel>
        <form onSubmit={createSite} className="grid gap-3 md:grid-cols-[1fr_1fr_auto]">
          <Input placeholder="网站名称" value={name} onChange={(event) => setName(event.target.value)} required />
          <Input placeholder="域名，例如 example.com" value={domain} onChange={(event) => setDomain(event.target.value)} />
          <Button>
            <Plus size={17} />
            创建网站
          </Button>
        </form>
        {error ? <p className="mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      </Panel>
      <div className="grid gap-4">
        {sites.map((site) => (
          <Panel key={site.id}>
            <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
              <div className="flex items-start gap-3">
                <span className="grid size-10 place-items-center rounded-md bg-mist text-brand">
                  <Globe2 size={20} />
                </span>
                <div>
                  <h2 className="font-bold">{site.name}</h2>
                  <p className="text-sm text-slate-500">{site.domain || "未设置域名"} · {site.site_key}</p>
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="rounded-md bg-teal-50 px-3 py-2 text-xs font-bold text-teal-700">{site.status}</span>
                <GhostButton onClick={() => toggleStatus(site)}>
                  {site.status === "active" ? "暂停" : "启用"}
                </GhostButton>
                <GhostButton onClick={() => showEmbed(site)}>
                  <Clipboard size={16} />
                  接入代码
                </GhostButton>
              </div>
            </div>
            {embedCodes[site.id] ? (
              <pre className="mt-4 overflow-x-auto rounded-md bg-ink p-4 text-xs text-white">{embedCodes[site.id]}</pre>
            ) : null}
          </Panel>
        ))}
        {!sites.length ? <Panel className="text-sm text-slate-500">还没有网站，先创建一个用于接入 widget。</Panel> : null}
      </div>
    </div>
  );
}
