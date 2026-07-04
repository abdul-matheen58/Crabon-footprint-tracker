import styles from "./landing.module.css";

export default function LandingPage() {
  return (
    <div className={styles.container}>
      {/* Navigation */}
      <nav className={styles.nav}>
        <div className={styles.logo}>
          <span className={styles.icon}>🌍</span>
          <span className="mono">CarbonTrack</span>
        </div>
        <div className={styles.navLinks}>
          <a href="/login" className={styles.link}>Login</a>
          <a href="/register" className={styles.btnPrimary}>Get Started</a>
        </div>
      </nav>

      {/* Hero Section */}
      <header className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.title}>
            Master Your Impact on <span className="text-gradient">the Planet</span>
          </h1>
          <p className={styles.subtitle}>
            A smart, context-aware platform to track emissions, set goals, 
            and get actionable AI-driven advice to reduce your footprint.
          </p>
          <div className={styles.heroBtns}>
            <a href="/register" className={styles.btnLarge}>Start Tracking Free</a>
            <a href="#features" className={styles.btnSecondary}>See How It Works</a>
          </div>
        </div>

        {/* Stats Grid */}
        <div className={styles.heroStats}>
          <div className={styles.statCard}>
            <span className={styles.statVal}>4.7t</span>
            <span className={styles.statLabel}>Avg World Footprint</span>
          </div>
          <div className={styles.statCard}>
            <span className={styles.statVal}>-15%</span>
            <span className={styles.statLabel}>Avg User Reduction</span>
          </div>
          <div className={styles.statCard}>
            <span className={styles.statVal}>24/7</span>
            <span className={styles.statLabel}>Smart Assitant</span>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section id="features" className={styles.features}>
        <h2 className={styles.sectionTitle}>Smarter Emissions Tracking</h2>
        <div className={styles.featureGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🚗</div>
            <h3>Intelligent Logging</h3>
            <p>Log transport, energy, food, and waste in seconds with our smart parsing engine.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🤖</div>
            <h3>Contextual Assistant</h3>
            <p>No generic tips. Get advice based on your actual data and top emission categories.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📈</div>
            <h3>Live Analytics</h3>
            <p>Visualize your progress with beautiful heatmaps and monthly performance trends.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
