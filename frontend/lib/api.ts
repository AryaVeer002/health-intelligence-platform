const API_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000";

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

export async function login(
  email: string,
  password: string
) {
  const response = await fetch(
    `${API_URL}/api/v1/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Invalid email or password");
  }

  return response.json();
}


export async function getDashboard(
  userId: number,
  token: string
): Promise<DashboardData> {
  const response = await fetch(
    `${API_URL}/api/v1/analytics/users/${userId}/dashboard`,
    {
      cache: "no-store",
      headers: {
        Authorization: `Bearer ${token}`,
      },
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
  userId: number,
  token: string
): Promise<MeasurementsResponse> {
  const response = await fetch(
    `${API_URL}/api/v1/analytics/users/${userId}/measurements`,
    {
      cache: "no-store",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(
      `Measurements API failed with status ${response.status}`
    );
  }

  return response.json();
}


export type InsightExplanation = {
  factor: string;
  contribution: number;
  direction: string;
};

export type HealthInsight = {
  type: string;
  metric: string;
  message: string;
  risk_score?: number;
  risk_level?: string;
  explanations?: InsightExplanation[];
};

export type InsightsResponse = {
  user_id: number;
  insight_count: number;
  insights: HealthInsight[];
};


export async function getInsights(
  userId: number,
  token: string
): Promise<InsightsResponse> {
  const response = await fetch(
    `${API_URL}/api/v1/analytics/users/${userId}/insights`,
    {
      cache: "no-store",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(
      `Insights API failed with status ${response.status}`
    );
  }

  return response.json();
}