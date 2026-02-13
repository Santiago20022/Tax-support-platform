"use client";

import { useState } from "react";
import Link from "next/link";
import { useApiQuery } from "@/lib/hooks";
import { useT, useLanguage } from "@/lib/language-context";
import { ROUTES } from "@/lib/constants";
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
  const t = useT();
  const { locale } = useLanguage();

  if (loading) return <SectionSpinner text={t.profile.loadingProfiles} />;

  if (showWizard || (profiles && profiles.length === 0)) {
    return (
      <div className="mx-auto max-w-2xl animate-fade-in">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-text-primary">
              {t.profile.newTitle}
            </h1>
            <p className="mt-1 text-sm text-text-secondary">
              {t.profile.completeData}
            </p>
          </div>
          {profiles && profiles.length > 0 && (
            <Button variant="secondary" size="sm" onClick={() => setShowWizard(false)}>
              {t.common.back}
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
        title={t.profile.noProfiles}
        description={t.profile.noProfilesDesc}
        action={{ label: t.profile.createProfile, onClick: () => setShowWizard(true) }}
      />
    );
  }

  return (
    <div className="mx-auto max-w-4xl animate-fade-in">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-text-primary">
            {t.profile.title}
          </h1>
          <p className="mt-1 text-sm text-text-secondary">
            {profiles.length} {profiles.length !== 1 ? t.profile.profilePlural : t.profile.profileSingular} {profiles.length !== 1 ? t.profile.createdPlural : t.profile.createdSingular}
          </p>
        </div>
        <Button onClick={() => setShowWizard(true)}>
          {t.profile.newProfile}
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
                    <h2 className="font-semibold text-text-primary">
                      {t.labels.personaTypes[profile.persona_type] || profile.persona_type}
                    </h2>
                    <p className="text-sm text-text-secondary">
                      {t.labels.regimes[profile.regime] || profile.regime}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Badge variant={profile.is_iva_responsable ? "info" : "gray"} dot>
                    {profile.is_iva_responsable ? t.profile.ivaResp : t.profile.noIva}
                  </Badge>
                </div>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-4 border-t border-border pt-4 text-sm sm:grid-cols-4">
                <div>
                  <span className="text-xs font-medium text-text-tertiary">{t.profile.income}</span>
                  <p className="mt-0.5 font-semibold text-text-primary">
                    {formatCOP(profile.ingresos_brutos_cop, locale)}
                  </p>
                </div>
                <div>
                  <span className="text-xs font-medium text-text-tertiary">{t.profile.wealth}</span>
                  <p className="mt-0.5 font-semibold text-text-primary">
                    {formatCOP(profile.patrimonio_bruto_cop, locale)}
                  </p>
                </div>
                {profile.city && (
                  <div>
                    <span className="text-xs font-medium text-text-tertiary">{t.profile.city}</span>
                    <p className="mt-0.5 font-semibold text-text-primary">{profile.city}</p>
                  </div>
                )}
                {profile.has_employees && (
                  <div>
                    <span className="text-xs font-medium text-text-tertiary">{t.profile.employees}</span>
                    <p className="mt-0.5 font-semibold text-text-primary">{profile.employee_count}</p>
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
