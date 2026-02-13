export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const ROUTES = {
  LOGIN: "/login",
  REGISTER: "/registro",
  DASHBOARD: "/dashboard",
  PROFILES: "/perfil",
  PROFILE_DETAIL: (id: string) => `/perfil/${id}`,
  EVALUATIONS: "/evaluacion",
  EVALUATION_DETAIL: (id: string) => `/evaluacion/${id}`,
  CALENDAR: "/calendario",
  OBLIGATIONS: "/obligaciones",
} as const;

export const RESULT_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  applies: { bg: "bg-success-50", text: "text-success-700", border: "border-success-500" },
  does_not_apply: { bg: "bg-gray-50", text: "text-gray-600", border: "border-gray-300" },
  conditional: { bg: "bg-warning-50", text: "text-warning-700", border: "border-warning-500" },
  needs_more_info: { bg: "bg-primary-50", text: "text-primary-700", border: "border-primary-500" },
};

export const NAV_ITEMS = [
  { key: "dashboard" as const, href: ROUTES.DASHBOARD, icon: "home" },
  { key: "taxProfile" as const, href: ROUTES.PROFILES, icon: "user" },
  { key: "evaluation" as const, href: ROUTES.EVALUATIONS, icon: "clipboard" },
  { key: "calendar" as const, href: ROUTES.CALENDAR, icon: "calendar" },
  { key: "obligations" as const, href: ROUTES.OBLIGATIONS, icon: "book" },
] as const;
