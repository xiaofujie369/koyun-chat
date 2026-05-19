"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { LogIn } from "lucide-react";
import { apiRequest, setToken } from "@/lib/api";
import type { AuthResponse } from "@/lib/types";
import { Button, Input, Panel } from "@/components/ui";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await apiRequest<AuthResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });
      setToken(data.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "登录失败");
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
        <h1 className="mt-8 text-2xl font-bold">登录后台</h1>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <Input type="email" placeholder="邮箱" value={email} onChange={(event) => setEmail(event.target.value)} required />
          <Input type="password" placeholder="密码" value={password} onChange={(event) => setPassword(event.target.value)} required />
          {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
          <Button className="w-full" disabled={loading}>
            <LogIn size={17} />
            {loading ? "登录中..." : "登录"}
          </Button>
        </form>
        <p className="mt-5 text-center text-sm text-slate-600">
          没有账号？ <Link href="/register" className="font-semibold text-brand">注册</Link>
        </p>
      </Panel>
    </main>
  );
}
