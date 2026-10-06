"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const menuItems = [
  {
    icon: "⌂",
    label: "Dashboard",
    href: "/",
  },
  {
    icon: "♡",
    label: "My Health",
    href: "/health",
  },
  {
    icon: "↑",
    label: "Upload Reports",
    href: "/upload",
  },
  {
    icon: "✦",
    label: "AI Assistant",
    href: "#",
  },
  {
    icon: "◈",
    label: "Insights",
    href: "/insights",
  },
  {
    icon: "◎",
    label: "Profile",
    href: "#",
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col border-r border-white/10 bg-[#0b0f14] px-5 py-6 text-white">
      {/* Logo */}
      <div className="mb-10 flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400/10 text-xl text-cyan-300">
          ✚
        </div>

        <div>
          <h1 className="text-sm font-semibold tracking-wide">
            Health Intelligence
          </h1>

          <p className="text-xs text-gray-500">
            Personal Health AI
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex flex-1 flex-col gap-2">
        {menuItems.map((item) => {
          const isActive =
            item.href !== "#" &&
            pathname === item.href;

          return (
            <Link
              key={item.label}
              href={item.href}
              className={`flex items-center gap-4 rounded-xl px-4 py-3 text-left text-sm transition ${
                isActive
                  ? "bg-cyan-400/10 text-cyan-300"
                  : "text-gray-400 hover:bg-white/5 hover:text-white"
              }`}
            >
              <span className="w-5 text-center text-lg">
                {item.icon}
              </span>

              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Bottom */}
      <div className="border-t border-white/10 pt-4">
        <button className="flex w-full items-center gap-4 rounded-xl px-4 py-3 text-sm text-gray-400 transition hover:bg-white/5 hover:text-white">
          <span className="w-5 text-center text-lg">
            ⚙
          </span>

          Settings
        </button>
      </div>
    </aside>
  );
} 