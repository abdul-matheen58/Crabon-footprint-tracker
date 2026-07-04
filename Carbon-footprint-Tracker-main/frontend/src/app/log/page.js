"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Sidebar from "@/components/Sidebar";
import api from "@/lib/api";
import styles from "./log.module.css";
import { useRouter } from "next/navigation";
import { toast, Toaster } from "react-hot-toast";

const categories = [
  { id: "energy", label: "Home Energy", icon: "⚡" },
  { id: "transport", label: "Transport", icon: "🚗" },
  { id: "food", label: "Diet & Food", icon: "🍔" },
  { id: "shopping", label: "Shopping", icon: "🛍️" },
  { id: "waste", label: "Waste", icon: "🗑️" },
];

export default function LogEmissionPage() {
  const router = useRouter();
  const [factors, setFactors] = useState({});
  const [form, setForm] = useState({
    category: "transport",
    sub_category: "petrol_car",
    activity_value: "",
    unit: "km",
    notes: "",
    logged_at: new Date().toISOString().split("T")[0]
  });

  const [isLoading, setIsLoading] = useState(false);

  // In a real app we'd fetch these from an endpoint or shared lib
  // For now, let's pre-define some common ones to avoid extra API hits
  const subCategories = {
    transport: [
      { id: "petrol_car", label: "Petrol Car", unit: "km" },
      { id: "electric_car", label: "Electric Car", unit: "km" },
      { id: "bus", label: "Bus", unit: "km" },
      { id: "train", label: "Train", unit: "km" },
      { id: "domestic_flight", label: "Domestic Flight", unit: "km" },
    ],
    energy: [
      { id: "electricity", label: "Electricity", unit: "kWh" },
      { id: "natural_gas", label: "Natural Gas", unit: "m³" },
    ],
    food: [
      { id: "beef", label: "Beef", unit: "kg" },
      { id: "chicken", label: "Chicken", unit: "kg" },
      { id: "vegetables", label: "Vegetables", unit: "kg" },
    ],
    shopping: [
      { id: "clothing", label: "Clothing Item", unit: "item" },
      { id: "smartphone", label: "Smartphone", unit: "unit" },
    ],
    waste: [
      { id: "landfill", label: "Landfill Waste", unit: "kg" },
      { id: "recycling", label: "Recycling", unit: "kg" },
    ]
  };

  const handleCategoryChange = (catId) => {
    const nextSub = subCategories[catId]?.[0];
    if (!nextSub) return;

    setForm((prev) => ({
      ...prev,
      category: catId,
      sub_category: nextSub.id,
      unit: nextSub.unit,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const selectedSub =
        subCategories[form.category]?.find((s) => s.id === form.sub_category) ||
        subCategories[form.category]?.[0];

      const payload = {
        ...form,
        sub_category: selectedSub?.id || form.sub_category,
        unit: selectedSub?.unit || form.unit,
        activity_value: parseFloat(form.activity_value),
      };

      await api.post("/emissions/", payload);
      toast.success("Emission logged successfully! 🌿", {
        style: { background: '#101810', color: '#E6F4EA', border: '1px solid #00C896' }
      });
      setForm((prev) => ({
        ...prev,
        activity_value: "",
        notes: "",
      }));
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to log emission.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.layout}>
      <Toaster position="top-right" />
      <Sidebar />
      <main className={styles.content}>
        <header className={styles.header}>
          <h1>Log Activity</h1>
          <p>Tell us what you did, and we'll calculate the impact.</p>
        </header>

        <div className={styles.mainGrid}>
          <div className={styles.formCard}>
            <form onSubmit={handleSubmit} className={styles.form}>
              {/* Category Selection */}
              <div className={styles.inputGroup}>
                <label>Select Category</label>
                <div className={styles.categoryGrid}>
                  {categories.map(cat => (
                    <button
                      key={cat.id}
                      type="button"
                      className={cn(styles.catBtn, form.category === cat.id && styles.activeCat)}
                      onClick={() => handleCategoryChange(cat.id)}
                    >
                      <span className={styles.catIcon}>{cat.icon}</span>
                      <span className={styles.catLabel}>{cat.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div className={styles.row}>
                <div className={styles.inputGroup}>
                  <label>Activity Type</label>
                  <select 
                    className={styles.select}
                    value={form.sub_category}
                    onChange={(e) => {
                      const sub = subCategories[form.category].find(s => s.id === e.target.value);
                      if (sub) {
                        setForm((prev) => ({
                          ...prev,
                          sub_category: e.target.value,
                          unit: sub.unit,
                        }));
                      }
                    }}
                  >
                    {subCategories[form.category].map(sub => (
                      <option key={sub.id} value={sub.id}>{sub.label}</option>
                    ))}
                  </select>
                </div>

                <div className={styles.inputGroup}>
                  <label>Amount ({form.unit})</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    className={styles.input}
                    placeholder={`e.g. 50`}
                    value={form.activity_value}
                    onChange={(e) => setForm((prev) => ({ ...prev, activity_value: e.target.value }))}
                  />
                </div>
              </div>

              <div className={styles.inputGroup}>
                <label>Date</label>
                <input
                  type="date"
                  required
                  className={styles.input}
                  value={form.logged_at}
                  onChange={(e) => setForm((prev) => ({ ...prev, logged_at: e.target.value }))}
                />
              </div>

              <div className={styles.inputGroup}>
                <label>Optional Notes</label>
                <textarea
                  className={styles.textarea}
                  placeholder="Commute to work, Grocery shopping, etc."
                  value={form.notes}
                  onChange={(e) => setForm((prev) => ({ ...prev, notes: e.target.value }))}
                />
              </div>

              <button type="submit" disabled={isLoading} className={styles.submitBtn}>
                {isLoading ? "Calculating..." : "Record Emission Log"}
              </button>
            </form>
          </div>

          <div className={styles.tipCard}>
            <div className={styles.tipHeader}>
              <span className={styles.tipIcon}>💡</span>
              <h3>Quick Tip</h3>
            </div>
            <p>
              Did you know? Switching to an electric vehicle can reduce your transport emissions by up to <b>70%</b> depending on your energy source.
            </p>
            <div className={styles.tipAction}>
              <Link href="/tips">View more tips →</Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function cn(...classes) {
  return classes.filter(Boolean).join(" ");
}
