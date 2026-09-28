type Measurement = {
  id: number;
  metric: string;
  value: number;
  unit: string;
  measured_at: string;
  report_id: number;
};

type HealthTimelineProps = {
  measurements: Measurement[];
};

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    year: "numeric",
  });
}

export default function HealthTimeline({
  measurements,
}: HealthTimelineProps) {
  const groupedDates = Array.from(
    new Map(
      measurements.map((measurement) => [
        measurement.measured_at,
        measurement.measured_at,
      ])
    ).values()
  ).sort(
    (a, b) =>
      new Date(a).getTime() - new Date(b).getTime()
  );

  return (
    <section className="rounded-2xl border border-white/10 bg-[#10161d] p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
            Longitudinal View
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Health Timeline
          </h2>
        </div>

        <span className="rounded-lg bg-cyan-400/10 px-3 py-2 text-xs text-cyan-300">
          {measurements.length} measurements
        </span>
      </div>

      {/* Timeline */}
      <div className="relative mt-8">
        <div className="absolute left-[7px] top-2 h-[calc(100%-8px)] w-px bg-white/10" />

        <div className="space-y-8">
          {groupedDates.map((date) => {
            const dateMeasurements = measurements.filter(
              (measurement) =>
                measurement.measured_at === date
            );

            return (
              <div
                key={date}
                className="relative flex gap-5"
              >
                {/* Timeline point */}
                <div className="relative z-10 mt-1 h-4 w-4 shrink-0 rounded-full border-4 border-[#10161d] bg-cyan-400 shadow-[0_0_12px_rgba(34,211,238,0.5)]" />

                {/* Date + measurements */}
                <div className="min-w-0 flex-1">
                  <p className="text-xs font-medium text-cyan-300">
                    {formatDate(date)}
                  </p>

                  <div className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
                    {dateMeasurements.map((measurement) => (
                      <div
                        key={measurement.id}
                        className="rounded-xl border border-white/5 bg-white/[0.02] p-3"
                      >
                        <p className="text-xs text-gray-500">
                          {measurement.metric}
                        </p>

                        <p className="mt-1 text-lg font-semibold text-white">
                          {measurement.value}
                        </p>

                        <p className="text-xs text-gray-600">
                          {measurement.unit}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}