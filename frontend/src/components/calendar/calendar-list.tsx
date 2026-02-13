"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api-client";
import { formatDate } from "@/lib/format";
import { useT, useLanguage } from "@/lib/language-context";
import type { CalendarEntry } from "@/lib/types";
import { Badge } from "@/components/ui/badge";

interface CalendarListProps {
  entries: CalendarEntry[];
  onUpdate: (updated: CalendarEntry) => void;
}

export function CalendarList({ entries, onUpdate }: CalendarListProps) {
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const t = useT();
  const { locale } = useLanguage();

  const grouped = entries.reduce<Record<string, CalendarEntry[]>>((acc, e) => {
    const date = new Date(e.due_date);
    const key = date.toLocaleDateString(locale, { year: "numeric", month: "long" });
    if (!acc[key]) acc[key] = [];
    acc[key].push(e);
    return acc;
  }, {});

  async function toggleComplete(entry: CalendarEntry) {
    setLoadingId(entry.id);
    try {
      const updated = await apiClient<CalendarEntry>(`/calendar/${entry.id}`, {
        method: "PATCH",
        body: { is_completed: !entry.is_completed },
      });
      onUpdate(updated);
    } catch {
      // ignore
    } finally {
      setLoadingId(null);
    }
  }

  return (
    <div className="space-y-8">
      {Object.entries(grouped).map(([month, monthEntries]) => (
        <div key={month}>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-text-tertiary">
            {month}
          </h3>
          <div className="stagger space-y-2">
            {monthEntries.map((entry) => {
              const isPast = !entry.is_completed && new Date(entry.due_date) < new Date();
              return (
                <div
                  key={entry.id}
                  className={`group flex items-start gap-4 rounded-2xl border p-4 transition-all duration-200 ${
                    entry.is_completed
                      ? "border-border bg-surface-inset/50"
                      : isPast
                        ? "border-danger-200 bg-danger-50/50"
                        : "border-border bg-surface hover:border-border-strong hover:shadow-sm"
                  }`}
                >
                  <button
                    onClick={() => toggleComplete(entry)}
                    disabled={loadingId === entry.id}
                    className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-md border-2 transition-all duration-200 ${
                      entry.is_completed
                        ? "border-success-500 bg-success-500 text-white"
                        : "border-text-tertiary hover:border-primary-400"
                    } ${loadingId === entry.id ? "animate-pulse" : ""}`}
                  >
                    {entry.is_completed && (
                      <svg className="h-3 w-3" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.5 6.5l2.5 2.5 4.5-5" />
                      </svg>
                    )}
                  </button>
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm font-medium leading-snug ${
                      entry.is_completed ? "text-text-tertiary line-through" : "text-text-primary"
                    }`}>
                      {entry.title}
                    </p>
                    <div className="mt-2 flex flex-wrap items-center gap-2">
                      <span className={`text-xs ${isPast && !entry.is_completed ? "font-semibold text-danger-600" : "text-text-secondary"}`}>
                        {formatDate(entry.due_date, locale)}
                      </span>
                      <Badge variant="gray" size="sm">
                        {t.labels.periodicities[entry.periodicity] || entry.periodicity}
                      </Badge>
                      {isPast && !entry.is_completed && (
                        <Badge variant="danger" size="sm" dot>{t.calendarPage.overdueLabel}</Badge>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
