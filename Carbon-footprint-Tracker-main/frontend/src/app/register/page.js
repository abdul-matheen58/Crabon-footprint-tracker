"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import styles from "../login/login.module.css"; // Reuse login styles

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({ name: "", email: "", password: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      await api.post("/auth/register", {
        name: formData.name,
        email: formData.email,
        password: formData.password
      });

      // After registration, log in automatically
      const params = new URLSearchParams();
      params.append("username", formData.email);
      params.append("password", formData.password);

      const res = await api.post("/auth/login", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      localStorage.setItem("token", res.data.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <div className={styles.header}>
          <Link href="/" className={styles.logo}>🌍 CarbonTrack</Link>
          <h1>Create Account</h1>
          <p>Join the movement to a greener future</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          {error && <div className={styles.error}>{error}</div>}
          
          <div className={styles.group}>
            <label htmlFor="name">Full Name</label>
            <input
              id="name"
              type="text"
              required
              className={styles.input}
              placeholder="John Doe"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>

          <div className={styles.group}>
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              required
              className={styles.input}
              placeholder="name@example.com"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
          </div>

          <div className={styles.group}>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              required
              className={styles.input}
              placeholder="Min. 8 characters"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            />
          </div>

          <button type="submit" disabled={isLoading} className={styles.button}>
            {isLoading ? "Creating account..." : "Start Journey Now"}
          </button>
        </form>

        <p className={styles.footer}>
          Already have an account? <Link href="/login">Log in here</Link>
        </p>
      </div>
    </div>
  );
}
