type Trend = {
  metric: string;
  first_value: number;
  latest_value: number;
  change_percent: number;
  unit: string;
};

type Measurement = {
  id: number;
  metric: string;
  value: number;
  unit: string;
  measured_at: string;
  report_id: number;
};

type TrendPanelProps = {
  trends: Trend[];
  measurements: Measurement[];
};

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    year: "numeric",
  });
}

function buildChartPoints(
  metric: string,
  measurements: Measurement[]
) {
  return measurements
    .filter((measurement) => measurement.metric === metric)
    .sort(
      (a, b) =>
        new Date(a.measured_at).getTime() -
        new Date(b.measured_at).getTime()
    );
}

export default function TrendPanel({
  trends,
  measurements,
}: TrendPanelProps) {
  return (
    <section className="rounded-2xl border border-white/10 bg-[#10161d] p-6">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
          Pattern Detection
        </p>

        <h2 className="mt-1 text-lg font-semibold text-white">
          Health Trends
        </h2>
      </div>

      <div className="mt-6 space-y-4">
        {trends.map((trend) => {
          const points = buildChartPoints(
            trend.metric,
            measurements
          );

          const values = points.map(
            (point) => point.value
          );

          const minValue =
            values.length > 0
              ? Math.min(...values)
              : 0;

          const maxValue =
            values.length > 0
              ? Math.max(...values)
              : 1;

          const range =
            maxValue - minValue || 1;

          return (
            <div
              key={trend.metric}
              className="rounded-xl border border-white/5 bg-white/[0.02] p-4"
            >
              {/* Header */}
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-white">
                    {trend.metric}
                  </p>

                  <p className="mt-1 text-xs text-gray-500">
                    {trend.first_value} →{" "}
                    {trend.latest_value} {trend.unit}
                  </p>
                </div>

                <span className="rounded-lg bg-cyan-400/10 px-2.5 py-1 text-xs font-medium text-cyan-300">
                  {trend.change_percent >= 0
                    ? "+"
                    : ""}
                  {trend.change_percent}%
                </span>
              </div>

              {/* Real Trend Chart */}
              <div className="mt-5">
                {points.length >= 2 ? (
                  <div className="relative h-20">
                    <div className="absolute bottom-4 left-0 right-0 h-px bg-white/10" />

                    <svg
                      viewBox="0 0 300 80"
                      className="h-full w-full overflow-visible"
                      preserveAspectRatio="none"
                    >
                      {/* Trend line */}
                      <polyline
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        className="text-cyan-400"
                        points={points
                          .map((point, index) => {
                            const x =
                              (index /
                                (points.length - 1)) *
                                280 +
                              10;

                            const normalized =
                              (point.value -
                                minValue) /
                              range;

                            const y =
                              65 -
                              normalized * 50;

                            return `${x},${y}`;
                          })
                          .join(" ")}
                      />

                      {/* Measurement points */}
                      {points.map((point, index) => {
                        const x =
                          (index /
                            (points.length - 1)) *
                            280 +
                          10;

                        const normalized =
                          (point.value -
                            minValue) /
                          range;

                        const y =
                          65 -
                          normalized * 50;

                        return (
                          <circle
                            key={point.id}
                            cx={x}
                            cy={y}
                            r="3"
                            fill="currentColor"
                            className="text-cyan-300"
                          />
                        );
                      })}
                    </svg>

                    {/* Dates */}
                    <div className="absolute bottom-0 left-0 right-0 flex justify-between text-[9px] text-gray-600">
                      <span>
                        {formatDate(
                          points[0].measured_at
                        )}
                      </span>

                      <span>
                        {formatDate(
                          points[
                            points.length - 1
                          ].measured_at
                        )}
                      </span>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-gray-600">
                    Not enough historical data
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}