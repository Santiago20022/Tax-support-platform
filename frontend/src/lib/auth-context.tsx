"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  type ReactNode,
} from "react";
import { apiClient, setTokens, clearTokens, loadTokens, getAccessToken } from "./api-client";
import type { TokenResponse, LoginRequest, RegisterRequest } from "./types";
import { ROUTES } from "./constants";
import { useRouter } from "next/navigation";

interface AuthUser {
  user_id: string;
  email: string;
  full_name: string;
  tenant_id: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    loadTokens();
    const token = getAccessToken();
    if (token) {
      // Decode JWT payload to restore user info
      try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        const stored = localStorage.getItem("auth_user");
        if (stored) {
          setUser(JSON.parse(stored));
        } else {
          // Minimal info from token
          setUser({
            user_id: payload.sub,
            email: "",
            full_name: "",
            tenant_id: payload.tenant_id || "",
          });
        }
      } catch {
        clearTokens();
      }
    }
    setIsLoading(false);
  }, []);

  const handleAuthResponse = useCallback((data: TokenResponse) => {
    setTokens(data.access_token, data.refresh_token);
    const authUser: AuthUser = {
      user_id: data.user_id,
      email: data.email,
      full_name: data.full_name,
      tenant_id: data.tenant_id,
    };
    setUser(authUser);
    localStorage.setItem("auth_user", JSON.stringify(authUser));
  }, []);

  const login = useCallback(
    async (data: LoginRequest) => {
      const res = await apiClient<TokenResponse>("/auth/login", {
        method: "POST",
        body: data,
        auth: false,
      });
      handleAuthResponse(res);
    },
    [handleAuthResponse],
  );

  const register = useCallback(
    async (data: RegisterRequest) => {
      const res = await apiClient<TokenResponse>("/auth/register", {
        method: "POST",
        body: data,
        auth: false,
      });
      handleAuthResponse(res);
    },
    [handleAuthResponse],
  );

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
    localStorage.removeItem("auth_user");
    router.push(ROUTES.LOGIN);
  }, [router]);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
