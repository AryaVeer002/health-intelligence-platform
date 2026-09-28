type Explanation = {
  factor: string;
  contribution: number;
  direction: string;
};

type Insight = {
  type: string;
  metric: string;
  message: string;
  risk_score?: number;
  risk_level?: string;
  explanations?: Explanation[];
};

type AIInsightPanelProps = {
  insights: Insight[];
};

export default function AIInsightPanel({
  insights,
}: AIInsightPanelProps) {
  return (
    <section className="rounded-2xl border border-cyan-400/10 bg-gradient-to-br from-cyan-400/[0.06] to-[#10161d] p-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">
            AI Intelligence
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Personalized Insights
          </h2>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-400/10 text-cyan-300">
          ✦
        </div>
      </div>

      {/* Insights */}
      <div className="mt-6 space-y-3">
        {insights.map((insight, index) => (
          <div
            key={`${insight.type}-${insight.metric}-${index}`}
            className="rounded-xl border border-white/5 bg-black/10 p-4"
          >
            <div className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan-300" />

              <p className="text-sm font-medium text-white">
                {insight.type === "risk"
                  ? "Risk model explanation"
                  : "Health trend detected"}
              </p>
            </div>

            <p className="mt-2 text-sm leading-6 text-gray-400">
              {insight.message}
            </p>

            {/* Risk explanations */}
            {insight.explanations &&
              insight.explanations.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {insight.explanations.map((explanation) => (
                    <span
                      key={explanation.factor}
                      className="rounded-lg bg-white/5 px-2.5 py-1 text-xs text-gray-400"
                    >
                      {explanation.factor}:{" "}
                      {explanation.direction}
                    </span>
                  ))}
                </div>
              )}
          </div>
        ))}
      </div>

      {/* Disclaimer */}
      <p className="mt-5 text-[11px] leading-5 text-gray-600">
        AI-generated insights are intended for health information and
        decision support, not medical diagnosis.
      </p>
    </section>
  );
}