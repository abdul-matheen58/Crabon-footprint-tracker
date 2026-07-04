"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import api from "@/lib/api";
import { useAuth } from "@/lib/useAuth";
import styles from "./dashboard.module.css";

import { formatCO2, getCategoryIcon } from "@/lib/utils";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from "recharts";

export default function DashboardPage() {
  const { loading: authLoading } = useAuth();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const res = await api.get("/analytics/summary");
        setSummary(res.data);
      } catch (err) {
        console.error("Failed to fetch dashboard summary", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, [authLoading]);

  if (authLoading || loading) return <div className={styles.loader}>Analyzing your footprint...</div>;


  const COLORS = ['#00C896', '#4FC3F7', '#FFB347', '#FF6B6B', '#90A090'];

  return (
    <div className={styles.layout}>
      <Sidebar />
      <main className={styles.content}>
        <header className={styles.header}>
          <h1>Dashboard Overview</h1>
          <p>Welcome back! Here's your environmental impact summary.</p>
        </header>

        {/* Top Stats */}
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <span className={styles.statLabel}>This Month</span>
            <div className={styles.statMain}>
              <span className={styles.statValue}>{summary?.total_co2e_this_month || 0}</span>
              <span className={styles.unit}>kg CO₂e</span>
            </div>
            {summary?.month_over_month_change_pct !== 0 && (
              <span className={summary?.month_over_month_change_pct < 0 ? styles.trendDown : styles.trendUp}>
                {summary?.month_over_month_change_pct < 0 ? '↓' : '↑'} {Math.abs(summary?.month_over_month_change_pct)}% vs last month
              </span>
            )}
          </div>

          <div className={styles.statCard}>
            <span className={styles.statLabel}>All Time Footprint</span>
            <div className={styles.statMain}>
              <span className={styles.statValue}>{formatCO2(summary?.total_co2e_all_time || 0).split(' ')[0]}</span>
              <span className={styles.unit}>{formatCO2(summary?.total_co2e_all_time || 0).split(' ')[1]}</span>
            </div>
            <span className={styles.statSub}>Since you joined</span>
          </div>

          <div className={styles.statCard}>
            <span className={styles.statLabel}>Top Category</span>
            <div className={styles.statMain}>
              <span className={styles.categoryIcon}>
                {getCategoryIcon(summary?.top_category)}
              </span>
              <span className={styles.statValueText}>{summary?.top_category || "N/A"}</span>
            </div>
            <span className={styles.statSub}>Biggest source of CO₂</span>
          </div>
        </div>

        {/* Charts Section */}
        <div className={styles.chartsGrid}>
          {/* Main Trend Line */}
          <div className={styles.chartCard}>
            <h3>30-Day Emission Trend</h3>
            <div className={styles.chartContainer}>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={summary?.daily_trends_30_days}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#222" vertical={false} />
                  <XAxis 
                    dataKey="date" 
                    stroke="#8AAE90" 
                    fontSize={12} 
                    tickFormatter={(val) => new Date(val).toLocaleDateString(undefined, { day: 'numeric', month: 'short' })}
                  />
                  <YAxis stroke="#8AAE90" fontSize={12} />
                  <Tooltip 
                    contentStyle={{ background: '#101810', border: '1px solid rgba(138,174,144,0.2)', borderRadius: '8px' }}
                    itemStyle={{ color: '#00C896' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="co2e_kg" 
                    stroke="#00C896" 
                    strokeWidth={3} 
                    dot={{ r: 4, fill: '#00C896' }} 
                    activeDot={{ r: 6 }} 
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Category Pie */}
          <div className={styles.chartCard}>
            <h3>Category Breakdown</h3>
            <div className={styles.chartContainer}>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={summary?.category_breakdown}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="co2e_kg"
                    nameKey="category"
                  >
                    {summary?.category_breakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ background: '#101810', border: '1px solid rgba(138,174,144,0.2)', borderRadius: '8px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className={styles.legend}>
                  {summary?.category_breakdown.map((entry, index) => (
                    <div key={entry.category} className={styles.legendItem}>
                      <span className={styles.dot} style={{ background: COLORS[index % COLORS.length] }}></span>
                      <span className={styles.label}>{entry.category} ({entry.percentage}%)</span>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
