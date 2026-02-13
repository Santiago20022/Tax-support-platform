"use client";

import { useState } from "react";
import { useApiQuery } from "@/lib/hooks";
import type { ObligationType } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { SectionSpinner } from "@/components/ui/spinner";

export default function ObligationsPage() {
  const { data: obligations, loading } = useApiQuery<ObligationType[]>("/obligations", { auth: false });
  const [filter, setFilter] = useState("");

  if (loading) return <SectionSpinner text="Cargando obligaciones..." />;
  if (!obligations) return null;

  const categories = [...new Set(obligations.map((o) => o.category))].sort();
  const filtered = obligations.filter((o) => (!filter || o.category === filter) && o.is_active);
  const grouped = filtered.reduce<Record<string, ObligationType[]>>((acc, o) => {
    if (!acc[o.category]) acc[o.category] = [];
    acc[o.category].push(o);
    return acc;
  }, {});

  return (
    <div className="mx-auto max-w-4xl animate-fade-in">
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">
          Catálogo de Obligaciones
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          {filtered.length} obligaciones tributarias colombianas
        </p>
      </div>

      {/* Category filter */}
      <div className="mb-6 flex flex-wrap gap-2">
        <button
          onClick={() => setFilter("")}
          className={`rounded-xl px-4 py-2 text-xs font-semibold transition-all duration-200 ${
            !filter
              ? "bg-primary-600 text-white shadow-sm shadow-primary-600/25"
              : "bg-white text-gray-600 border border-gray-200 hover:border-gray-300 hover:bg-gray-50"
          }`}
        >
          Todas
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`rounded-xl px-4 py-2 text-xs font-semibold capitalize transition-all duration-200 ${
              filter === cat
                ? "bg-primary-600 text-white shadow-sm shadow-primary-600/25"
                : "bg-white text-gray-600 border border-gray-200 hover:border-gray-300 hover:bg-gray-50"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Grouped obligations */}
      <div className="space-y-8">
        {Object.entries(grouped).map(([category, obls]) => (
          <div key={category}>
            <h2 className="mb-4 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-400">
              <span className="h-px flex-1 bg-gray-200" />
              {category}
              <span className="h-px flex-1 bg-gray-200" />
            </h2>
            <div className="stagger grid gap-4 sm:grid-cols-2">
              {obls.map((o) => (
                <Card key={o.id} hover>
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="font-semibold text-gray-900 leading-snug">{o.name}</h3>
                    <Badge variant="gray" size="sm">{o.code}</Badge>
                  </div>
                  <p className="mt-2 text-sm leading-relaxed text-gray-500">{o.description}</p>
                  <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1 border-t border-gray-100 pt-3 text-xs text-gray-400">
                    <span className="flex items-center gap-1">
                      <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 0h.008v.008h-.008V7.5z" />
                      </svg>
                      {o.responsible_entity}
                    </span>
                    {o.legal_base && (
                      <span className="flex items-center gap-1">
                        <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
                        </svg>
                        {o.legal_base}
                      </span>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
