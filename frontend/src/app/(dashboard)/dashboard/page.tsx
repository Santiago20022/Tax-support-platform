"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useApiQuery } from "@/lib/hooks";
import { ROUTES } from "@/lib/constants";
import type { ProfileResponse, EvaluationListItem, CalendarEntry } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const quickActions = [
  {
    title: "Perfil Tributario",
    description: "Crea o administra tu perfil fiscal",
    href: ROUTES.PROFILES,
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      </svg>
    ),
    color: "from-primary-500 to-primary-600",
    shadowColor: "shadow-primary-500/20",
  },
  {
    title: "Evaluación",
    description: "Consulta qué obligaciones te aplican",
    href: ROUTES.EVALUATIONS,
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    color: "from-success-500 to-success-600",
    shadowColor: "shadow-success-500/20",
  },
  {
    title: "Calendario",
    description: "Fechas de vencimiento y checklist",
    href: ROUTES.CALENDAR,
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
      </svg>
    ),
    color: "from-warning-500 to-warning-600",
    shadowColor: "shadow-warning-500/20",
  },
  {
    title: "Obligaciones",
    description: "Catálogo de obligaciones tributarias",
    href: ROUTES.OBLIGATIONS,
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
      </svg>
    ),
    color: "from-gray-600 to-gray-700",
    shadowColor: "shadow-gray-500/20",
  },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const { data: profiles } = useApiQuery<ProfileResponse[]>("/profiles");
  const { data: evaluations } = useApiQuery<EvaluationListItem[]>("/evaluations");
  const { data: calendar } = useApiQuery<CalendarEntry[]>("/calendar");

  const profileCount = profiles?.length ?? 0;
  const latestEval = evaluations?.[0];
  const pendingCalendar = calendar?.filter((e) => !e.is_completed).length ?? 0;

  return (
    <div className="mx-auto max-w-5xl animate-fade-in">
      {/* Welcome header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">
          Hola, {user?.full_name?.split(" ")[0] || "Usuario"}
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Aquí tienes un resumen de tu situación tributaria
        </p>
      </div>

      {/* Stats row */}
      <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Card className="flex items-center gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary-50">
            <span className="text-xl font-bold text-primary-600">{profileCount}</span>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">Perfiles</p>
            <p className="text-xs text-gray-500">Perfiles tributarios creados</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-success-50">
            <span className="text-xl font-bold text-success-600">
              {latestEval?.summary?.applies ?? "—"}
            </span>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">Aplican</p>
            <p className="text-xs text-gray-500">Obligaciones identificadas</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-warning-50">
            <span className="text-xl font-bold text-warning-600">{pendingCalendar}</span>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">Pendientes</p>
            <p className="text-xs text-gray-500">Fechas en calendario</p>
          </div>
        </Card>
      </div>

      {/* Quick actions */}
      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-gray-400">
        Acciones rápidas
      </h2>
      <div className="stagger grid gap-4 sm:grid-cols-2">
        {quickActions.map((action) => (
          <Link key={action.href} href={action.href}>
            <Card hover className="group flex items-start gap-4">
              <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br ${action.color} shadow-md ${action.shadowColor} text-white transition-transform duration-200 group-hover:scale-105`}>
                {action.icon}
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">
                  {action.title}
                </h3>
                <p className="mt-0.5 text-sm text-gray-500">
                  {action.description}
                </p>
              </div>
            </Card>
          </Link>
        ))}
      </div>

      {/* Latest evaluation summary */}
      {latestEval?.summary && (
        <div className="mt-8">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-gray-400">
            Última evaluación
          </h2>
          <Card>
            <div className="flex flex-wrap items-center gap-3">
              <Badge variant="success" dot>{latestEval.summary.applies} aplican</Badge>
              <Badge variant="gray" dot>{latestEval.summary.does_not_apply} no aplican</Badge>
              {latestEval.summary.conditional > 0 && (
                <Badge variant="warning" dot>{latestEval.summary.conditional} condicional</Badge>
              )}
              {latestEval.summary.needs_more_info > 0 && (
                <Badge variant="info" dot>{latestEval.summary.needs_more_info} requiere info</Badge>
              )}
              <Link
                href={ROUTES.EVALUATION_DETAIL(latestEval.id)}
                className="ml-auto text-sm font-semibold text-primary-600 hover:text-primary-500"
              >
                Ver detalle
              </Link>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
