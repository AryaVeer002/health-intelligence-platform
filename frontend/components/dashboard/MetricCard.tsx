type MetricCardProps = {
  label: string;
  value: string;
  unit?: string;
  description?: string;
};

export default function MetricCard({
  label,
  value,
  unit,
  description,
}: MetricCardProps) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#10161d] p-5 transition hover:border-cyan-400/20">
      <p className="text-sm text-gray-500">
        {label}
      </p>

      <div className="mt-3 flex items-end gap-2">
        <span className="text-3xl font-semibold tracking-tight text-white">
          {value}
        </span>

        {unit && (
          <span className="mb-1 text-xs text-gray-500">
            {unit}
          </span>
        )}
      </div>

      {description && (
        <p className="mt-3 text-xs text-gray-500">
          {description}
        </p>
      )}
    </div>
  );
}