import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Audit COBIT 5 - SIAKAD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk Tampilan Modern
st.markdown("""
<style>
    /* Latar belakang utama */
    .stApp {
        background-color: #f4f7fb;
    }

    /* Hero Banner Header */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
        padding: 2rem 2.2rem;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.18);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.28);
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 0.7rem;
        color: #e0f2fe;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
        line-height: 1.25;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 0.96rem;
        color: #cbd5e1;
        margin: 0;
    }

    /* Kartu KPI Metrik */
    .kpi-card {
        background: #ffffff;
        padding: 1.25rem 1.35rem;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.15;
    }
    .kpi-desc {
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 0.35rem;
    }
    .border-blue { border-top: 4px solid #2563eb; }
    .border-amber { border-top: 4px solid #f59e0b; }
    .border-rose { border-top: 4px solid #e11d48; }
    .border-emerald { border-top: 4px solid #10b981; }

    /* Container Konten */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0.5rem 0 0.8rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header Utama
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">COBIT 5 PROCESS CAPABILITY ASSESSMENT</div>
    <div class="hero-title">Dashboard Audit Tata Kelola TI — SIAKAD</div>
    <p class="hero-subtitle">
        Evaluasi tingkat kapabilitas proses TI (As-Is vs To-Be), pemetaan analisis kesenjangan (Gap Analysis),
        serta penentuan prioritas rekomendasi perbaikan layanan akademik.
    </p>
</div>
""", unsafe_allow_html=True)

# Fungsi Logika COBIT 5
def tentukan_level(skor):
    level = int(np.floor(skor))
    label = {
        0: "Level 0 - Incomplete",
        1: "Level 1 - Performed",
        2: "Level 2 - Managed",
        3: "Level 3 - Established",
        4: "Level 4 - Predictable",
        5: "Level 5 - Optimizing"
    }
    return label.get(level, "Level 0 - Incomplete")

def buat_rekomendasi(gap, batas_signifikan):
    if gap <= 0:
        return "Target tercapai. Pertahankan kontrol dan lakukan evaluasi berkala."
    elif gap <= batas_signifikan:
        return "Gap minor. Perkuat standarisasi SOP dan kelengkapan dokumentasi."
    else:
        return "Gap signifikan. Prioritaskan perbaikan tata kelola dan sumber daya TI."

def muat_data_default():
    if os.path.exists("data_kuesioner_siakad_cobit5.csv"):
        return pd.read_csv("data_kuesioner_siakad_cobit5.csv")
    return pd.DataFrame({
        "Domain": ["APO", "BAI", "DSS", "DSS", "DSS"],
        "Kode Proses": ["APO12", "BAI06", "DSS01", "DSS02", "DSS05"],
        "Nama Proses": [
            "Manage Risk",
            "Manage Changes",
            "Manage Operations",
            "Manage Service Requests and Incidents",
            "Manage Security Services"
        ],
        "Fokus Audit SIAKAD": [
            "Mitigasi risiko gangguan server saat pengisian KRS serentak",
            "Pengelolaan pembaruan fitur dan perbaikan bug SIAKAD",
            "Pengawasan operasional harian jaringan dan server kampus",
            "Penanganan tiket kendala login dan input nilai oleh helpdesk",
            "Perlindungan hak akses akun dan kerahasiaan data akademik"
        ],
        "Auditor_1_Head_IT": [2.4, 2.8, 3.1, 2.6, 2.9],
        "Auditor_2_SysAdmin": [2.2, 2.6, 3.3, 2.5, 3.1],
        "Auditor_3_Developer": [2.5, 3.0, 3.0, 2.4, 2.8],
        "Auditor_4_Helpdesk": [2.1, 2.6, 3.0, 2.9, 2.8],
        "Target_To_Be": [4.0, 3.0, 4.0, 4.0, 4.0]
    })

# Sidebar Kontrol & Filter
with st.sidebar:
    st.markdown("### ⚙️ Panel Kontrol Audit")
    uploaded_file = st.file_uploader("Upload Dataset Kuesioner (CSV)", type=["csv"])

    if uploaded_file is not None:
        df_raw = pd.read_csv(uploaded_file)
        st.success("Dataset kustom berhasil dimuat.")
    else:
        df_raw = muat_data_default()
        st.info("Sumber: `data_kuesioner_siakad_cobit5.csv`")

    st.divider()
    st.markdown("### 🔍 Filter & Parameter")
    if "Domain" in df_raw.columns:
        daftar_domain = sorted(df_raw["Domain"].unique().tolist())
        pilih_domain = st.multiselect(
            "Filter Domain COBIT 5:",
            options=daftar_domain,
            default=daftar_domain
        )
    else:
        pilih_domain = []

    batas_gap = st.slider(
        "Ambang Batas Gap Signifikan:",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Proses dengan nilai Gap di atas batas ini ditandai merah sebagai prioritas utama."
    )

    st.divider()
    st.caption("Tugas 2 Audit Sistem Informasi (AUSI) • Semester Ganjil 2026")

# Filter Data Berdasarkan Domain
if "Domain" in df_raw.columns and len(pilih_domain) > 0:
    df_filtered = df_raw[df_raw["Domain"].isin(pilih_domain)].copy()
else:
    df_filtered = df_raw.copy()

if len(df_filtered) == 0:
    st.warning("Silakan pilih minimal satu Domain COBIT pada panel sebelah kiri.")
    st.stop()

# Hitung Skor Awal untuk Ringkasan & Grafik (mendukung edit interaktif di Tab 3)
if "edited_data" not in st.session_state or st.session_state.get("last_domains") != pilih_domain or uploaded_file is not None:
    st.session_state["edited_data"] = df_filtered.copy()
    st.session_state["last_domains"] = pilih_domain

df_aktif = st.session_state["edited_data"].copy()
kolom_auditor = [col for col in df_aktif.columns if col.startswith("Auditor_")]

if len(kolom_auditor) == 0:
    st.error("Dataset harus memiliki minimal satu kolom dengan awalan 'Auditor_'.")
    st.stop()

df_aktif["Skor_As_Is"] = df_aktif[kolom_auditor].mean(axis=1).round(2)
df_aktif["Capability_Level"] = df_aktif["Skor_As_Is"].apply(tentukan_level)
df_aktif["Gap"] = (df_aktif["Target_To_Be"] - df_aktif["Skor_As_Is"]).round(2)
df_aktif["Rekomendasi"] = df_aktif["Gap"].apply(lambda g: buat_rekomendasi(g, batas_gap))

df_hasil = df_aktif.sort_values(by="Gap", ascending=False).reset_index(drop=True)
df_hasil.insert(0, "Prioritas", df_hasil.index + 1)

# Kartu KPI Ringkasan Eksekutif
avg_asis = df_aktif["Skor_As_Is"].mean()
avg_tobe = df_aktif["Target_To_Be"].mean()
avg_gap = df_aktif["Gap"].mean()
top_proc = df_hasil.iloc[0]["Kode Proses"]
top_gap = df_hasil.iloc[0]["Gap"]
jml_signifikan = int((df_aktif["Gap"] > batas_gap).sum())

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card border-blue">
        <div class="kpi-label">Rata-Rata Skor As-Is</div>
        <div class="kpi-value">{avg_asis:.2f} <span style="font-size:1rem;color:#64748b;">/ 5.00</span></div>
        <div class="kpi-desc">Kondisi kapabilitas aktual saat ini</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card border-amber">
        <div class="kpi-label">Rata-Rata Target To-Be</div>
        <div class="kpi-value">{avg_tobe:.2f} <span style="font-size:1rem;color:#64748b;">/ 5.00</span></div>
        <div class="kpi-desc">Standar target tata kelola kampus</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card border-rose">
        <div class="kpi-label">Rata-Rata Nilai Gap</div>
        <div class="kpi-value">{avg_gap:.2f}</div>
        <div class="kpi-desc">{jml_signifikan} dari {len(df_aktif)} proses berstatus Gap signifikan</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card border-emerald">
        <div class="kpi-label">Prioritas Utama Perbaikan</div>
        <div class="kpi-value">{top_proc}</div>
        <div class="kpi-desc">Gap tertinggi sebesar {top_gap:.2f} poin</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Navigasi Tab Interaktif
tab1, tab2, tab3 = st.tabs([
    "📊 Visualisasi & Analisis Grafik",
    "📋 Peringkat Prioritas & Rekomendasi",
    "✏️ Input & Simulasi Skor Kuesioner"
])

# TAB 1: Visualisasi Grafik Modern
with tab1:
    col_g1, col_g2 = st.columns([1.35, 1])

    with col_g1:
        st.markdown('<div class="section-header">Perbandingan Capability Level (As-Is vs To-Be)</div>', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(8, 4.6))
        fig1.patch.set_facecolor("#ffffff")
        ax1.set_facecolor("#f8fafc")

        x = np.arange(len(df_aktif["Kode Proses"]))
        width = 0.36
        bar1 = ax1.bar(x - width / 2, df_aktif["Skor_As_Is"], width, label="As-Is (Saat Ini)", color="#2563eb", edgecolor="none", zorder=3)
        bar2 = ax1.bar(x + width / 2, df_aktif["Target_To_Be"], width, label="To-Be (Target)", color="#f59e0b", edgecolor="none", zorder=3)

        ax1.set_ylabel("Skor Capability Level (0 - 5)", fontsize=10, color="#334155", fontweight="bold")
        ax1.set_xticks(x)
        ax1.set_xticklabels(df_aktif["Kode Proses"], fontsize=10, fontweight="bold", color="#1e293b")
        ax1.set_ylim(0, 5.4)
        ax1.grid(axis="y", linestyle="--", alpha=0.6, color="#cbd5e1", zorder=0)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_color("#cbd5e1")
        ax1.spines["bottom"].set_color("#cbd5e1")
        ax1.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", loc="upper right")

        ax1.bar_label(bar1, padding=4, fontsize=9, fontweight="bold", color="#1e3a8a")
        ax1.bar_label(bar2, padding=4, fontsize=9, fontweight="bold", color="#b45309")

        plt.tight_layout()
        st.pyplot(fig1)

    with col_g2:
        st.markdown('<div class="section-header">Peringkat Nilai Gap per Proses TI</div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(6.5, 4.6))
        fig2.patch.set_facecolor("#ffffff")
        ax2.set_facecolor("#f8fafc")

        df_urut = df_aktif.sort_values(by="Gap", ascending=True)
        warna_gap = ["#e11d48" if g > batas_gap else "#0ea5e9" for g in df_urut["Gap"]]
        bars_gap = ax2.barh(df_urut["Kode Proses"], df_urut["Gap"], color=warna_gap, height=0.55, zorder=3)

        ax2.axvline(batas_gap, color="#64748b", linestyle=":", linewidth=1.5, zorder=4, label=f"Batas Signifikan ({batas_gap:.1f})")
        ax2.set_xlabel("Selisih Gap (To-Be - As-Is)", fontsize=10, color="#334155", fontweight="bold")
        ax2.set_xlim(0, max(2.3, df_urut["Gap"].max() + 0.45))
        ax2.tick_params(axis="y", labelsize=10)
        ax2.grid(axis="x", linestyle="--", alpha=0.6, color="#cbd5e1", zorder=0)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["left"].set_color("#cbd5e1")
        ax2.spines["bottom"].set_color("#cbd5e1")
        ax2.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", loc="lower right")
        ax2.bar_label(bars_gap, padding=5, fontsize=9.5, fontweight="bold", color="#1e293b")

        plt.tight_layout()
        st.pyplot(fig2)

    # Grafik Radar (Spider Chart) jika proses >= 3
    if len(df_aktif) >= 3:
        st.markdown('<div class="section-header">Peta Radar Kematangan Tata Kelola SIAKAD (COBIT 5)</div>', unsafe_allow_html=True)
        col_r1, col_r2 = st.columns([1.1, 1])
        with col_r1:
            labels = df_aktif["Kode Proses"].tolist()
            stats_asis = df_aktif["Skor_As_Is"].tolist()
            stats_tobe = df_aktif["Target_To_Be"].tolist()

            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            stats_asis += stats_asis[:1]
            stats_tobe += stats_tobe[:1]
            angles += angles[:1]

            fig_radar, ax_radar = plt.subplots(figsize=(6, 4.5), subplot_kw=dict(polar=True))
            fig_radar.patch.set_facecolor("#ffffff")
            ax_radar.plot(angles, stats_tobe, color="#f59e0b", linewidth=2, linestyle="--", label="Target To-Be")
            ax_radar.fill(angles, stats_tobe, color="#f59e0b", alpha=0.12)

            ax_radar.plot(angles, stats_asis, color="#2563eb", linewidth=2.5, label="Skor As-Is")
            ax_radar.fill(angles, stats_asis, color="#2563eb", alpha=0.25)

            ax_radar.set_xticks(angles[:-1])
            ax_radar.set_xticklabels(labels, fontsize=10, fontweight="bold", color="#1e293b")
            ax_radar.set_ylim(0, 5)
            ax_radar.set_yticks([1, 2, 3, 4, 5])
            ax_radar.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8, color="#64748b")
            ax_radar.grid(color="#cbd5e1", linestyle="--", alpha=0.7)
            ax_radar.legend(loc="upper right", bbox_to_anchor=(1.28, 1.12), frameon=True)

            plt.tight_layout()
            st.pyplot(fig_radar)

        with col_r2:
            st.info(
                "**Cara Membaca Grafik Radar:**\n\n"
                "- **Area Biru (As-Is):** Menunjukkan cakupan kapabilitas aktual tata kelola SIAKAD saat ini.\n"
                "- **Garis Oranye Putus-Putus (To-Be):** Menunjukkan target kapabilitas yang diharapkan manajemen kampus.\n"
                "- Semakin lebar jarak antara garis biru dan oranye pada suatu proses (seperti **APO12**), semakin mendesak kebutuhan perbaikan pada proses tersebut."
            )

# TAB 2: Tabel Peringkat Berwarna & Download
with tab2:
    st.markdown('<div class="section-header">Tabel Peringkat Prioritas dan Rekomendasi Audit</div>', unsafe_allow_html=True)

    kolom_tampil = [
        "Prioritas", "Domain", "Kode Proses", "Nama Proses",
        "Skor_As_Is", "Target_To_Be", "Gap", "Capability_Level", "Rekomendasi"
    ]
    kolom_tersedia = [k for k in kolom_tampil if k in df_hasil.columns]
    df_tampil = df_hasil[kolom_tersedia].copy()

    def highlight_gap(s):
        styles = []
        for val in s:
            if val > batas_gap:
                styles.append("background-color: #ffe4e6; color: #be123c; font-weight: bold;")
            elif val > 0:
                styles.append("background-color: #e0f2fe; color: #0369a1; font-weight: bold;")
            else:
                styles.append("background-color: #dcfce7; color: #15803d; font-weight: bold;")
        return styles

    styled_df = df_tampil.style.apply(highlight_gap, subset=["Gap"]).format({
        "Skor_As_Is": "{:.2f}",
        "Target_To_Be": "{:.2f}",
        "Gap": "{:.2f}"
    })

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    csv_output = df_hasil.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Laporan Hasil Audit (CSV)",
        data=csv_output,
        file_name="hasil_audit_siakad_cobit5.csv",
        mime="text/csv"
    )

# TAB 3: Editor Interaktif
with tab3:
    st.markdown('<div class="section-header">Editor Penilaian Kuesioner Responden SIAKAD</div>', unsafe_allow_html=True)
    st.caption("Ubah angka penilaian pada kolom Auditor atau Target_To_Be di bawah ini. Seluruh kartu ringkasan, grafik, dan peringkat akan otomatis diperbarui.")

    edited_result = st.data_editor(
        st.session_state["edited_data"],
        num_rows="dynamic",
        use_container_width=True,
        key="editor_kuesioner"
    )

    if not edited_result.equals(st.session_state["edited_data"]):
        st.session_state["edited_data"] = edited_result.copy()
        st.rerun()
