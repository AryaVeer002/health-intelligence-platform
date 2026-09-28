"use client";

import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";

type AppShellProps = {
  children: React.ReactNode;
};

export default function AppShell({
  children,
}: AppShellProps) {
  return (
    <main className="flex min-h-screen bg-[#080c10] text-white">
      <Sidebar />

      <div className="min-w-0 flex-1">
        <Topbar />

        <div className="min-h-[calc(100vh-5rem)]">
          {children}
        </div>
      </div>
    </main>
  );
}