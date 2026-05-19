import { Bell, KeyRound, SlidersHorizontal, UsersRound } from "lucide-react";
import { Panel } from "@/components/ui";

const settings = [
  { icon: UsersRound, title: "团队设置", text: "邀请客服坐席、设置 owner/admin/agent/viewer 权限。" },
  { icon: SlidersHorizontal, title: "站点默认设置", text: "统一配置欢迎语、离线留言、颜色和品牌展示。" },
  { icon: Bell, title: "通知设置", text: "连接 SMTP 后可发送线索和离线消息通知。" },
  { icon: KeyRound, title: "API 设置", text: "配置 OpenAI-compatible API、私有化部署和后续 webhook。" }
];

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold text-brand">Settings</p>
        <h1 className="text-3xl font-bold">设置</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {settings.map((item) => {
          const Icon = item.icon;
          return (
            <Panel key={item.title}>
              <Icon className="text-brand" />
              <h2 className="mt-4 font-bold">{item.title}</h2>
              <p className="mt-2 text-sm leading-6 text-slate-600">{item.text}</p>
            </Panel>
          );
        })}
      </div>
    </div>
  );
}
