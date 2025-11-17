// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function apiFetch(url: string, options: any = {}) {
  const token = localStorage.getItem("token");

  const authHeaders = token
    ? { Authorization: `Bearer ${token}` }
    : {};

  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders,
      ...(options.headers || {}),
    },
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }

  return res;
}