"use client";

import { useEffect, useState } from "react";
import { Mail, Phone } from "lucide-react";
import { apiRequest } from "@/lib/api";
import type { Lead } from "@/lib/types";
import { Panel } from "@/components/ui";

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);

  useEffect(() => {
    apiRequest<Lead[]>("/leads").then(setLeads).catch(() => setLeads([]));
  }, []);

  async function updateStatus(lead: Lead, status: string) {
    const updated = await apiRequest<Lead>(`/leads/${lead.id}`, {
      method: "PUT",
      body: JSON.stringify({ status })
    });
    setLeads((prev) => prev.map((item) => (item.id === updated.id ? updated : item)));
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold text-brand">Leads</p>
        <h1 className="text-3xl font-bold">销售线索</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {leads.map((lead) => (
          <Panel key={lead.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="font-bold">{lead.name || "未命名线索"}</h2>
                <p className="mt-1 text-xs text-slate-500">{new Date(lead.created_at).toLocaleString()}</p>
              </div>
              <select
                className="h-8 rounded-md border border-line bg-white px-2 text-xs font-bold text-slate-700"
                value={lead.status}
                onChange={(event) => updateStatus(lead, event.target.value)}
              >
                {["new", "contacted", "won", "lost", "invalid"].map((status) => (
                  <option key={status} value={status}>{status}</option>
                ))}
              </select>
            </div>
            <div className="mt-4 space-y-2 text-sm text-slate-600">
              {lead.email ? <p className="flex items-center gap-2"><Mail size={15} />{lead.email}</p> : null}
              {lead.phone ? <p className="flex items-center gap-2"><Phone size={15} />{lead.phone}</p> : null}
              {lead.telegram ? <p>Telegram: {lead.telegram}</p> : null}
              {lead.whatsapp ? <p>WhatsApp: {lead.whatsapp}</p> : null}
              {lead.source_url ? <p className="break-all">来源: {lead.source_url}</p> : null}
            </div>
            {lead.message ? <p className="mt-4 rounded-md bg-mist p-3 text-sm text-slate-700">{lead.message}</p> : null}
          </Panel>
        ))}
        {!leads.length ? <Panel className="text-sm text-slate-500">暂无线索。</Panel> : null}
      </div>
    </div>
  );
}
