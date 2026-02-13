"use client";

import { useState, useEffect, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { apiClient, ApiError } from "@/lib/api-client";
import { useT, useLanguage } from "@/lib/language-context";
import { ROUTES } from "@/lib/constants";
import { formatCOP } from "@/lib/format";
import type {
  ProfileCreateRequest,
  FiscalYear,
  EvaluationResponse,
} from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { Alert } from "@/components/ui/alert";

const defaultProfile: ProfileCreateRequest = {
  fiscal_year_id: "",
  persona_type: "natural",
  regime: "ordinario",
  is_iva_responsable: false,
  ingresos_brutos_cop: 0,
  economic_activity_ciiu: "",
  economic_activities: [],
  patrimonio_bruto_cop: 0,
  has_employees: false,
  employee_count: 0,
  city: "",
  department: "",
  has_rut: false,
  has_comercio_registration: false,
  nit_last_digit: null,
  consignaciones_cop: 0,
  compras_consumos_cop: 0,
};

function Checkbox({
  id,
  label,
  checked,
  onChange,
}: {
  id: string;
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <label
      htmlFor={id}
      className={`flex cursor-pointer items-center gap-3 rounded-xl border p-3.5 transition-all duration-200 ${
        checked
          ? "border-primary-300 bg-primary-50 ring-1 ring-primary-200"
          : "border-border-strong hover:border-text-tertiary hover:bg-surface-hover"
      }`}
    >
      <input
        type="checkbox"
        id={id}
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
      />
      <span className="text-sm font-medium text-text-label">{label}</span>
    </label>
  );
}

export function ProfileWizard() {
  const router = useRouter();
  const t = useT();
  const { locale } = useLanguage();
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<ProfileCreateRequest>(defaultProfile);
  const [fiscalYears, setFiscalYears] = useState<FiscalYear[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const STEPS = t.wizard.steps;

  useEffect(() => {
    apiClient<FiscalYear[]>("/fiscal-years", { auth: false })
      .then((data) => {
        setFiscalYears(data);
        if (data.length > 0) setForm((f) => ({ ...f, fiscal_year_id: data[0].id }));
      })
      .catch(() => {});
  }, []);

  function update(fields: Partial<ProfileCreateRequest>) {
    setForm((f) => ({ ...f, ...fields }));
  }

  function numVal(val: string): number {
    const n = parseFloat(val.replace(/,/g, ""));
    return isNaN(n) ? 0 : n;
  }

  function next() {
    setError("");
    if (step === 0 && !form.fiscal_year_id) {
      setError(t.wizard.fiscalYearRequired);
      return;
    }
    if (step === 1 && form.ingresos_brutos_cop <= 0) {
      setError(t.wizard.grossIncomeRequired);
      return;
    }
    setStep((s) => Math.min(s + 1, STEPS.length - 1));
  }

  function prev() {
    setStep((s) => Math.max(s - 1, 0));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const profile = await apiClient<{ id: string }>("/profiles", { method: "POST", body: form });
      const evaluation = await apiClient<EvaluationResponse>("/evaluations", {
        method: "POST",
        body: { tax_profile_id: profile.id },
      });
      router.push(ROUTES.EVALUATION_DETAIL(evaluation.id));
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : t.wizard.createError);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Step indicator */}
      <div className="flex items-center gap-1">
        {STEPS.map((s, i) => (
          <div key={i} className="flex flex-1 flex-col items-center gap-1.5">
            <div className="flex w-full items-center">
              <div
                className={`mx-auto flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-bold transition-all duration-300 ${
                  i < step
                    ? "bg-primary-600 text-white shadow-sm shadow-primary-600/25"
                    : i === step
                      ? "bg-primary-600 text-white shadow-sm shadow-primary-600/25 ring-4 ring-primary-100"
                      : "bg-surface-secondary text-text-tertiary"
                }`}
              >
                {i < step ? (
                  <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clipRule="evenodd" />
                  </svg>
                ) : (
                  i + 1
                )}
              </div>
            </div>
            <span className={`text-[11px] font-medium hidden sm:block ${
              i <= step ? "text-primary-600" : "text-text-tertiary"
            }`}>
              {s.title}
            </span>
          </div>
        ))}
      </div>

      {error && <Alert variant="error">{error}</Alert>}

      <Card>
        <form onSubmit={handleSubmit}>
          <div className="animate-fade-in" key={step}>
            {/* Step 0 */}
            {step === 0 && (
              <div className="space-y-5">
                <div>
                  <h2 className="text-lg font-semibold text-text-primary">{t.wizard.taxpayerType}</h2>
                  <p className="mt-1 text-sm text-text-secondary">{t.wizard.selectTaxpayerDesc}</p>
                </div>
                <Select
                  id="fiscal_year_id"
                  label={t.wizard.fiscalYear}
                  value={form.fiscal_year_id}
                  onChange={(e) => update({ fiscal_year_id: e.target.value })}
                  options={fiscalYears.map((fy) => ({
                    value: fy.id,
                    label: `${fy.year} (UVT: ${formatCOP(fy.uvt_value, locale)})`,
                  }))}
                  placeholder={t.wizard.selectFiscalYear}
                />
                <Select
                  id="persona_type"
                  label={t.wizard.personaType}
                  value={form.persona_type}
                  onChange={(e) => update({ persona_type: e.target.value })}
                  options={Object.entries(t.labels.personaTypes).map(([value, label]) => ({ value, label }))}
                />
                <Select
                  id="regime"
                  label={t.wizard.regime}
                  value={form.regime}
                  onChange={(e) => update({ regime: e.target.value })}
                  options={Object.entries(t.labels.regimes).map(([value, label]) => ({ value, label }))}
                />
                <Checkbox
                  id="is_iva_responsable"
                  label={t.wizard.ivaCheckbox}
                  checked={form.is_iva_responsable}
                  onChange={(v) => update({ is_iva_responsable: v })}
                />
              </div>
            )}

            {/* Step 1 */}
            {step === 1 && (
              <div className="space-y-5">
                <div>
                  <h2 className="text-lg font-semibold text-text-primary">{t.wizard.financialTitle}</h2>
                  <p className="mt-1 text-sm text-text-secondary">{t.wizard.financialDesc}</p>
                </div>
                <Input
                  id="ingresos_brutos_cop"
                  label={t.wizard.grossIncome}
                  type="number"
                  value={form.ingresos_brutos_cop || ""}
                  onChange={(e) => update({ ingresos_brutos_cop: numVal(e.target.value) })}
                  placeholder="0"
                  required
                  hint={t.wizard.grossIncomeHint}
                />
                <Input
                  id="patrimonio_bruto_cop"
                  label={t.wizard.grossWealth}
                  type="number"
                  value={form.patrimonio_bruto_cop || ""}
                  onChange={(e) => update({ patrimonio_bruto_cop: numVal(e.target.value) })}
                  placeholder="0"
                  hint={t.wizard.grossWealthHint}
                />
                <Input
                  id="consignaciones_cop"
                  label={t.wizard.deposits}
                  type="number"
                  value={form.consignaciones_cop || ""}
                  onChange={(e) => update({ consignaciones_cop: numVal(e.target.value) })}
                  placeholder="0"
                />
                <Input
                  id="compras_consumos_cop"
                  label={t.wizard.purchases}
                  type="number"
                  value={form.compras_consumos_cop || ""}
                  onChange={(e) => update({ compras_consumos_cop: numVal(e.target.value) })}
                  placeholder="0"
                />
              </div>
            )}

            {/* Step 2 */}
            {step === 2 && (
              <div className="space-y-5">
                <div>
                  <h2 className="text-lg font-semibold text-text-primary">{t.wizard.activityTitle}</h2>
                  <p className="mt-1 text-sm text-text-secondary">{t.wizard.activityDesc}</p>
                </div>
                <Input
                  id="economic_activity_ciiu"
                  label={t.wizard.ciiuCode}
                  type="text"
                  value={form.economic_activity_ciiu || ""}
                  onChange={(e) => update({ economic_activity_ciiu: e.target.value })}
                  placeholder="Ej: 4711"
                  hint={t.wizard.ciiuHint}
                />
                <div className="space-y-3">
                  <label className="block text-sm font-medium text-text-label">{t.wizard.activeRegistrations}</label>
                  <Checkbox
                    id="has_rut"
                    label={t.wizard.hasRut}
                    checked={form.has_rut ?? false}
                    onChange={(v) => update({ has_rut: v })}
                  />
                  <Checkbox
                    id="has_comercio_registration"
                    label={t.wizard.hasCommerceReg}
                    checked={form.has_comercio_registration ?? false}
                    onChange={(v) => update({ has_comercio_registration: v })}
                  />
                </div>
              </div>
            )}

            {/* Step 3 */}
            {step === 3 && (
              <div className="space-y-5">
                <div>
                  <h2 className="text-lg font-semibold text-text-primary">{t.wizard.locationTitle}</h2>
                  <p className="mt-1 text-sm text-text-secondary">{t.wizard.locationDesc}</p>
                </div>
                <div className="grid gap-4 sm:grid-cols-2">
                  <Input
                    id="city"
                    label={t.wizard.cityLabel}
                    type="text"
                    value={form.city || ""}
                    onChange={(e) => update({ city: e.target.value })}
                    placeholder={t.wizard.cityPlaceholder}
                  />
                  <Input
                    id="department"
                    label={t.wizard.departmentLabel}
                    type="text"
                    value={form.department || ""}
                    onChange={(e) => update({ department: e.target.value })}
                    placeholder={t.wizard.departmentPlaceholder}
                  />
                </div>
                <Checkbox
                  id="has_employees"
                  label={t.wizard.hasEmployees}
                  checked={form.has_employees ?? false}
                  onChange={(v) => update({ has_employees: v, employee_count: v ? form.employee_count : 0 })}
                />
                {form.has_employees && (
                  <Input
                    id="employee_count"
                    label={t.wizard.employeeCount}
                    type="number"
                    value={form.employee_count || ""}
                    onChange={(e) => update({ employee_count: parseInt(e.target.value) || 0 })}
                    placeholder="0"
                  />
                )}
              </div>
            )}

            {/* Step 4 — Review */}
            {step === 4 && (
              <div className="space-y-5">
                <div>
                  <h2 className="text-lg font-semibold text-text-primary">{t.wizard.reviewTitle}</h2>
                  <p className="mt-1 text-sm text-text-secondary">{t.wizard.reviewDesc}</p>
                </div>
                <Input
                  id="nit_last_digit"
                  label={t.wizard.nitLastDigit}
                  type="number"
                  min={0}
                  max={9}
                  value={form.nit_last_digit ?? ""}
                  onChange={(e) => update({ nit_last_digit: e.target.value === "" ? null : parseInt(e.target.value) })}
                  placeholder="0-9"
                  hint={t.wizard.nitHint}
                />

                <div className="rounded-2xl border border-border bg-surface-inset p-5">
                  <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-text-tertiary">{t.wizard.summaryLabel}</h3>
                  <dl className="grid grid-cols-2 gap-x-6 gap-y-4 text-sm">
                    {[
                      [t.profileFields.personaType, t.labels.personaTypes[form.persona_type] || form.persona_type],
                      [t.profileFields.regime, t.labels.regimes[form.regime] || form.regime],
                      [t.profileFields.ivaResponsable, form.is_iva_responsable ? t.common.yes : t.common.no],
                      [t.profileFields.grossIncome, formatCOP(form.ingresos_brutos_cop, locale)],
                      [t.profileFields.grossWealth, formatCOP(form.patrimonio_bruto_cop ?? 0, locale)],
                      [t.profileFields.deposits, formatCOP(form.consignaciones_cop ?? 0, locale)],
                      ...(form.city ? [[t.profileFields.city, form.city]] : []),
                      ...(form.has_employees ? [[t.profileFields.employees, `${form.employee_count}`]] : []),
                    ].map(([label, value]) => (
                      <div key={label as string}>
                        <dt className="text-xs font-medium text-text-tertiary">{label}</dt>
                        <dd className="mt-0.5 font-semibold text-text-primary">{value}</dd>
                      </div>
                    ))}
                  </dl>
                </div>
              </div>
            )}
          </div>

          {/* Navigation */}
          <div className="mt-8 flex items-center justify-between border-t border-border pt-5">
            {step > 0 ? (
              <Button type="button" variant="ghost" onClick={prev}>
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                </svg>
                {t.common.previous}
              </Button>
            ) : (
              <div />
            )}
            {step < STEPS.length - 1 ? (
              <Button type="button" onClick={next}>
                {t.common.next}
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                </svg>
              </Button>
            ) : (
              <Button type="submit" loading={loading} variant="success">
                {t.wizard.createAndEvaluate}
              </Button>
            )}
          </div>
        </form>
      </Card>
    </div>
  );
}
