import type { EvaluationSummary } from "@/lib/types";

interface ResultSummaryProps {
  summary: EvaluationSummary;
}

const items = [
  { key: "applies" as const, label: "Aplican", icon: "check", color: "from-success-500 to-success-600", bg: "bg-success-50", text: "text-success-700" },
  { key: "does_not_apply" as const, label: "No aplican", icon: "x", color: "from-gray-400 to-gray-500", bg: "bg-gray-50", text: "text-gray-600" },
  { key: "conditional" as const, label: "Condicional", icon: "warning", color: "from-warning-500 to-warning-600", bg: "bg-warning-50", text: "text-warning-700" },
  { key: "needs_more_info" as const, label: "Requiere info", icon: "info", color: "from-primary-500 to-primary-600", bg: "bg-primary-50", text: "text-primary-700" },
];

export function ResultSummary({ summary }: ResultSummaryProps) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {items.map((item) => (
        <div
          key={item.key}
          className={`relative overflow-hidden rounded-2xl ${item.bg} p-4`}
        >
          <div className={`text-3xl font-bold ${item.text}`}>
            {summary[item.key]}
          </div>
          <div className={`mt-0.5 text-xs font-semibold ${item.text} opacity-70`}>
            {item.label}
          </div>
          {/* Decorative gradient circle */}
          <div className={`absolute -right-3 -top-3 h-12 w-12 rounded-full bg-gradient-to-br ${item.color} opacity-10`} />
        </div>
      ))}
    </div>
  );
}
