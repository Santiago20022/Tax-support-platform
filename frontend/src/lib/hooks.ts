"use client";

import { useState, useEffect, useCallback } from "react";
import { apiClient, ApiError } from "./api-client";

interface UseApiQueryResult<T> {
  data: T | null;
  loading: boolean;
  error: string;
  refetch: () => void;
}

export function useApiQuery<T>(
  path: string,
  options?: { auth?: boolean; enabled?: boolean },
): UseApiQueryResult<T> {
  const { auth = true, enabled = true } = options ?? {};
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetch = useCallback(() => {
    if (!enabled) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError("");
    apiClient<T>(path, { auth })
      .then(setData)
      .catch((err) => {
        setError(err instanceof ApiError ? err.detail : "Error de conexión");
      })
      .finally(() => setLoading(false));
  }, [path, auth, enabled]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { data, loading, error, refetch: fetch };
}

interface UseApiMutationResult<TReq, TRes> {
  mutate: (body: TReq) => Promise<TRes>;
  loading: boolean;
  error: string;
}

export function useApiMutation<TReq, TRes>(
  path: string,
  method: string = "POST",
): UseApiMutationResult<TReq, TRes> {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const mutate = useCallback(
    async (body: TReq): Promise<TRes> => {
      setLoading(true);
      setError("");
      try {
        const res = await apiClient<TRes>(path, { method, body });
        return res;
      } catch (err) {
        const msg = err instanceof ApiError ? err.detail : "Error inesperado";
        setError(msg);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [path, method],
  );

  return { mutate, loading, error };
}
