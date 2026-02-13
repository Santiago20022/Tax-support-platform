"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { ROUTES } from "@/lib/constants";
import { ApiError } from "@/lib/api-client";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert } from "@/components/ui/alert";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden");
      return;
    }
    if (password.length < 8) {
      setError("La contraseña debe tener al menos 8 caracteres");
      return;
    }

    setLoading(true);
    try {
      await register({ email, password, full_name: fullName });
      router.push(ROUTES.DASHBOARD);
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : "Error al registrarse");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="animate-fade-in">
      {/* Mobile logo */}
      <div className="mb-8 flex items-center gap-3 lg:hidden">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 shadow-sm shadow-primary-500/25">
          <svg className="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
          </svg>
        </div>
        <span className="text-xl font-bold text-gray-900">Tributario</span>
      </div>

      <h1 className="text-2xl font-bold tracking-tight text-gray-900">
        Crear cuenta
      </h1>
      <p className="mt-2 text-sm text-gray-500">
        Regístrate para evaluar tu perfil tributario
      </p>

      {error && (
        <Alert variant="error" className="mt-6">{error}</Alert>
      )}

      <form onSubmit={handleSubmit} className="mt-8 space-y-5">
        <Input
          id="fullName"
          label="Nombre completo"
          type="text"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="Tu nombre completo"
          required
          autoComplete="name"
        />
        <Input
          id="email"
          label="Correo electrónico"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="nombre@correo.com"
          required
          autoComplete="email"
        />
        <Input
          id="password"
          label="Contraseña"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Mínimo 8 caracteres"
          required
          autoComplete="new-password"
          hint="Mínimo 8 caracteres"
        />
        <Input
          id="confirmPassword"
          label="Confirmar contraseña"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Repite tu contraseña"
          required
          autoComplete="new-password"
        />
        <Button type="submit" loading={loading} className="w-full" size="lg">
          Crear cuenta
        </Button>
      </form>

      <p className="mt-8 text-center text-sm text-gray-500">
        ¿Ya tienes cuenta?{" "}
        <Link
          href={ROUTES.LOGIN}
          className="font-semibold text-primary-600 transition-colors hover:text-primary-500"
        >
          Inicia sesión
        </Link>
      </p>
    </div>
  );
}
