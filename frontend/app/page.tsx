"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/layout/AppShell";

import WelcomePanel from "@/components/dashboard/WelcomePanel";
import MetricCard from "@/components/dashboard/MetricCard";
import HealthTimeline from "@/components/dashboard/HealthTimeline";
import TrendPanel from "@/components/dashboard/TrendPanel";
import AIInsightPanel from "@/components/dashboard/AIInsightPanel";

import {
  getDashboard,
  getMeasurements,
  login,
  type DashboardData,
  type MeasurementsResponse,
} from "@/lib/api";

const DEMO_USER_ID = 6;

export default function Home() {
  const [token, setToken] = useState<string | null>(null);

  const [email, setEmail] = useState(
    "demo@healthplatform.com"
  );

  const [password, setPassword] = useState(
    "Demo@12345"
  );

  const [dashboard, setDashboard] =
    useState<DashboardData | null>(null);

  const [measurements, setMeasurements] =
    useState<MeasurementsResponse | null>(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  useEffect(() => {
    const savedToken =
      window.localStorage.getItem("health_token");

    if (savedToken) {
      setToken(savedToken);
    }
  }, []);

  useEffect(() => {
    if (!token) {
      return;
    }

    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const [dashboardData, measurementData] =
          await Promise.all([
            getDashboard(DEMO_USER_ID, token),
            getMeasurements(DEMO_USER_ID, token),
          ]);

        setDashboard(dashboardData);
        setMeasurements(measurementData);
      } catch (err) {
        window.localStorage.removeItem(
          "health_token"
        );

        setToken(null);

        setError(
          err instanceof Error
            ? err.message
            : "Unable to load dashboard"
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [token]);

  async function handleLogin(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");

      const result = await login(
        email,
        password
      );

      window.localStorage.setItem(
        "health_token",
        result.access_token
      );

      setToken(result.access_token);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Login failed"
      );
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    window.localStorage.removeItem(
      "health_token"
    );

    setToken(null);
    setDashboard(null);
    setMeasurements(null);
  }

  if (!token) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
        <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
          <div className="mb-8 text-center">
            <h1 className="text-3xl font-bold text-slate-900">
              Health Intelligence Platform
            </h1>

            <p className="mt-2 text-sm text-slate-500">
              AI-powered health information and
              decision-support platform
            </p>
          </div>

          <form
            onSubmit={handleLogin}
            className="space-y-5"
          >
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">
                Email
              </label>

              <input
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">
                Password
              </label>

              <input
                type="password"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500"
                required
              />
            </div>

            {error && (
              <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:opacity-50"
            >
              {loading
                ? "Signing in..."
                : "Sign In"}
            </button>
          </form>

          <div className="mt-6 rounded-lg bg-slate-50 p-4 text-xs text-slate-500">
            <p className="font-semibold">
              Hackathon Demo Account
            </p>

            <p className="mt-1">
              demo@healthplatform.com
            </p>

            <p>
              Demo@12345
            </p>
          </div>
        </div>
      </main>
    );
  }

  if (loading || !dashboard || !measurements) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="text-slate-600">
          Loading health dashboard...
        </p>
      </main>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6 p-6 lg:p-8">

        <div className="flex justify-end">
          <button
            onClick={handleLogout}
            className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            Logout
          </button>
        </div>

        <WelcomePanel />

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
            label="Model Risk Score"
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

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1.4fr_1fr]">
          <HealthTimeline
            measurements={measurements.measurements}
          />

          <TrendPanel
            trends={dashboard.trends}
            measurements={measurements.measurements}
          />
        </section>

        <AIInsightPanel
          insights={dashboard.insights}
        />

      </div>
    </AppShell>
  );
}