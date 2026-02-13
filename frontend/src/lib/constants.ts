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

export const PERSONA_TYPES: Record<string, string> = {
  natural: "Persona Natural",
  natural_comerciante: "Persona Natural Comerciante",
};

export const REGIMES: Record<string, string> = {
  ordinario: "Régimen Ordinario",
  simple: "Régimen Simple de Tributación",
};

export const RESULT_LABELS: Record<string, string> = {
  applies: "Aplica",
  does_not_apply: "No aplica",
  conditional: "Condicional",
  needs_more_info: "Requiere más info",
};

export const RESULT_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  applies: { bg: "bg-success-50", text: "text-success-700", border: "border-success-500" },
  does_not_apply: { bg: "bg-gray-50", text: "text-gray-600", border: "border-gray-300" },
  conditional: { bg: "bg-warning-50", text: "text-warning-700", border: "border-warning-500" },
  needs_more_info: { bg: "bg-primary-50", text: "text-primary-700", border: "border-primary-500" },
};

export const PERIODICITY_LABELS: Record<string, string> = {
  annual: "Anual",
  bimonthly: "Bimestral",
  quarterly: "Trimestral",
  monthly: "Mensual",
};

export const NAV_ITEMS = [
  { label: "Dashboard", href: ROUTES.DASHBOARD, icon: "home" },
  { label: "Perfil Tributario", href: ROUTES.PROFILES, icon: "user" },
  { label: "Evaluación", href: ROUTES.EVALUATIONS, icon: "clipboard" },
  { label: "Calendario", href: ROUTES.CALENDAR, icon: "calendar" },
  { label: "Obligaciones", href: ROUTES.OBLIGATIONS, icon: "book" },
] as const;
