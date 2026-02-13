"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { apiClient, ApiError } from "@/lib/api-client";
import { useApiQuery } from "@/lib/hooks";
import { ROUTES, PERSONA_TYPES, REGIMES } from "@/lib/constants";
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
      setError(err instanceof ApiError ? err.detail : "Error al evaluar");
      setEvaluating(false);
    }
  }

  async function handleDelete() {
    if (!confirm("¿Estás seguro de eliminar este perfil?")) return;
    try {
      await apiClient(`/profiles/${id}`, { method: "DELETE" });
      router.push(ROUTES.PROFILES);
    } catch {
      setError("Error al eliminar el perfil");
    }
  }

  if (loading) return <SectionSpinner text="Cargando perfil..." />;
  if (loadError || !profile) return <Alert variant="error">{loadError || "Perfil no encontrado"}</Alert>;

  const fields = [
    { label: "Tipo de persona", value: PERSONA_TYPES[profile.persona_type] || profile.persona_type },
    { label: "Régimen", value: REGIMES[profile.regime] || profile.regime },
    { label: "Responsable IVA", value: profile.is_iva_responsable ? "Sí" : "No" },
    { label: "Ingresos brutos", value: formatCOP(profile.ingresos_brutos_cop) },
    { label: "Patrimonio bruto", value: formatCOP(profile.patrimonio_bruto_cop) },
    { label: "Consignaciones", value: formatCOP(profile.consignaciones_cop) },
    { label: "Compras y consumos", value: formatCOP(profile.compras_consumos_cop) },
    { label: "CIIU", value: profile.economic_activity_ciiu || "—" },
    { label: "Ciudad", value: profile.city || "—" },
    { label: "Departamento", value: profile.department || "—" },
    { label: "Empleados", value: profile.has_employees ? `${profile.employee_count}` : "No" },
    { label: "RUT", value: profile.has_rut ? "Sí" : "No" },
    { label: "Registro mercantil", value: profile.has_comercio_registration ? "Sí" : "No" },
    { label: "Último dígito NIT", value: profile.nit_last_digit?.toString() ?? "—" },
  ];

  return (
    <div className="mx-auto max-w-2xl animate-fade-in space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Detalle del Perfil</h1>
          <p className="mt-1 text-sm text-gray-500">
            {PERSONA_TYPES[profile.persona_type]} — {REGIMES[profile.regime]}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => router.push(ROUTES.PROFILES)}>
            Volver
          </Button>
          <Button variant="danger" size="sm" onClick={handleDelete}>
            Eliminar
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
            <h2 className="text-lg font-semibold text-gray-900">
              {PERSONA_TYPES[profile.persona_type]}
            </h2>
            <Badge variant={profile.is_iva_responsable ? "info" : "gray"} dot>
              {profile.is_iva_responsable ? "IVA Responsable" : "No responsable de IVA"}
            </Badge>
          </div>
        </div>
        <dl className="grid grid-cols-2 gap-x-6 gap-y-4 border-t border-gray-100 pt-5">
          {fields.map((f) => (
            <div key={f.label}>
              <dt className="text-xs font-medium text-gray-400">{f.label}</dt>
              <dd className="mt-0.5 text-sm font-semibold text-gray-900">{f.value}</dd>
            </div>
          ))}
        </dl>
      </Card>

      <Button onClick={handleEvaluate} loading={evaluating} className="w-full" size="lg" variant="success">
        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Evaluar Obligaciones Tributarias
      </Button>
    </div>
  );
}
