"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, CreditCard } from "lucide-react";
import { apiRequest } from "@/lib/api";
import type { Plan } from "@/lib/types";
import { Button, Panel } from "@/components/ui";

export default function BillingPage() {
  const [plans, setPlans] = useState<Plan[]>([]);

  useEffect(() => {
    apiRequest<Plan[]>("/billing/plans").then(setPlans).catch(() => setPlans([]));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold text-brand">Billing</p>
        <h1 className="text-3xl font-bold">套餐与账单</h1>
      </div>
      <Panel>
        <div className="flex items-center gap-3">
          <CreditCard className="text-brand" />
          <div>
            <h2 className="font-bold">当前套餐</h2>
            <p className="text-sm text-slate-500">注册后默认 Trial，支付渠道接入后可升级。</p>
          </div>
        </div>
      </Panel>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        {plans.map((plan) => (
          <Panel key={plan.id}>
            <h2 className="text-lg font-bold">{plan.name}</h2>
            <p className="mt-3 text-3xl font-bold">{plan.price_monthly === null ? "Custom" : `$${plan.price_monthly}`}</p>
            <div className="mt-4 space-y-2 text-sm text-slate-600">
              <p className="flex gap-2"><CheckCircle2 size={16} className="text-leaf" />网站数：{plan.max_sites ?? "不限"}</p>
              <p className="flex gap-2"><CheckCircle2 size={16} className="text-leaf" />客服数：{plan.max_agents ?? "不限"}</p>
              <p className="flex gap-2"><CheckCircle2 size={16} className="text-leaf" />AI 消息：{plan.max_ai_messages_monthly ?? "不限"}</p>
            </div>
            <Button className="mt-5 w-full">升级</Button>
          </Panel>
        ))}
      </div>
    </div>
  );
}
