import AppShell from "@/components/layout/AppShell";
import { getInsights } from "@/lib/api";

export default async function InsightsPage() {
  const data = await getInsights(1);

  const trendInsights = data.insights.filter(
    (insight) => insight.type === "trend"
  );

  const profileInsights = data.insights.filter(
    (insight) => insight.type === "profile"
  );

  const riskInsights = data.insights.filter(
    (insight) => insight.type === "risk"
  );

  return (
    <AppShell>
      <main className="px-6 py-8 text-white lg:px-8">
        <div className="mx-auto max-w-7xl">
          {/* Header */}
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-cyan-300">
              AI Intelligence
            </p>

            <h1 className="mt-2 text-3xl font-semibold tracking-tight">
              Health Insights
            </h1>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-500">
              Trends, profile information and model-generated
              health intelligence derived from your available
              data.
            </p>
          </div>

          {/* Summary */}
          <section className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="rounded-2xl border border-white/10 bg-[#10161d] p-5">
              <p className="text-sm text-gray-500">
                Total Insights
              </p>

              <p className="mt-3 text-3xl font-semibold text-white">
                {data.insight_count}
              </p>

              <p className="mt-2 text-xs text-gray-600">
                Generated from current health data
              </p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-[#10161d] p-5">
              <p className="text-sm text-gray-500">
                Trends Detected
              </p>

              <p className="mt-3 text-3xl font-semibold text-white">
                {trendInsights.length}
              </p>

              <p className="mt-2 text-xs text-gray-600">
                Historical measurement changes
              </p>
            </div>

            <div className="rounded-2xl border border-cyan-400/10 bg-cyan-400/[0.04] p-5">
              <p className="text-sm text-gray-500">
                Risk Models
              </p>

              <p className="mt-3 text-3xl font-semibold text-cyan-300">
                {riskInsights.length}
              </p>

              <p className="mt-2 text-xs text-gray-600">
                Model-estimated assessments
              </p>
            </div>
          </section>

          {/* Trend Insights */}
          <section className="mt-8">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
                Pattern Detection
              </p>

              <h2 className="mt-1 text-lg font-semibold text-white">
                Health Trends
              </h2>
            </div>

            <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
              {trendInsights.map((insight) => (
                <div
                  key={insight.metric}
                  className="rounded-2xl border border-white/10 bg-[#10161d] p-5"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-400/10 text-cyan-300">
                      ↑
                    </div>

                    <div>
                      <p className="text-sm font-medium text-white">
                        {insight.metric}
                      </p>

                      <p className="text-xs text-gray-600">
                        Trend detected
                      </p>
                    </div>
                  </div>

                  <p className="mt-4 text-sm leading-6 text-gray-400">
                    {insight.message}
                  </p>
                </div>
              ))}
            </div>
          </section>

          {/* Profile Insights */}
          {profileInsights.length > 0 && (
            <section className="mt-8">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
                  Profile Intelligence
                </p>

                <h2 className="mt-1 text-lg font-semibold text-white">
                  Current Profile
                </h2>
              </div>

              <div className="mt-4 space-y-3">
                {profileInsights.map((insight, index) => (
                  <div
                    key={`${insight.metric}-${index}`}
                    className="rounded-2xl border border-white/10 bg-[#10161d] p-5"
                  >
                    <p className="text-sm font-medium text-white">
                      {insight.metric}
                    </p>

                    <p className="mt-2 text-sm text-gray-400">
                      {insight.message}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Risk Intelligence */}
          {riskInsights.length > 0 && (
            <section className="mt-8">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">
                  Risk Intelligence
                </p>

                <h2 className="mt-1 text-lg font-semibold text-white">
                  Model Assessment
                </h2>
              </div>

              <div className="mt-4 space-y-4">
                {riskInsights.map((insight, index) => (
                  <div
                    key={`${insight.metric}-${index}`}
                    className="rounded-2xl border border-cyan-400/10 bg-gradient-to-br from-cyan-400/[0.05] to-[#10161d] p-6"
                  >
                    <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
                      <div>
                        <p className="text-sm font-medium text-white">
                          {insight.metric}
                        </p>

                        <p className="mt-3 text-4xl font-semibold text-cyan-300">
                          {insight.risk_score !==
                          undefined
                            ? `${(
                                insight.risk_score * 100
                              ).toFixed(2)}%`
                            : "—"}
                        </p>

                        <p className="mt-2 text-xs text-gray-500">
                          Risk level:{" "}
                          {insight.risk_level ?? "—"}
                        </p>
                      </div>

                      <div className="max-w-2xl">
                        <p className="text-sm leading-6 text-gray-400">
                          {insight.message}
                        </p>

                        {insight.explanations &&
                          insight.explanations.length > 0 && (
                            <div className="mt-4">
                              <p className="text-xs uppercase tracking-[0.2em] text-gray-600">
                                Model Factors
                              </p>

                              <div className="mt-3 flex flex-wrap gap-2">
                                {insight.explanations.map(
                                  (explanation) => (
                                    <span
                                      key={
                                        explanation.factor
                                      }
                                      className="rounded-lg border border-white/5 bg-white/[0.03] px-3 py-2 text-xs text-gray-400"
                                    >
                                      {explanation.factor}:{" "}
                                      {
                                        explanation.direction
                                      }
                                    </span>
                                  )
                                )}
                              </div>
                            </div>
                          )}
                      </div>
                    </div>

                    <p className="mt-6 text-[11px] leading-5 text-gray-600">
                      Model-generated information is intended
                      for health information and decision
                      support. It is not a medical diagnosis or
                      treatment recommendation.
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>
    </AppShell>
  );
}