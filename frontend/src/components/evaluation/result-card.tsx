"use client";

import { useState } from "react";
import type { EvaluationResult } from "@/lib/types";
import { RESULT_LABELS, PERIODICITY_LABELS } from "@/lib/constants";
import { Badge } from "@/components/ui/badge";

interface ResultCardProps {
  result: EvaluationResult;
}

const resultBadgeVariant: Record<string, "success" | "danger" | "warning" | "info" | "gray"> = {
  applies: "success",
  does_not_apply: "gray",
  conditional: "warning",
  needs_more_info: "info",
};

const resultIcons: Record<string, React.ReactNode> = {
  applies: (
    <svg className="h-5 w-5 text-success-500" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clipRule="evenodd" />
    </svg>
  ),
  does_not_apply: (
    <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clipRule="evenodd" />
    </svg>
  ),
  conditional: (
    <svg className="h-5 w-5 text-warning-500" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 6a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 6zm0 9a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
    </svg>
  ),
  needs_more_info: (
    <svg className="h-5 w-5 text-primary-500" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z" clipRule="evenodd" />
    </svg>
  ),
};

export function ResultCard({ result }: ResultCardProps) {
  const [expanded, setExpanded] = useState(false);
  const hasDetails = result.legal_references.length > 0 || result.conditions_evaluated.length > 0;

  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm transition-all duration-200 hover:shadow-md">
      <div className="flex items-start gap-3">
        <div className="mt-0.5 shrink-0">
          {resultIcons[result.result] || resultIcons.does_not_apply}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-start justify-between gap-2">
            <div>
              <h3 className="font-semibold text-gray-900 leading-snug">
                {result.obligation.name}
              </h3>
              {result.obligation.category && (
                <p className="mt-0.5 text-xs text-gray-400">{result.obligation.category}</p>
              )}
            </div>
            <div className="flex shrink-0 items-center gap-2">
              {result.periodicity && (
                <Badge variant="gray" size="sm">
                  {PERIODICITY_LABELS[result.periodicity] || result.periodicity}
                </Badge>
              )}
              <Badge variant={resultBadgeVariant[result.result] || "gray"}>
                {RESULT_LABELS[result.result] || result.result}
              </Badge>
            </div>
          </div>

          <p className="mt-2.5 text-sm leading-relaxed text-gray-600">{result.explanation}</p>

          {hasDetails && (
            <button
              type="button"
              onClick={() => setExpanded(!expanded)}
              className="mt-3 inline-flex items-center gap-1 text-xs font-semibold text-primary-600 transition-colors hover:text-primary-500"
            >
              {expanded ? "Ocultar detalles" : "Ver detalles"}
              <svg
                className={`h-3.5 w-3.5 transition-transform duration-200 ${expanded ? "rotate-180" : ""}`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </button>
          )}

          {expanded && (
            <div className="mt-4 space-y-4 animate-fade-in">
              {result.legal_references.length > 0 && (
                <div className="rounded-xl bg-gray-50 p-3">
                  <h4 className="mb-2 text-[11px] font-semibold uppercase tracking-wider text-gray-400">
                    Referencias legales
                  </h4>
                  <ul className="space-y-1">
                    {result.legal_references.map((ref, i) => (
                      <li key={i} className="text-xs text-gray-600 leading-relaxed">{ref}</li>
                    ))}
                  </ul>
                </div>
              )}
              {result.conditions_evaluated.length > 0 && (
                <div className="rounded-xl bg-gray-50 p-3">
                  <h4 className="mb-2 text-[11px] font-semibold uppercase tracking-wider text-gray-400">
                    Condiciones evaluadas
                  </h4>
                  <ul className="space-y-1.5">
                    {result.conditions_evaluated.map((cond, i) => (
                      <li key={i} className="flex items-center gap-2 text-xs text-gray-600">
                        <span
                          className={`inline-block h-2 w-2 shrink-0 rounded-full ${
                            (cond as Record<string, unknown>).met ? "bg-success-500" : "bg-danger-500"
                          }`}
                        />
                        {String(cond.description || cond.field || "")}{" "}
                        {String(cond.operator || "")} {String(cond.value ?? "")}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
