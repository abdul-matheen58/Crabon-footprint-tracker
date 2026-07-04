"use client";

import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import api from "@/lib/api";
import styles from "./tips.module.css";
import { Lightbulb, Star, CheckCircle2, ChevronRight, Leaf, Zap, Car, ShoppingBag, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { toast, Toaster } from "react-hot-toast";

const categoryIcons = {
  energy: <Zap size={20} />,
  transport: <Car size={20} />,
  food: <Leaf size={20} />,
  shopping: <ShoppingBag size={20} />,
  waste: <Trash2 size={20} />,
};

export default function TipsPage() {
  const [tips, setTips] = useState([]);
  const [myTips, setMyTips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [tipsRes, myTipsRes] = await Promise.all([
        api.get("/tips/"),
        api.get("/tips/my-tips")
      ]);
      setTips(tipsRes.data);
      setMyTips(myTipsRes.data);
    } catch (err) {
      console.error("Failed to fetch tips", err);
    } finally {
      setLoading(false);
    }
  };

  const handleBookmark = async (tipId) => {
    try {
      await api.post(`/tips/${tipId}/bookmark`);
      toast.success("Tip bookmarked! ⭐");
      fetchData();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Action failed");
    }
  };

  const filteredTips = filter === "all" ? tips : tips.filter(t => t.category === filter);
  const bookmarkedIds = new Set(myTips.map(mt => mt.tip_id));

  return (
    <div className={styles.layout}>
      <Toaster position="top-right" />
      <Sidebar />
      <main className={styles.content}>
        <header className={styles.header}>
          <h1>Tips & Carbon Offsets</h1>
          <p>Personalized recommendations to lower your footprint.</p>
        </header>

        <div className={styles.filterBar}>
          {["all", "energy", "transport", "food", "shopping", "waste"].map(f => (
            <button 
              key={f} 
              className={cn(styles.filterBtn, filter === f && styles.activeFilter)}
              onClick={() => setFilter(f)}
            >
              {f}
            </button>
          ))}
        </div>

        <div className={styles.grid}>
          {filteredTips.map((tip) => (
            <div key={tip.id} className={styles.tipCard}>
              <div className={styles.tipTop}>
                <div className={styles.iconBox} data-category={tip.category}>
                  {categoryIcons[tip.category] || <Lightbulb size={20} />}
                </div>
                <div className={styles.impact}>
                  <div className={styles.impactVal}>-{tip.impact_kg_month}kg</div>
                  <div className={styles.impactLabel}>CO₂e / mo</div>
                </div>
              </div>
              
              <h3 className={styles.tipTitle}>{tip.title}</h3>
              <p className={styles.tipDesc}>{tip.description}</p>
              
              <div className={styles.tipMeta}>
                <span className={cn(styles.difficulty, styles[tip.difficulty.toLowerCase()])}>
                  {tip.difficulty}
                </span>
                <button 
                  className={cn(styles.bookmarkBtn, bookmarkedIds.has(tip.id) && styles.isBookmarked)}
                  onClick={() => !bookmarkedIds.has(tip.id) && handleBookmark(tip.id)}
                  disabled={bookmarkedIds.has(tip.id)}
                >
                  {bookmarkedIds.has(tip.id) ? (
                    <><CheckCircle2 size={16} /> Bookmarked</>
                  ) : (
                    <><Star size={16} /> Bookmark</>
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
