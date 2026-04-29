import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1565C0, #1976D2);
        padding: 1rem 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .metric-value { font-size: 1.8rem; font-weight: 700; margin: 0; }
    .metric-label { font-size: 0.85rem; opacity: 0.9; margin: 0; }
    h1 { color: #1565C0; }
    h2 { color: #1976D2; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    main = pd.read_csv(os.path.join(base, "main_data.csv"),
                       parse_dates=["order_purchase_timestamp"])
    rfm  = pd.read_csv(os.path.join(base, "rfm_data.csv"))
    return main, rfm

main_data, rfm_data = load_data()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shopping-cart.png", width=80)
    st.title("🛒 E-Commerce Analytics")
    st.markdown("---")

    years = sorted(main_data["order_purchase_timestamp"].dt.year.dropna().unique())
    selected_years = st.multiselect("📅 Pilih Tahun", years, default=years)

    all_cats = sorted(main_data["product_category_name_english"].dropna().unique())
    top10_default = (
        main_data.groupby("product_category_name_english")["total_payment"]
        .sum().sort_values(ascending=False).head(10).index.tolist()
    )
    selected_cats = st.multiselect(
        "📦 Filter Kategori (Opsional)",
        all_cats,
        default=[],
        placeholder="Semua kategori"
    )

    states = sorted(main_data["customer_state"].dropna().unique())
    selected_states = st.multiselect(
        "📍 Filter State (Opsional)",
        states,
        default=[],
        placeholder="Semua state"
    )

    st.markdown("---")
    st.caption("📊 Data: E-Commerce Public Dataset\n\n"
               "👤 Muhammad Alif Anshar\n\nalif040105@gmail.com")

# ─── Filter Data ──────────────────────────────────────────────────────────────
df = main_data[main_data["order_purchase_timestamp"].dt.year.isin(selected_years)].copy()
if selected_cats:
    df = df[df["product_category_name_english"].isin(selected_cats)]
if selected_states:
    df = df[df["customer_state"].isin(selected_states)]

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("🛒 E-Commerce Public Dataset — Analytics Dashboard")
st.markdown("Dashboard interaktif untuk menganalisis pola penjualan, pengiriman, dan segmentasi pelanggan.")
st.markdown("---")

# ─── KPI Cards ────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
total_rev   = df["total_payment"].sum()
total_orders = df["order_id"].nunique()
avg_order   = df["total_payment"].mean()
n_categories = df["product_category_name_english"].nunique()

for col, val, label, icon in [
    (col1, f"BRL {total_rev/1e6:.2f}M", "Total Revenue", "💰"),
    (col2, f"{total_orders:,}", "Total Pesanan", "🛍️"),
    (col3, f"BRL {avg_order:.2f}", "Rata-rata Nilai Pesanan", "📊"),
    (col4, str(n_categories), "Jumlah Kategori", "📦"),
]:
    col.markdown(f"""
    <div class="metric-card">
        <p class="metric-label">{icon} {label}</p>
        <p class="metric-value">{val}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tab Layout ───────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📦 Revenue & Kategori", "🚚 Pengiriman & Review", "👥 RFM Segmentasi"])

# ════════════════════════════════════════════════════
# TAB 1: Revenue & Kategori
# ════════════════════════════════════════════════════
with tab1:
    st.subheader("Kategori Produk dengan Revenue Tertinggi & Tren Bulanan")

    cat_rev = (
        df.groupby("product_category_name_english")["total_payment"]
        .sum().sort_values(ascending=False).head(10).reset_index()
    )
    cat_rev.columns = ["Kategori", "Revenue"]

    col_a, col_b = st.columns([1, 1.5])

    with col_a:
        st.markdown("**Top 10 Kategori berdasarkan Revenue**")
        # PERBAIKAN 1: Cek apakah data kosong agar terhindar dari ValueError NaN
        if cat_rev.empty:
            st.info("Tidak ada data kategori untuk filter yang dipilih.")
        else:
            fig, ax = plt.subplots(figsize=(6, 5))
            colors = ["#1565C0" if i == 0 else "#90CAF9" for i in range(len(cat_rev))]
            ax.barh(cat_rev["Kategori"][::-1], cat_rev["Revenue"][::-1]/1e6,
                    color=colors[::-1], edgecolor="white")
            for i, v in enumerate(cat_rev["Revenue"][::-1]/1e6):
                ax.text(v + 0.01, i, f"{v:.1f}M", va="center", fontsize=8)
            ax.set_xlabel("Total Revenue (Juta BRL)", fontsize=10)
            
            # Set X-limit dengan aman
            max_rev = cat_rev["Revenue"].max() / 1e6
            ax.set_xlim(0, max_rev * 1.22)
            
            ax.grid(axis="x", alpha=0.4)
            sns.despine(left=True, bottom=True)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    with col_b:
        st.markdown("**Tren Revenue Bulanan — Top Kategori**")
        
        top_cats = cat_rev["Kategori"].head(3).tolist()
        
        # PERBAIKAN 2: Cek apakah top_cats ada isinya agar terhindar dari IndexError
        if not top_cats:
            st.info("Tidak ada data tren bulanan untuk filter yang dipilih.")
        else:
            df["year_month_dt"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
            monthly = (
                df[df["product_category_name_english"].isin(top_cats)]
                .groupby(["year_month_dt", "product_category_name_english"])["total_payment"]
                .sum().reset_index()
            )
            
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Membuat palette warna secara otomatis sesuai jumlah kategori yang tersisa
            default_colors = ["#1565C0", "#FF7043", "#43A047"]
            palette = {cat: default_colors[i] for i, cat in enumerate(top_cats)}
            
            for cat in top_cats:
                sub = monthly[monthly["product_category_name_english"] == cat]
                if not sub.empty:
                    ax.plot(sub["year_month_dt"], sub["total_payment"]/1e3,
                            marker="o", markersize=4, linewidth=2, label=cat,
                            color=palette.get(cat, "#888"))
            
            ax.set_xlabel("Bulan", fontsize=10)
            ax.set_ylabel("Revenue (Ribu BRL)", fontsize=10)
            ax.legend(fontsize=8)
            ax.tick_params(axis="x", rotation=45)
            ax.grid(axis="y", alpha=0.4)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    # Tabel detail
    with st.expander("📋 Lihat Data Lengkap Top Kategori"):
        if cat_rev.empty:
            st.write("Data kosong.")
        else:
            cat_rev_display = cat_rev.copy()
            cat_rev_display["Revenue (BRL)"] = cat_rev_display["Revenue"].map("BRL {:,.2f}".format)
            st.dataframe(cat_rev_display[["Kategori", "Revenue (BRL)"]], use_container_width=True)

# ════════════════════════════════════════════════════
# TAB 2: Pengiriman & Review
# ════════════════════════════════════════════════════
with tab2:
    st.subheader("Pertanyaan 2: Keterlambatan Pengiriman & Dampak pada Review Score")

    delay_df = df.dropna(subset=["delay_days", "review_score"]).copy()
    delay_df["delay_category"] = pd.cut(
        delay_df["delay_days"],
        bins=[-np.inf, -14, -7, 0, 7, np.inf],
        labels=["Sangat Cepat\n(>14h)", "Cepat\n(7-14h)",
                "Tepat Waktu\n(0-7h)", "Terlambat\n(1-7h)", "Sangat Terlambat\n(>7h)"]
    )
    delay_avg = delay_df.groupby("delay_category")["review_score"].mean().reset_index()

    state_delay = (
        delay_df.groupby("customer_state")
        .agg(avg_delay=("delay_days","mean"), avg_review=("review_score","mean"), count=("order_id","count"))
        .reset_index().sort_values("avg_delay", ascending=False)
    )

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("**Rata-rata Review Score per Kategori Keterlambatan**")
        fig, ax = plt.subplots(figsize=(6, 5))
        delay_colors = ["#1565C0", "#42A5F5", "#A5D6A7", "#FFCC80", "#EF5350"]
        bars = ax.bar(delay_avg["delay_category"].astype(str),
                      delay_avg["review_score"],
                      color=delay_colors, edgecolor="white", width=0.6)
        ax.set_ylim(0, 5.5)
        ax.set_ylabel("Rata-rata Review Score", fontsize=10)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.05,
                    f"{h:.2f}", ha="center", fontsize=9)
        ax.tick_params(axis="x", labelsize=8, rotation=10)
        ax.grid(axis="y", alpha=0.4)
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_d:
        st.markdown("**Top 10 State: Rata-rata Delay Pengiriman**")
        top10 = state_delay.head(10)
        fig, ax = plt.subplots(figsize=(6, 5))
        bar_c = ["#EF5350" if v > 0 else "#42A5F5" for v in top10["avg_delay"]]
        ax.barh(top10["customer_state"][::-1], top10["avg_delay"][::-1],
                color=bar_c[::-1], edgecolor="white")
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_xlabel("Rata-rata Delay (hari)", fontsize=10)
        ax.grid(axis="x", alpha=0.4)
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    col_e, col_f = st.columns(2)
    late_pct = (delay_df["delay_days"] > 0).mean() * 100
    avg_delay_val = delay_df["delay_days"].mean()
    avg_review_val = delay_df["review_score"].mean()
    corr_val = delay_df[["delay_days","review_score"]].corr().iloc[0,1]

    col_e.metric("Persentase Pesanan Terlambat", f"{late_pct:.1f}%")
    col_f.metric("Rata-rata Delay (hari)", f"{avg_delay_val:.1f}")
    col_e.metric("Rata-rata Review Score", f"{avg_review_val:.2f} / 5")
    col_f.metric("Korelasi Delay-Review", f"{corr_val:.3f}")

# ════════════════════════════════════════════════════
# TAB 3: RFM Segmentasi
# ════════════════════════════════════════════════════
with tab3:
    st.subheader("Analisis Lanjutan: RFM Segmentasi Pelanggan")
    st.markdown(
        "RFM Analysis mengelompokkan pelanggan berdasarkan **Recency** (kapan terakhir beli), "
        "**Frequency** (seberapa sering beli), dan **Monetary** (berapa banyak uang dikeluarkan)."
    )

    seg_counts = rfm_data["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]

    rfm_seg = rfm_data.groupby("Segment")[["Recency","Frequency","Monetary"]].mean().reset_index()

    col_g, col_h = st.columns(2)

    with col_g:
        st.markdown("**Distribusi Segmen Pelanggan**")
        fig, ax = plt.subplots(figsize=(6, 5))
        seg_colors = ["#1565C0","#42A5F5","#A5D6A7","#FFCC80","#EF9A9A","#B0BEC5","#CE93D8"]
        ax.pie(seg_counts["Count"], labels=seg_counts["Segment"],
               autopct="%1.1f%%", colors=seg_colors[:len(seg_counts)],
               startangle=140, pctdistance=0.82)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_h:
        st.markdown("**Rata-rata RFM per Segmen (Ternormalisasi)**")
        fig, ax = plt.subplots(figsize=(7, 5))
        x = np.arange(len(rfm_seg))
        w = 0.25
        r_n = rfm_seg["Recency"] / rfm_seg["Recency"].max()
        f_n = rfm_seg["Frequency"] / rfm_seg["Frequency"].max()
        m_n = rfm_seg["Monetary"] / rfm_seg["Monetary"].max()
        ax.bar(x - w, r_n, w, label="Recency", color="#EF5350", alpha=0.85)
        ax.bar(x, f_n, w, label="Frequency", color="#42A5F5", alpha=0.85)
        ax.bar(x + w, m_n, w, label="Monetary", color="#66BB6A", alpha=0.85)
        ax.set_xticks(x)
        ax.set_xticklabels(rfm_seg["Segment"], rotation=30, ha="right", fontsize=8)
        ax.set_ylabel("Nilai Ternormalisasi", fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.4)
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.markdown("**Statistik Lengkap RFM per Segmen**")
    rfm_detail = rfm_data.groupby("Segment").agg(
        Jumlah_Pelanggan=("customer_unique_id","count"),
        Avg_Recency=("Recency","mean"),
        Avg_Frequency=("Frequency","mean"),
        Avg_Monetary=("Monetary","mean"),
        Total_Revenue=("Monetary","sum")
    ).reset_index().sort_values("Jumlah_Pelanggan", ascending=False)

    rfm_detail["Avg_Recency"] = rfm_detail["Avg_Recency"].round(0).astype(int)
    rfm_detail["Avg_Frequency"] = rfm_detail["Avg_Frequency"].round(2)
    rfm_detail["Avg_Monetary"] = rfm_detail["Avg_Monetary"].map("BRL {:.2f}".format)
    rfm_detail["Total_Revenue"] = rfm_detail["Total_Revenue"].map("BRL {:,.0f}".format)
    st.dataframe(rfm_detail, use_container_width=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("📊 E-Commerce Public Dataset Analysis | Muhammad Alif Anshar | Dicoding Data Analysis Project")
