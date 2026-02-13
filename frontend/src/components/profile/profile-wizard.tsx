"use client";

import { useState, useEffect, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { apiClient, ApiError } from "@/lib/api-client";
import { ROUTES, PERSONA_TYPES, REGIMES } from "@/lib/constants";
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

const STEPS = [
  { title: "Contribuyente", description: "Tipo y régimen" },
  { title: "Finanzas", description: "Datos financieros" },
  { title: "Actividad", description: "Económica y registros" },
  { title: "Ubicación", description: "Ciudad y empleados" },
  { title: "Revisión", description: "NIT y resumen final" },
];

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
          : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
      }`}
    >
      <input
        type="checkbox"
        id={id}
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
      />
      <span className="text-sm font-medium text-gray-700">{label}</span>
    </label>
  );
}

export function ProfileWizard() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<ProfileCreateRequest>(defaultProfile);
  const [fiscalYears, setFiscalYears] = useState<FiscalYear[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

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
      setError("Selecciona un año fiscal");
      return;
    }
    if (step === 1 && form.ingresos_brutos_cop <= 0) {
      setError("Los ingresos brutos son requeridos");
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
      setError(err instanceof ApiError ? err.detail : "Error al crear el perfil");
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
                      : "bg-gray-100 text-gray-400"
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
              i <= step ? "text-primary-600" : "text-gray-400"
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
                  <h2 className="text-lg font-semibold text-gray-900">Tipo de Contribuyente</h2>
                  <p className="mt-1 text-sm text-gray-500">Selecciona tu tipo de persona y régimen tributario</p>
                </div>
                <Select
                  id="fiscal_year_id"
                  label="Año Fiscal"
                  value={form.fiscal_year_id}
                  onChange={(e) => update({ fiscal_year_id: e.target.value })}
                  options={fiscalYears.map((fy) => ({
                    value: fy.id,
                    label: `${fy.year} (UVT: ${formatCOP(fy.uvt_value)})`,
                  }))}
                  placeholder="Selecciona el año fiscal"
                />
                <Select
                  id="persona_type"
                  label="Tipo de Persona"
                  value={form.persona_type}
                  onChange={(e) => update({ persona_type: e.target.value })}
                  options={Object.entries(PERSONA_TYPES).map(([value, label]) => ({ value, label }))}
                />
                <Select
                  id="regime"
                  label="Régimen Tributario"
                  value={form.regime}
                  onChange={(e) => update({ regime: e.target.value })}
                  options={Object.entries(REGIMES).map(([value, label]) => ({ value, label }))}
                />
                <Checkbox
                  id="is_iva_responsable"
                  label="Soy responsable de IVA"
                  checked={form.is_iva_responsable}
                  onChange={(v) => update({ is_iva_responsable: v })}
                />
              </div>
            )}

            {/* Step 1 */}
            {step === 1 && (
              <div className="space-y-5">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">Datos Financieros</h2>
                  <p className="mt-1 text-sm text-gray-500">Información de ingresos y patrimonio del año gravable</p>
                </div>
                <Input
                  id="ingresos_brutos_cop"
                  label="Ingresos Brutos (COP)"
                  type="number"
                  value={form.ingresos_brutos_cop || ""}
                  onChange={(e) => update({ ingresos_brutos_cop: numVal(e.target.value) })}
                  placeholder="0"
                  required
                  hint="Total de ingresos en el año gravable"
                />
                <Input
                  id="patrimonio_bruto_cop"
                  label="Patrimonio Bruto (COP)"
                  type="number"
                  value={form.patrimonio_bruto_cop || ""}
                  onChange={(e) => update({ patrimonio_bruto_cop: numVal(e.target.value) })}
                  placeholder="0"
                  hint="Valor total de bienes y derechos"
                />
                <Input
                  id="consignaciones_cop"
                  label="Consignaciones Bancarias (COP)"
                  type="number"
                  value={form.consignaciones_cop || ""}
                  onChange={(e) => update({ consignaciones_cop: numVal(e.target.value) })}
                  placeholder="0"
                />
                <Input
                  id="compras_consumos_cop"
                  label="Compras y Consumos con Tarjeta (COP)"
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
                  <h2 className="text-lg font-semibold text-gray-900">Actividad Económica</h2>
                  <p className="mt-1 text-sm text-gray-500">Código CIIU y registros activos</p>
                </div>
                <Input
                  id="economic_activity_ciiu"
                  label="Código CIIU Principal"
                  type="text"
                  value={form.economic_activity_ciiu || ""}
                  onChange={(e) => update({ economic_activity_ciiu: e.target.value })}
                  placeholder="Ej: 4711"
                  hint="Clasificación Industrial Internacional Uniforme"
                />
                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Registros activos</label>
                  <Checkbox
                    id="has_rut"
                    label="Tengo RUT activo"
                    checked={form.has_rut ?? false}
                    onChange={(v) => update({ has_rut: v })}
                  />
                  <Checkbox
                    id="has_comercio_registration"
                    label="Tengo registro mercantil activo"
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
                  <h2 className="text-lg font-semibold text-gray-900">Ubicación y Empleados</h2>
                  <p className="mt-1 text-sm text-gray-500">Información geográfica y de nómina</p>
                </div>
                <div className="grid gap-4 sm:grid-cols-2">
                  <Input
                    id="city"
                    label="Ciudad"
                    type="text"
                    value={form.city || ""}
                    onChange={(e) => update({ city: e.target.value })}
                    placeholder="Ej: Bogotá"
                  />
                  <Input
                    id="department"
                    label="Departamento"
                    type="text"
                    value={form.department || ""}
                    onChange={(e) => update({ department: e.target.value })}
                    placeholder="Ej: Cundinamarca"
                  />
                </div>
                <Checkbox
                  id="has_employees"
                  label="Tengo empleados a cargo"
                  checked={form.has_employees ?? false}
                  onChange={(v) => update({ has_employees: v, employee_count: v ? form.employee_count : 0 })}
                />
                {form.has_employees && (
                  <Input
                    id="employee_count"
                    label="Número de empleados"
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
                  <h2 className="text-lg font-semibold text-gray-900">Revisión Final</h2>
                  <p className="mt-1 text-sm text-gray-500">Verifica los datos antes de crear el perfil</p>
                </div>
                <Input
                  id="nit_last_digit"
                  label="Último dígito del NIT"
                  type="number"
                  min={0}
                  max={9}
                  value={form.nit_last_digit ?? ""}
                  onChange={(e) => update({ nit_last_digit: e.target.value === "" ? null : parseInt(e.target.value) })}
                  placeholder="0-9"
                  hint="Se usa para determinar las fechas del calendario tributario"
                />

                <div className="rounded-2xl border border-gray-100 bg-gray-50 p-5">
                  <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-gray-400">Resumen</h3>
                  <dl className="grid grid-cols-2 gap-x-6 gap-y-4 text-sm">
                    {[
                      ["Tipo de persona", PERSONA_TYPES[form.persona_type] || form.persona_type],
                      ["Régimen", REGIMES[form.regime] || form.regime],
                      ["Responsable IVA", form.is_iva_responsable ? "Sí" : "No"],
                      ["Ingresos brutos", formatCOP(form.ingresos_brutos_cop)],
                      ["Patrimonio bruto", formatCOP(form.patrimonio_bruto_cop ?? 0)],
                      ["Consignaciones", formatCOP(form.consignaciones_cop ?? 0)],
                      ...(form.city ? [["Ciudad", form.city]] : []),
                      ...(form.has_employees ? [["Empleados", `${form.employee_count}`]] : []),
                    ].map(([label, value]) => (
                      <div key={label as string}>
                        <dt className="text-xs font-medium text-gray-400">{label}</dt>
                        <dd className="mt-0.5 font-semibold text-gray-900">{value}</dd>
                      </div>
                    ))}
                  </dl>
                </div>
              </div>
            )}
          </div>

          {/* Navigation */}
          <div className="mt-8 flex items-center justify-between border-t border-gray-100 pt-5">
            {step > 0 ? (
              <Button type="button" variant="ghost" onClick={prev}>
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                </svg>
                Anterior
              </Button>
            ) : (
              <div />
            )}
            {step < STEPS.length - 1 ? (
              <Button type="button" onClick={next}>
                Siguiente
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                </svg>
              </Button>
            ) : (
              <Button type="submit" loading={loading} variant="success">
                Crear Perfil y Evaluar
              </Button>
            )}
          </div>
        </form>
      </Card>
    </div>
  );
}
