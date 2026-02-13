"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { apiClient, ApiError } from "@/lib/api-client";
import { useApiQuery } from "@/lib/hooks";
import { useT, useLanguage } from "@/lib/language-context";
import { ROUTES } from "@/lib/constants";
import { formatCOP } from "@/lib/format";
import type { ProfileResponse, EvaluationResponse } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { SectionSpinner } from "@/components/ui/spinner";
import { Alert } from "@/components/ui/alert";

export default function ProfileDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const t = useT();
  const { locale } = useLanguage();
  const { data: profile, loading, error: loadError } = useApiQuery<ProfileResponse>(`/profiles/${id}`);
  const [evaluating, setEvaluating] = useState(false);
  const [error, setError] = useState("");

  async function handleEvaluate() {
    setEvaluating(true);
    setError("");
    try {
      const evaluation = await apiClient<EvaluationResponse>("/evaluations", {
        method: "POST",
        body: { tax_profile_id: id },
      });
      router.push(ROUTES.EVALUATION_DETAIL(evaluation.id));
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : t.profile.evaluateError);
      setEvaluating(false);
    }
  }

  async function handleDelete() {
    if (!confirm(t.profile.deleteConfirm)) return;
    try {
      await apiClient(`/profiles/${id}`, { method: "DELETE" });
      router.push(ROUTES.PROFILES);
    } catch {
      setError(t.profile.deleteError);
    }
  }

  if (loading) return <SectionSpinner text={t.profile.loadingProfile} />;
  if (loadError || !profile) return <Alert variant="error">{loadError || t.profile.notFound}</Alert>;

  const fields = [
    { label: t.profileFields.personaType, value: t.labels.personaTypes[profile.persona_type] || profile.persona_type },
    { label: t.profileFields.regime, value: t.labels.regimes[profile.regime] || profile.regime },
    { label: t.profileFields.ivaResponsable, value: profile.is_iva_responsable ? t.common.yes : t.common.no },
    { label: t.profileFields.grossIncome, value: formatCOP(profile.ingresos_brutos_cop, locale) },
    { label: t.profileFields.grossWealth, value: formatCOP(profile.patrimonio_bruto_cop, locale) },
    { label: t.profileFields.deposits, value: formatCOP(profile.consignaciones_cop, locale) },
    { label: t.profileFields.purchases, value: formatCOP(profile.compras_consumos_cop, locale) },
    { label: t.profileFields.ciiu, value: profile.economic_activity_ciiu || "—" },
    { label: t.profileFields.city, value: profile.city || "—" },
    { label: t.profileFields.department, value: profile.department || "—" },
    { label: t.profileFields.employees, value: profile.has_employees ? `${profile.employee_count}` : t.common.no },
    { label: t.profileFields.rut, value: profile.has_rut ? t.common.yes : t.common.no },
    { label: t.profileFields.commerceReg, value: profile.has_comercio_registration ? t.common.yes : t.common.no },
    { label: t.profileFields.nitLastDigit, value: profile.nit_last_digit?.toString() ?? "—" },
  ];

  return (
    <div className="mx-auto max-w-2xl animate-fade-in space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-text-primary">{t.profile.detail}</h1>
          <p className="mt-1 text-sm text-text-secondary">
            {t.labels.personaTypes[profile.persona_type]} — {t.labels.regimes[profile.regime]}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => router.push(ROUTES.PROFILES)}>
            {t.common.back}
          </Button>
          <Button variant="danger" size="sm" onClick={handleDelete}>
            {t.common.delete}
          </Button>
        </div>
      </div>

      {error && <Alert variant="error">{error}</Alert>}

      <Card>
        <div className="mb-5 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600">
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
            </svg>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-text-primary">
              {t.labels.personaTypes[profile.persona_type]}
            </h2>
            <Badge variant={profile.is_iva_responsable ? "info" : "gray"} dot>
              {profile.is_iva_responsable ? t.profile.ivaResp : t.profile.ivaNotResp}
            </Badge>
          </div>
        </div>
        <dl className="grid grid-cols-2 gap-x-6 gap-y-4 border-t border-border pt-5">
          {fields.map((f) => (
            <div key={f.label}>
              <dt className="text-xs font-medium text-text-tertiary">{f.label}</dt>
              <dd className="mt-0.5 text-sm font-semibold text-text-primary">{f.value}</dd>
            </div>
          ))}
        </dl>
      </Card>

      <Button onClick={handleEvaluate} loading={evaluating} className="w-full" size="lg" variant="success">
        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {t.profile.evaluateBtn}
      </Button>
    </div>
  );
}
