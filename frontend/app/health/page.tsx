import { getDashboard, getMeasurements } from "@/lib/api";

export default async function HealthPage() {
  const [dashboard, measurements] = await Promise.all([
    getDashboard(1),
    getMeasurements(1),
  ]);

  return (
    <main className="min-h-screen bg-[#080c10] px-6 py-8 text-white lg:px-8">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-cyan-300">
            Personal Health
          </p>

          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            My Health
          </h1>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-500">
            A detailed view of your health profile, measurements and
            historical data.
          </p>
        </div>

        {/* Profile Overview */}
        <section className="mt-8">
          <div className="mb-4">
            <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
              Personal Overview
            </p>

            <h2 className="mt-1 text-lg font-semibold text-white">
              Current Health Profile
            </h2>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <div className="rounded-2xl border border-white/10 bg-[#10161d] p-5">
              <p className="text-sm text-gray-500">Age</p>

              <p className="mt-3 text-3xl font-semibold">
                {dashboard.profile?.age ?? "—"}
              </p>

              <p className="mt-2 text-xs text-gray-600">
                years
              </p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-[#10161d] p-5">
              <p className="text-sm text-gray-500">Weight</p>

              <p className="mt-3 text-3xl font-semibold">
                {dashboard.profile?.weight ?? "—"}
              </p>

              <p className="mt-2 text-xs text-gray-600">
                kg
              </p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-[#10161d] p-5">
              <p className="text-sm text-gray-500">Height</p>

              <p className="mt-3 text-3xl font-semibold">
                {dashboard.profile?.height ?? "—"}
              </p>

              <p className="mt-2 text-xs text-gray-600">
                cm
              </p>
            </div>

            <div className="rounded-2xl border border-cyan-400/10 bg-cyan-400/[0.04] p-5">
              <p className="text-sm text-gray-500">BMI</p>

              <p className="mt-3 text-3xl font-semibold text-cyan-300">
                {dashboard.profile?.bmi.toFixed(2) ?? "—"}
              </p>

              <p className="mt-2 text-xs text-gray-600">
                kg/m²
              </p>
            </div>
          </div>
        </section>

        {/* Measurements */}
        <section className="mt-8">
          <div className="mb-4 flex items-end justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
                Health Data
              </p>

              <h2 className="mt-1 text-lg font-semibold text-white">
                Measurements
              </h2>
            </div>

            <span className="rounded-lg bg-cyan-400/10 px-3 py-2 text-xs text-cyan-300">
              {measurements.count} measurements
            </span>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {measurements.measurements.map((measurement) => (
              <div
                key={measurement.id}
                className="rounded-2xl border border-white/10 bg-[#10161d] p-5"
              >
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm font-medium text-white">
                      {measurement.metric}
                    </p>

                    <p className="mt-1 text-xs text-gray-600">
                      {new Date(
                        measurement.measured_at
                      ).toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                        year: "numeric",
                      })}
                    </p>
                  </div>

                  <div className="text-right">
                    <p className="text-xl font-semibold text-white">
                      {measurement.value}
                    </p>

                    <p className="text-xs text-gray-500">
                      {measurement.unit}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Risk Intelligence */}
        {dashboard.risk && (
          <section className="mt-8 rounded-2xl border border-cyan-400/10 bg-gradient-to-br from-cyan-400/[0.05] to-[#10161d] p-6">
            <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">
              Risk Intelligence
            </p>

            <div className="mt-3 flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
              <div>
                <h2 className="text-lg font-semibold text-white">
                  {dashboard.risk.risk_type} risk model
                </h2>

                <p className="mt-2 text-sm text-gray-500">
                  Model-estimated risk score
                </p>

                <p className="mt-3 text-3xl font-semibold text-cyan-300">
                  {(dashboard.risk.risk_score * 100).toFixed(2)}%
                </p>

                <p className="mt-1 text-xs text-gray-600">
                  Level: {dashboard.risk.risk_level}
                </p>
              </div>

              <div className="max-w-xl">
                <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
                  Model Factors
                </p>

                <div className="mt-3 flex flex-wrap gap-2">
                  {dashboard.risk.explanations.map(
                    (explanation) => (
                      <span
                        key={explanation.factor}
                        className="rounded-lg border border-white/5 bg-white/[0.03] px-3 py-2 text-xs text-gray-400"
                      >
                        {explanation.factor}:{" "}
                        {explanation.direction}
                      </span>
                    )
                  )}
                </div>
              </div>
            </div>

            <p className="mt-6 text-[11px] leading-5 text-gray-600">
              This model provides health information and
              decision support. Its results are not a medical
              diagnosis or treatment recommendation.
            </p>
          </section>
        )}
      </div>
    </main>
  );
}