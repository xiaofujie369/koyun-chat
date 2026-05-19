"use client";

import { useEffect, useState } from "react";
import { Shield } from "lucide-react";
import { apiRequest } from "@/lib/api";
import { Panel, StatCard } from "@/components/ui";

type Stats = {
  users: number;
  workspaces: number;
  sites: number;
  subscriptions: number;
};

export default function AdminPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiRequest<Stats>("/admin/stats").then(setStats).catch((err) => setError(err instanceof Error ? err.message : "无权限"));
  }, []);

  return (
    <main className="min-h-screen bg-mist px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl space-y-6">
        <div className="flex items-center gap-3">
          <span className="grid size-11 place-items-center rounded-md bg-ink text-white"><Shield size={20} /></span>
          <div>
            <p className="text-sm font-bold text-brand">Admin</p>
            <h1 className="text-3xl font-bold">平台后台</h1>
          </div>
        </div>
        {error ? <Panel className="text-sm text-red-700">{error}</Panel> : null}
        <div className="grid gap-4 md:grid-cols-4">
          <StatCard label="用户" value={String(stats?.users ?? 0)} />
          <StatCard label="工作区" value={String(stats?.workspaces ?? 0)} />
          <StatCard label="网站" value={String(stats?.sites ?? 0)} />
          <StatCard label="订阅" value={String(stats?.subscriptions ?? 0)} />
        </div>
      </div>
    </main>
  );
}
