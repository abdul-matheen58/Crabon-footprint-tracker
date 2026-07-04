import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Utility to merge Tailwind classes efficiently
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

/**
 * Format CO2e values with appropriate decimals
 */
export function formatCO2(val) {
  if (val >= 1000) {
    return (val / 1000).toFixed(2) + " t";
  }
  return val.toFixed(1) + " kg";
}

/**
 * Get category icon emoji
 */
export function getCategoryIcon(category) {
  const icons = {
    energy: "⚡",
    transport: "🚗",
    food: "🍔",
    shopping: "🛍️",
    waste: "🗑️",
  };
  return icons[category?.toLowerCase()] || "🌍";
}
