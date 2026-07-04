"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import styles from "./login.module.css";

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      // Create x-www-form-urlencoded data for OAuth2 login
      const params = new URLSearchParams();
      params.append("username", formData.username);
      params.append("password", formData.password);

      const res = await api.post("/auth/login", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      localStorage.setItem("token", res.data.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid email or password");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <div className={styles.header}>
          <Link href="/" className={styles.logo}>🌍 CarbonTrack</Link>
          <h1>Welcome Back</h1>
          <p>Login to track your environmental impact</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          {error && <div className={styles.error}>{error}</div>}
          
          <div className={styles.group}>
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              required
              className={styles.input}
              placeholder="name@example.com"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            />
          </div>

          <div className={styles.group}>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              required
              className={styles.input}
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            />
          </div>

          <button type="submit" disabled={isLoading} className={styles.button}>
            {isLoading ? "Logging in..." : "Login to Platform"}
          </button>
        </form>

        <p className={styles.footer}>
          Don't have an account? <Link href="/register">Register now</Link>
        </p>
      </div>
    </div>
  );
}
