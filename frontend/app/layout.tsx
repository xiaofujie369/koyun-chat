import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "KoyunChat",
  description: "AI live chat, visitor tracking, and lead collection for any website."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
