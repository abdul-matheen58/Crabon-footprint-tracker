"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { 
  LayoutDashboard, 
  PlusCircle, 
  BarChart3, 
  Target, 
  Lightbulb, 
  Bot, 
  Settings, 
  LogOut 
} from "lucide-react";
import { cn } from "@/lib/utils";
import styles from "./sidebar.module.css";

const menuItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard" },
  { icon: PlusCircle, label: "Log Emission", href: "/log" },
  { icon: BarChart3, label: "Analytics", href: "/analytics" },
  { icon: Target, label: "Goals", href: "/goals" },
  { icon: Lightbulb, label: "Tips & Offsets", href: "/tips" },
  { icon: Bot, label: "AI Assistant", href: "/assistant" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <aside className={styles.sidebar}>
      <div className={styles.top}>
        <Link href="/" className={styles.logo}>
          <span className={styles.logoIcon}>🌍</span>
          <span className="mono">CarbonTrack</span>
        </Link>

        <nav className={styles.nav}>
          {menuItems.map((item) => (
            <Link 
              key={item.href} 
              href={item.href}
              className={cn(styles.item, pathname === item.href && styles.active)}
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>
      </div>

      <div className={styles.bottom}>
        <Link 
          href="/settings" 
          className={cn(styles.item, pathname === "/settings" && styles.active)}
        >
          <Settings size={20} />
          <span>Settings</span>
        </Link>
        <button className={styles.logout} onClick={handleLogout}>
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}
