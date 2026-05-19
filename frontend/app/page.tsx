import { Bot, CheckCircle2, Code2, Gauge, MessagesSquare, MousePointer2, Radio, ShieldCheck, Sparkles, UsersRound } from "lucide-react";
import Link from "next/link";

const features = [
  { icon: MessagesSquare, title: "在线客服聊天", text: "客服坐席和访客实时对话，AI 可先接待，人工随时接管。" },
  { icon: Radio, title: "实时访客追踪", text: "查看访客来源、当前页面、设备和最近访问时间。" },
  { icon: Bot, title: "AI 自动回复", text: "基于商家知识库回答问题，引导访客留下有效联系方式。" },
  { icon: UsersRound, title: "销售线索收集", text: "离线或无法确认答案时自动收集姓名、邮箱和社交账号。" },
  { icon: ShieldCheck, title: "多租户隔离", text: "站点、访客、消息和线索按 workspace/site 严格隔离。" },
  { icon: Gauge, title: "套餐用量控制", text: "站点数、客服数、AI 消息数和访客量都有可扩展限制。" }
];

const plans = [
  ["Trial", "$0", "7 天试用，1 个网站，100 条 AI 消息"],
  ["Basic", "$9.9", "1 个网站，1 个客服，1000 条 AI 消息"],
  ["Pro", "$19.9", "3 个网站，3 个客服，可自定义颜色"],
  ["Business", "$49", "10 个网站，10 个客服，可去品牌"],
  ["Private", "Custom", "私有化部署和自定义限制"]
];

export default function HomePage() {
  return (
    <main className="bg-mist text-ink">
      <section className="min-h-[92vh] overflow-hidden border-b border-line bg-white">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-5 sm:px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-3 text-lg font-bold">
            <span className="grid size-9 place-items-center rounded-md bg-ink text-white">K</span>
            KoyunChat
          </Link>
          <div className="flex items-center gap-3">
            <Link href="/login" className="rounded-md px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-mist">
              登录
            </Link>
            <Link href="/register" className="rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700">
              注册
            </Link>
          </div>
        </nav>

        <div className="mx-auto grid max-w-7xl items-center gap-10 px-4 pb-12 pt-8 sm:px-6 lg:grid-cols-[0.9fr_1.1fr] lg:px-8">
          <div>
            <div className="inline-flex items-center gap-2 rounded-md border border-line bg-mist px-3 py-2 text-sm font-semibold text-slate-600">
              <Sparkles size={16} />
              一段代码接入在线客服
            </div>
            <h1 className="mt-6 max-w-3xl text-5xl font-bold leading-tight tracking-normal text-ink sm:text-6xl">
              给你的网站添加 24 小时 AI 在线客服
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
              一段代码接入，实时查看访客来源，自动回复客户问题，自动收集销售线索。
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/register" className="inline-flex h-11 items-center gap-2 rounded-md bg-brand px-5 text-sm font-bold text-white hover:bg-blue-700">
                <MousePointer2 size={17} />
                免费开始
              </Link>
              <a href="#pricing" className="inline-flex h-11 items-center gap-2 rounded-md border border-line bg-white px-5 text-sm font-bold text-ink hover:bg-mist">
                查看套餐
              </a>
            </div>
          </div>

          <div className="relative min-h-[560px]">
            <div className="absolute inset-x-0 top-0 rounded-lg border border-line bg-ink p-4 shadow-panel">
              <div className="flex items-center justify-between border-b border-white/10 pb-3">
                <div className="flex items-center gap-2 text-sm font-semibold text-white">
                  <span className="size-2 rounded-full bg-leaf" />
                  Live visitors
                </div>
                <Code2 size={18} className="text-white/70" />
              </div>
              <div className="grid gap-3 pt-4 sm:grid-cols-3">
                {["今日访客 248", "在线 16", "新线索 9"].map((item) => (
                  <div key={item} className="rounded-md bg-white/8 p-4 text-white">
                    <p className="text-sm text-white/60">{item.split(" ")[0]}</p>
                    <p className="mt-2 text-2xl font-bold">{item.split(" ")[1]}</p>
                  </div>
                ))}
              </div>
              <div className="mt-4 grid gap-3">
                {["Google /pricing", "Telegram /demo", "Direct /checkout"].map((item) => (
                  <div key={item} className="flex items-center justify-between rounded-md bg-white px-4 py-3 text-sm">
                    <span className="font-semibold text-ink">{item}</span>
                    <span className="rounded-md bg-teal-50 px-2 py-1 text-xs font-bold text-teal-700">online</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="absolute bottom-0 right-0 w-full max-w-sm rounded-lg border border-line bg-white shadow-panel">
              <div className="flex items-center justify-between border-b border-line px-4 py-3">
                <div>
                  <p className="font-bold">KoyunChat</p>
                  <p className="text-xs text-slate-500">AI 正在接待</p>
                </div>
                <span className="size-3 rounded-full bg-leaf" />
              </div>
              <div className="space-y-3 p-4 text-sm">
                <div className="max-w-[82%] rounded-md bg-mist p-3">您好，我想了解 Pro 套餐。</div>
                <div className="ml-auto max-w-[84%] rounded-md bg-brand p-3 text-white">Pro 支持 3 个网站、3 个客服和 5000 条 AI 消息。需要我帮您安排演示吗？</div>
                <div className="max-w-[82%] rounded-md bg-mist p-3">可以，联系我。</div>
              </div>
              <div className="border-t border-line p-3">
                <div className="h-10 rounded-md bg-mist px-3 py-2 text-sm text-slate-400">输入消息...</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <article key={feature.title} className="rounded-lg border border-line bg-white p-5 shadow-sm">
                <Icon className="text-brand" size={24} />
                <h2 className="mt-4 text-lg font-bold">{feature.title}</h2>
                <p className="mt-2 text-sm leading-6 text-slate-600">{feature.text}</p>
              </article>
            );
          })}
        </div>
      </section>

      <section id="pricing" className="border-y border-line bg-white">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="flex items-end justify-between gap-4">
            <div>
              <p className="text-sm font-bold text-brand">Pricing</p>
              <h2 className="mt-2 text-3xl font-bold">按成长阶段选择套餐</h2>
            </div>
            <CheckCircle2 className="hidden text-leaf sm:block" size={34} />
          </div>
          <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-5">
            {plans.map(([name, price, detail]) => (
              <article key={name} className="rounded-lg border border-line p-5">
                <h3 className="text-lg font-bold">{name}</h3>
                <p className="mt-4 text-3xl font-bold">{price}</p>
                <p className="mt-3 text-sm leading-6 text-slate-600">{detail}</p>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
