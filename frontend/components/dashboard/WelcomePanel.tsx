import Link from "next/link";

export default function WelcomePanel() {
  return (
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-cyan-400/10 via-[#101820] to-[#0b0f14] p-8">
      
      {/* Glow */}
      <div className="pointer-events-none absolute -right-20 -top-20 h-64 w-64 rounded-full bg-cyan-400/10 blur-3xl" />

      <div className="relative max-w-2xl">
        <p className="mb-3 text-xs font-medium uppercase tracking-[0.25em] text-cyan-300">
          Personal Health Intelligence
        </p>

        <h1 className="text-3xl font-semibold leading-tight tracking-tight text-white sm:text-4xl">
          Understand Your Health.
          <br />
          Before It Becomes a Problem.
        </h1>

        <p className="mt-4 max-w-xl text-sm leading-6 text-gray-400">
          Your health data, reports and trends brought together into one
          intelligent view.
        </p>

        <div className="mt-7 flex flex-wrap gap-3">
          <Link
            href="/upload"
            className="rounded-xl bg-cyan-400 px-5 py-3 text-sm font-medium text-black transition hover:bg-cyan-300"
          >
            Upload Report
          </Link>

          <button className="rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-medium text-white transition hover:bg-white/10">
            Ask AI
          </button>
        </div>
      </div>
    </section>
  );
}