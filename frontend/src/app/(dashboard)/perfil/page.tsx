"use client";

import { useState } from "react";
import Link from "next/link";
import { useApiQuery } from "@/lib/hooks";
import { ROUTES, PERSONA_TYPES, REGIMES } from "@/lib/constants";
import { formatCOP } from "@/lib/format";
import type { ProfileResponse } from "@/lib/types";
import { ProfileWizard } from "@/components/profile/profile-wizard";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { SectionSpinner } from "@/components/ui/spinner";
import { EmptyState } from "@/components/ui/empty-state";

export default function ProfilesPage() {
  const { data: profiles, loading } = useApiQuery<ProfileResponse[]>("/profiles");
  const [showWizard, setShowWizard] = useState(false);

  if (loading) return <SectionSpinner text="Cargando perfiles..." />;

  if (showWizard || (profiles && profiles.length === 0)) {
    return (
      <div className="mx-auto max-w-2xl animate-fade-in">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-gray-900">
              Nuevo Perfil Tributario
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              Completa los datos para evaluar tus obligaciones
            </p>
          </div>
          {profiles && profiles.length > 0 && (
            <Button variant="secondary" size="sm" onClick={() => setShowWizard(false)}>
              Volver
            </Button>
          )}
        </div>
        <ProfileWizard />
      </div>
    );
  }

  if (!profiles || profiles.length === 0) {
    return (
      <EmptyState
        icon={
          <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
          </svg>
        }
        title="Sin perfiles"
        description="Crea tu primer perfil tributario para evaluar qué obligaciones te aplican."
        action={{ label: "Crear Perfil", onClick: () => setShowWizard(true) }}
      />
    );
  }

  return (
    <div className="mx-auto max-w-4xl animate-fade-in">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">
            Perfiles Tributarios
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            {profiles.length} perfil{profiles.length !== 1 ? "es" : ""} creado{profiles.length !== 1 ? "s" : ""}
          </p>
        </div>
        <Button onClick={() => setShowWizard(true)}>
          Nuevo Perfil
        </Button>
      </div>

      <div className="stagger space-y-4">
        {profiles.map((profile) => (
          <Link key={profile.id} href={ROUTES.PROFILE_DETAIL(profile.id)}>
            <Card hover>
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary-50 text-primary-600">
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                    </svg>
                  </div>
                  <div>
                    <h2 className="font-semibold text-gray-900">
                      {PERSONA_TYPES[profile.persona_type] || profile.persona_type}
                    </h2>
                    <p className="text-sm text-gray-500">
                      {REGIMES[profile.regime] || profile.regime}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Badge variant={profile.is_iva_responsable ? "info" : "gray"} dot>
                    {profile.is_iva_responsable ? "IVA Responsable" : "No IVA"}
                  </Badge>
                </div>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-4 border-t border-gray-100 pt-4 text-sm sm:grid-cols-4">
                <div>
                  <span className="text-xs font-medium text-gray-400">Ingresos</span>
                  <p className="mt-0.5 font-semibold text-gray-900">
                    {formatCOP(profile.ingresos_brutos_cop)}
                  </p>
                </div>
                <div>
                  <span className="text-xs font-medium text-gray-400">Patrimonio</span>
                  <p className="mt-0.5 font-semibold text-gray-900">
                    {formatCOP(profile.patrimonio_bruto_cop)}
                  </p>
                </div>
                {profile.city && (
                  <div>
                    <span className="text-xs font-medium text-gray-400">Ciudad</span>
                    <p className="mt-0.5 font-semibold text-gray-900">{profile.city}</p>
                  </div>
                )}
                {profile.has_employees && (
                  <div>
                    <span className="text-xs font-medium text-gray-400">Empleados</span>
                    <p className="mt-0.5 font-semibold text-gray-900">{profile.employee_count}</p>
                  </div>
                )}
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
