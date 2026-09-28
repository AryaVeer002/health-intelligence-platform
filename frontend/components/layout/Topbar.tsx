export default function Topbar() {
  return (
    <header className="flex h-20 items-center justify-between border-b border-white/10 bg-[#0b0f14] px-8 text-white">
      
      {/* Page title */}
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
          Health Overview
        </p>

        <h2 className="mt-1 text-xl font-semibold">
          Your Health Intelligence
        </h2>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-5">

        {/* Notification */}
        <button className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 text-gray-400 transition hover:bg-white/5 hover:text-white">
          ♢
        </button>

        {/* User */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-cyan-400/10 text-sm font-semibold text-cyan-300">
            AV
          </div>

          <div className="hidden sm:block">
            <p className="text-sm font-medium">
              Arya Veer
            </p>

            <p className="text-xs text-gray-500">
              Personal Dashboard
            </p>
          </div>
        </div>

      </div>
    </header>
  );
}