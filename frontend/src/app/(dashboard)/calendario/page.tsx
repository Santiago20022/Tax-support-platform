"use client";

import { useState, useEffect } from "react";
import { useApiQuery } from "@/lib/hooks";
import type { CalendarEntry } from "@/lib/types";
import { CalendarList } from "@/components/calendar/calendar-list";
import { SectionSpinner } from "@/components/ui/spinner";
import { EmptyState } from "@/components/ui/empty-state";
import { ROUTES } from "@/lib/constants";

export default function CalendarPage() {
  const { data, loading } = useApiQuery<CalendarEntry[]>("/calendar");
  const [entries, setEntries] = useState<CalendarEntry[]>([]);

  useEffect(() => {
    if (data) setEntries(data);
  }, [data]);

  function handleUpdate(updated: CalendarEntry) {
    setEntries((prev) => prev.map((e) => (e.id === updated.id ? updated : e)));
  }

  if (loading) return <SectionSpinner text="Cargando calendario..." />;

  if (entries.length === 0) {
    return (
      <EmptyState
        icon={
          <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
          </svg>
        }
        title="Calendario vacío"
        description="Evalúa un perfil tributario para generar tu calendario de vencimientos."
        action={{ label: "Ir a Perfiles", href: ROUTES.PROFILES }}
      />
    );
  }

  const pending = entries.filter((e) => !e.is_completed).length;
  const completed = entries.filter((e) => e.is_completed).length;
  const overdue = entries.filter(
    (e) => !e.is_completed && new Date(e.due_date) < new Date(),
  ).length;

  return (
    <div className="mx-auto max-w-3xl animate-fade-in">
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">
          Calendario Tributario
        </h1>
        <div className="mt-2 flex flex-wrap gap-3">
          <span className="inline-flex items-center gap-1.5 text-sm text-gray-500">
            <span className="h-2 w-2 rounded-full bg-primary-500" />
            {pending} pendiente{pending !== 1 ? "s" : ""}
          </span>
          <span className="inline-flex items-center gap-1.5 text-sm text-gray-500">
            <span className="h-2 w-2 rounded-full bg-success-500" />
            {completed} completada{completed !== 1 ? "s" : ""}
          </span>
          {overdue > 0 && (
            <span className="inline-flex items-center gap-1.5 text-sm font-medium text-danger-600">
              <span className="h-2 w-2 rounded-full bg-danger-500" />
              {overdue} vencida{overdue !== 1 ? "s" : ""}
            </span>
          )}
        </div>
      </div>

      <CalendarList entries={entries} onUpdate={handleUpdate} />
    </div>
  );
}
