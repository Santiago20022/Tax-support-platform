// Auth
export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  tenant_slug?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
  tenant_slug?: string;
}

export interface TokenResponse {
  user_id: string;
  email: string;
  full_name: string;
  tenant_id: string;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RefreshResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// Fiscal Years
export interface FiscalYear {
  id: string;
  year: number;
  uvt_value: number;
  status: string;
  notes: string | null;
}

// Profiles
export interface ProfileCreateRequest {
  fiscal_year_id: string;
  persona_type: string;
  regime: string;
  is_iva_responsable: boolean;
  ingresos_brutos_cop: number;
  economic_activity_ciiu?: string | null;
  economic_activities?: string[];
  patrimonio_bruto_cop?: number | null;
  has_employees?: boolean;
  employee_count?: number;
  city?: string | null;
  department?: string | null;
  has_rut?: boolean;
  has_comercio_registration?: boolean;
  nit_last_digit?: number | null;
  consignaciones_cop?: number | null;
  compras_consumos_cop?: number | null;
  additional_data?: Record<string, unknown>;
}

export interface ProfileResponse {
  id: string;
  user_id: string;
  fiscal_year_id: string;
  persona_type: string;
  regime: string;
  is_iva_responsable: boolean;
  ingresos_brutos_cop: number;
  economic_activity_ciiu: string | null;
  patrimonio_bruto_cop: number | null;
  has_employees: boolean;
  employee_count: number;
  city: string | null;
  department: string | null;
  has_rut: boolean;
  has_comercio_registration: boolean;
  nit_last_digit: number | null;
  consignaciones_cop: number | null;
  compras_consumos_cop: number | null;
}

// Evaluations
export interface EvaluationCreateRequest {
  tax_profile_id: string;
}

export interface EvaluationSummary {
  total_obligations_evaluated: number;
  applies: number;
  does_not_apply: number;
  conditional: number;
  needs_more_info: number;
}

export interface ObligationBrief {
  code: string;
  name: string;
  category: string | null;
  responsible_entity: string | null;
}

export interface CalendarEntryBrief {
  title: string;
  due_date: string;
  periodicity: string;
}

export interface EvaluationResult {
  obligation: ObligationBrief;
  result: "applies" | "does_not_apply" | "needs_more_info" | "conditional";
  periodicity: string | null;
  explanation: string;
  legal_references: string[];
  conditions_evaluated: Record<string, unknown>[];
  calendar_entries: CalendarEntryBrief[];
}

export interface DisclaimerInfo {
  version: number;
  text: string;
  is_informational_only: boolean;
}

export interface EvaluationResponse {
  id: string;
  fiscal_year: number | null;
  rule_set_version: number | null;
  evaluated_at: string;
  profile_summary: Record<string, unknown>;
  results: EvaluationResult[];
  summary: EvaluationSummary | null;
  disclaimer: DisclaimerInfo | null;
}

export interface EvaluationListItem {
  id: string;
  fiscal_year_id: string;
  status: string;
  evaluated_at: string;
  summary: EvaluationSummary | null;
}

// Calendar
export interface CalendarEntry {
  id: string;
  obligation_type_id: string;
  title: string;
  description: string | null;
  due_date: string;
  periodicity: string;
  is_completed: boolean;
  completed_at: string | null;
}

// Obligations
export interface ObligationType {
  id: string;
  code: string;
  name: string;
  category: string;
  description: string;
  responsible_entity: string;
  legal_base: string | null;
  is_active: boolean;
  display_order: number;
}

// Disclaimers
export interface DisclaimerCurrent {
  id: string;
  version: number;
  content_es: string;
  content_en: string | null;
}
