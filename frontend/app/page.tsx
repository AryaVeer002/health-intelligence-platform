import AppShell from "@/components/layout/AppShell";

import WelcomePanel from "@/components/dashboard/WelcomePanel";
import MetricCard from "@/components/dashboard/MetricCard";
import HealthTimeline from "@/components/dashboard/HealthTimeline";
import TrendPanel from "@/components/dashboard/TrendPanel";
import AIInsightPanel from "@/components/dashboard/AIInsightPanel";

import {
  getDashboard,
  getMeasurements,
} from "@/lib/api";

export default async function Home() {
  const [dashboard, measurements] = await Promise.all([
    getDashboard(1),
    getMeasurements(1),
  ]);

  return (
    <AppShell>
      <div className="space-y-6 p-6 lg:p-8">

        {/* Welcome */}
        <WelcomePanel />

        {/* Health Metrics */}
        <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            label="BMI"
            value={
              dashboard.profile?.bmi.toFixed(2) ?? "—"
            }
            unit="kg/m²"
            description="Current profile"
          />

          <MetricCard
            label="Weight"
            value={
              dashboard.profile?.weight.toString() ?? "—"
            }
            unit="kg"
            description="Current profile"
          />

          <MetricCard
            label="Height"
            value={
              dashboard.profile?.height.toString() ?? "—"
            }
            unit="cm"
            description="Current profile"
          />

          <MetricCard
            label="Risk Score"
            value={
              dashboard.risk
                ? `${(
                    dashboard.risk.risk_score * 100
                  ).toFixed(2)}`
                : "—"
            }
            unit="%"
            description="Model-estimated"
          />
        </section>

        {/* Timeline + Trends */}
        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1.4fr_1fr]">
          <HealthTimeline
            measurements={measurements.measurements}
          />

          <TrendPanel
            trends={dashboard.trends}
            measurements={measurements.measurements}
          />
        </section>

        {/* AI Insights */}
        <AIInsightPanel
          insights={dashboard.insights}
        />

      </div>
    </AppShell>
  );
}