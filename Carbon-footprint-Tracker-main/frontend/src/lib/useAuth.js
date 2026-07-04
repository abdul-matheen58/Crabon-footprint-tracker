import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

/**
 * Hook to protect routes that require authentication
 */
export function useAuth() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.replace("/login");
    } else {
      setLoading(false);
    }
  }, [router]);

  return { loading };
}
