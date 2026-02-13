"use client";

import { useLanguage } from "@/lib/language-context";

export function LanguageToggle() {
  const { language, setLanguage } = useLanguage();

  return (
    <button
      onClick={() => setLanguage(language === "es" ? "en" : "es")}
      className="rounded-lg px-2 py-1.5 text-xs font-bold text-text-tertiary transition-colors hover:bg-surface-secondary hover:text-text-primary"
    >
      {language === "es" ? "EN" : "ES"}
    </button>
  );
}
