"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { UserPlus } from "lucide-react";
import { apiRequest, setToken } from "@/lib/api";
import type { AuthResponse } from "@/lib/types";
import { Button, Input, Panel } from "@/components/ui";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "", workspace_name: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await apiRequest<AuthResponse>("/auth/register", {
        method: "POST",
        body: JSON.stringify(form)
      });
      setToken(data.access_token);
      router.push("/dashboard/sites");
    } catch (err) {
      setError(err instanceof Error ? err.message : "注册失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-mist px-4">
      <Panel className="w-full max-w-md">
        <Link href="/" className="flex items-center gap-3 text-lg font-bold">
          <span className="grid size-9 place-items-center rounded-md bg-ink text-white">K</span>
          KoyunChat
        </Link>
        <h1 className="mt-8 text-2xl font-bold">创建工作区</h1>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <Input placeholder="姓名" value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
          <Input type="email" placeholder="邮箱" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required />
          <Input type="password" placeholder="密码（至少 8 位）" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required minLength={8} />
          <Input placeholder="工作区名称" value={form.workspace_name} onChange={(event) => setForm({ ...form, workspace_name: event.target.value })} />
          {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
          <Button className="w-full" disabled={loading}>
            <UserPlus size={17} />
            {loading ? "创建中..." : "注册并开始"}
          </Button>
        </form>
        <p className="mt-5 text-center text-sm text-slate-600">
          已有账号？ <Link href="/login" className="font-semibold text-brand">登录</Link>
        </p>
      </Panel>
    </main>
  );
}
