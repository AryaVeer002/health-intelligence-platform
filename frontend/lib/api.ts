const API_URL =
  process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

export type DashboardData = {
  user_id: number;

  profile: {
    age: number;
    weight: number;
    height: number;
    bmi: number;
  } | null;

  risk: {
    risk_type: string;
    risk_score: number;
    risk_level: string;
    explanations: {
      factor: string;
      contribution: number;
      direction: string;
    }[];
  } | null;

  trends: {
    metric: string;
    unit: string;
    first_value: number;
    latest_value: number;
    change: number;
    change_percent: number;
    trend: string;
  }[];

  anomalies: {
    metric: string;
    value: number;
    previous_value: number;
    change_percent: number;
    is_anomaly: boolean;
  }[];

  insights: {
    type: string;
    metric: string;
    message: string;
    risk_score?: number;
    risk_level?: string;
    explanations?: {
      factor: string;
      contribution: number;
      direction: string;
    }[];
  }[];
};

export async function getDashboard(
  userId: number
): Promise<DashboardData> {
  const response = await fetch(
    `${API_URL}/api/v1/analytics/users/${userId}/dashboard`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(
      `Dashboard API failed with status ${response.status}`
    );
  }

  return response.json();
}


export type Measurement = {
  id: number;
  metric: string;
  value: number;
  unit: string;
  measured_at: string;
  report_id: number;
};

export type MeasurementsResponse = {
  user_id: number;
  count: number;
  measurements: Measurement[];
};

export async function getMeasurements(
  userId: number
): Promise<MeasurementsResponse> {
  const response = await fetch(
    `${API_URL}/api/v1/analytics/users/${userId}/measurements`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(
      `Measurements API failed with status ${response.status}`
    );
  }

  return response.json();
}