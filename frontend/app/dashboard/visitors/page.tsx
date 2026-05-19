"use client";

import { useEffect, useState } from "react";
import { MonitorSmartphone } from "lucide-react";
import { apiRequest } from "@/lib/api";
import type { Visitor } from "@/lib/types";
import { Panel } from "@/components/ui";

export default function VisitorsPage() {
  const [visitors, setVisitors] = useState<Visitor[]>([]);

  useEffect(() => {
    apiRequest<Visitor[]>("/visitors").then(setVisitors).catch(() => setVisitors([]));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold text-brand">Visitors</p>
        <h1 className="text-3xl font-bold">访客追踪</h1>
      </div>
      <Panel>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[760px] text-left text-sm">
            <thead className="text-slate-500">
              <tr>
                <th className="py-3">访客</th>
                <th>状态</th>
                <th>设备</th>
                <th>浏览器</th>
                <th>语言</th>
                <th>最后访问</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {visitors.map((visitor) => (
                <tr key={visitor.id}>
                  <td className="py-3 font-semibold">{visitor.visitor_uid}</td>
                  <td>
                    <span className={`rounded-md px-2 py-1 text-xs font-bold ${visitor.is_online ? "bg-teal-50 text-teal-700" : "bg-slate-100 text-slate-600"}`}>
                      {visitor.is_online ? "online" : "offline"}
                    </span>
                  </td>
                  <td className="flex items-center gap-2 py-3">
                    <MonitorSmartphone size={16} className="text-brand" />
                    {visitor.device_type || "-"} / {visitor.os || "-"}
                  </td>
                  <td>{visitor.browser || "-"}</td>
                  <td>{visitor.language || "-"}</td>
                  <td>{new Date(visitor.last_seen_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {!visitors.length ? <p className="py-8 text-sm text-slate-500">暂无访客数据。</p> : null}
        </div>
      </Panel>
    </div>
  );
}
