const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "/api";

export function getToken() {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("koyunchat_token");
}

export function setToken(token: string) {
  window.localStorage.setItem("koyunchat_token", token);
}

export function clearToken() {
  window.localStorage.removeItem("koyunchat_token");
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(init.headers);
  if (!headers.has("Content-Type") && init.body) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers
  });

  if (!response.ok) {
    let message = `Request failed with ${response.status}`;
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      // Keep the HTTP fallback message.
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}
