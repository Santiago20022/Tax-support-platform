"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from "react";
import type { Translations } from "./i18n/types";
import { es } from "./i18n/es";
import { en } from "./i18n/en";

type Language = "es" | "en";

interface LanguageContextValue {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: Translations;
  locale: string;
}

const translations: Record<Language, Translations> = { es, en };
const locales: Record<Language, string> = { es: "es-CO", en: "en-US" };

const LanguageContext = createContext<LanguageContextValue>({
  language: "es",
  setLanguage: () => {},
  t: es,
  locale: "es-CO",
});

export function useLanguage() {
  return useContext(LanguageContext);
}

export function useT() {
  return useContext(LanguageContext).t;
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLangState] = useState<Language>("es");

  useEffect(() => {
    const stored = localStorage.getItem("language") as Language | null;
    if (stored && (stored === "es" || stored === "en")) {
      setLangState(stored);
    }
  }, []);

  function setLanguage(lang: Language) {
    setLangState(lang);
    localStorage.setItem("language", lang);
    document.documentElement.lang = lang;
  }

  return (
    <LanguageContext.Provider
      value={{
        language,
        setLanguage,
        t: translations[language],
        locale: locales[language],
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}
