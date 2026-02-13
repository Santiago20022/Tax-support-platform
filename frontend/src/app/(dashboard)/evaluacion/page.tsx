"use client";

import Link from "next/link";
import { useApiQuery } from "@/lib/hooks";
import { useT, useLanguage } from "@/lib/language-context";
import { ROUTES } from "@/lib/constants";
import { formatDateTime } from "@/lib/format";
import type { EvaluationListItem } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { SectionSpinner } from "@/components/ui/spinner";
import { EmptyState } from "@/components/ui/empty-state";

export default function EvaluationsPage() {
  const { data: evaluations, loading } = useApiQuery<EvaluationListItem[]>("/evaluations");
  const t = useT();
  const { locale } = useLanguage();

  if (loading) return <SectionSpinner text={t.evaluation.loadingEvaluations} />;

  if (!evaluations || evaluations.length === 0) {
    return (
      <EmptyState
        icon={
          <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        }
        title={t.evaluation.noEvaluations}
        description={t.evaluation.noEvaluationsDesc}
        action={{ label: t.evaluation.createProfile, href: ROUTES.PROFILES }}
      />
    );
  }

  return (
    <div className="mx-auto max-w-4xl animate-fade-in">
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-text-primary">{t.evaluation.title}</h1>
        <p className="mt-1 text-sm text-text-secondary">
          {t.evaluation.historyDesc}
        </p>
      </div>

      <div className="stagger space-y-4">
        {evaluations.map((ev) => (
          <Link key={ev.id} href={ROUTES.EVALUATION_DETAIL(ev.id)}>
            <Card hover>
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${
                    ev.status === "completed" ? "bg-success-50 text-success-600" : "bg-warning-50 text-warning-600"
                  }`}>
                    {ev.status === "completed" ? (
                      <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm.75-13a.75.75 0 00-1.5 0v5c0 .414.336.75.75.75h4a.75.75 0 000-1.5h-3.25V5z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-text-primary">
                      {formatDateTime(ev.evaluated_at, locale)}
                    </p>
                    <Badge
                      variant={ev.status === "completed" ? "success" : "warning"}
                      size="sm"
                      dot
                      className="mt-1"
                    >
                      {ev.status === "completed" ? t.evaluation.completed : t.evaluation.pendingStatus}
                    </Badge>
                  </div>
                </div>
                {ev.summary && (
                  <div className="flex gap-2">
                    <Badge variant="success">{ev.summary.applies} {t.dashboard.nApply}</Badge>
                    <Badge variant="gray">{ev.summary.does_not_apply} {t.dashboard.nDontApply}</Badge>
                    {ev.summary.conditional > 0 && (
                      <Badge variant="warning">{ev.summary.conditional} cond.</Badge>
                    )}
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
