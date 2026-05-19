"use client";

import { BarChart3, BookOpen, CreditCard, Inbox, LayoutDashboard, Radio, Settings, Shield, UsersRound, Webhook } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { clearToken } from "@/lib/api";

const navItems = [
  { href: "/dashboard", label: "概览", icon: LayoutDashboard },
  { href: "/dashboard/sites", label: "网站", icon: Webhook },
  { href: "/dashboard/visitors", label: "访客", icon: Radio },
  { href: "/dashboard/inbox", label: "收件箱", icon: Inbox },
  { href: "/dashboard/knowledge", label: "知识库", icon: BookOpen },
  { href: "/dashboard/leads", label: "线索", icon: UsersRound },
  { href: "/dashboard/billing", label: "套餐", icon: CreditCard },
  { href: "/dashboard/settings", label: "设置", icon: Settings },
  { href: "/admin", label: "平台后台", icon: Shield }
];

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  function logout() {
    clearToken();
    router.push("/login");
  }

  return (
    <div className="min-h-screen bg-mist">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-white px-4 py-5 lg:block">
        <Link href="/" className="flex items-center gap-3 px-2 text-lg font-bold text-ink">
          <span className="grid size-9 place-items-center rounded-md bg-ink text-white">K</span>
          KoyunChat
        </Link>
        <nav className="mt-8 space-y-1">
          {navItems.map((item) => {
            const active = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex h-10 items-center gap-3 rounded-md px-3 text-sm font-medium transition ${
                  active ? "bg-brand text-white" : "text-slate-600 hover:bg-mist hover:text-ink"
                }`}
              >
                <Icon size={18} />
                {item.label}
              </Link>
            );
          })}
        </nav>
        <button onClick={logout} className="absolute bottom-5 left-4 right-4 h-10 rounded-md border border-line text-sm font-semibold text-slate-600">
          退出登录
        </button>
      </aside>
      <main className="lg:pl-64">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</div>
      </main>
    </div>
  );
}
