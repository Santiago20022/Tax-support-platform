"use client";

import { useParams, useRouter } from "next/navigation";
import { useApiQuery } from "@/lib/hooks";
import { ROUTES } from "@/lib/constants";
import { formatDateTime } from "@/lib/format";
import type { EvaluationResponse } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { SectionSpinner } from "@/components/ui/spinner";
import { Alert } from "@/components/ui/alert";
import { ResultSummary } from "@/components/evaluation/result-summary";
import { ResultCard } from "@/components/evaluation/result-card";
import { DisclaimerBanner } from "@/components/evaluation/disclaimer-banner";

export default function EvaluationDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const { data: evaluation, loading, error } = useApiQuery<EvaluationResponse>(
    `/evaluations/${id}`,
  );

  if (loading) return <SectionSpinner text="Cargando resultados..." />;
  if (error || !evaluation) return <Alert variant="error">{error || "Evaluación no encontrada"}</Alert>;

  const grouped = evaluation.results.reduce<Record<string, typeof evaluation.results>>(
    (acc, r) => {
      const cat = r.obligation.category || "Otros";
      if (!acc[cat]) acc[cat] = [];
      acc[cat].push(r);
      return acc;
    },
    {},
  );

  return (
    <div className="mx-auto max-w-4xl animate-fade-in">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">
            Resultados
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            {formatDateTime(evaluation.evaluated_at)}
            {evaluation.fiscal_year && (
              <span className="ml-2 inline-flex items-center rounded-md bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600">
                Año {evaluation.fiscal_year}
              </span>
            )}
          </p>
        </div>
        <Button variant="secondary" size="sm" onClick={() => router.push(ROUTES.EVALUATIONS)}>
          Volver
        </Button>
      </div>

      <div className="space-y-6">
        <DisclaimerBanner text={evaluation.disclaimer?.text} />

        {evaluation.summary && <ResultSummary summary={evaluation.summary} />}

        {Object.entries(grouped).map(([category, results]) => (
          <div key={category}>
            <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-gray-400">
              <span className="h-px flex-1 bg-gray-200" />
              {category}
              <span className="h-px flex-1 bg-gray-200" />
            </h2>
            <div className="stagger space-y-3">
              {results.map((r, i) => (
                <ResultCard key={`${r.obligation.code}-${i}`} result={r} />
              ))}
            </div>
          </div>
        ))}

        <DisclaimerBanner text={evaluation.disclaimer?.text} />
      </div>
    </div>
  );
}
