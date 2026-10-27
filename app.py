import io
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==============================================================================
st.set_page_config(
    page_title="TalentSet • Sistem Klasifikasi Himpunan",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. INJEKSI CUSTOM CSS (Modern Slate Dark Dashboard)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Padding layout rapi */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1250px;
    }

    /* Header Banner Gelap Mewah */
    .header-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .header-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #f8fafc !important;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .header-sub {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 4px;
    }
    .header-badge {
        background: #0f172a;
        color: #38bdf8;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #0284c7;
        letter-spacing: 0.03em;
    }

    /* Kartu Metrik Dark Slate */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .metric-card:hover {
        border-color: #64748b;
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }
    .metric-number {
        font-size: 1.85rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .metric-desc {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 6px;
    }

    /* Kotak Info Operasi Aktif */
    .op-banner {
        background: #1e293b;
        border: 1px solid #334155;
        border-left: 4px solid #818cf8;
        border-radius: 12px;
        padding: 14px 20px;
        margin: 1.2rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    .op-title {
        font-size: 1rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .op-formula {
        font-family: monospace;
        font-size: 0.88rem;
        color: #818cf8;
        font-weight: 700;
        margin-top: 2px;
    }
    .op-desc {
        font-size: 0.84rem;
        color: #cbd5e1;
        margin-top: 4px;
        line-height: 1.45;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. DATASET DEFAULT (15 DATA SESUAI MILESTONE PJBL-2)
# ==============================================================================
DEFAULT_DATA = [
    {"id_pendaftar": "P01", "nama": "Aditia Nugraha", "ipk": 3.82, "nilai_alpro": 88, "pengalaman_organisasi": 3},
    {"id_pendaftar": "P02", "nama": "Bella Safitri", "ipk": 3.65, "nilai_alpro": 84, "pengalaman_organisasi": 1},
    {"id_pendaftar": "P03", "nama": "Candra Pratama", "ipk": 3.30, "nilai_alpro": 92, "pengalaman_organisasi": 0},
    {"id_pendaftar": "P04", "nama": "Dian Kusuma", "ipk": 3.55, "nilai_alpro": 74, "pengalaman_organisasi": 2},
    {"id_pendaftar": "P05", "nama": "Eko Santoso", "ipk": 3.10, "nilai_alpro": 68, "pengalaman_organisasi": 3},
    {"id_pendaftar": "P06", "nama": "Farhan Ramadhan", "ipk": 3.78, "nilai_alpro": 70, "pengalaman_organisasi": 0},
    {"id_pendaftar": "P07", "nama": "Gita Ayu", "ipk": 3.88, "nilai_alpro": 85, "pengalaman_organisasi": 2},
    {"id_pendaftar": "P08", "nama": "Hendra Wijaya", "ipk": 3.40, "nilai_alpro": 81, "pengalaman_organisasi": 2},
    {"id_pendaftar": "P09", "nama": "Indah Permata", "ipk": 3.60, "nilai_alpro": 90, "pengalaman_organisasi": 1},
    {"id_pendaftar": "P10", "nama": "Joko Susilo", "ipk": 3.25, "nilai_alpro": 65, "pengalaman_organisasi": 1},
    {"id_pendaftar": "P11", "nama": "Kartika Sari", "ipk": 3.52, "nilai_alpro": 82, "pengalaman_organisasi": 2},
    {"id_pendaftar": "P12", "nama": "Lukman Hakim", "ipk": 3.70, "nilai_alpro": 62, "pengalaman_organisasi": 2},
    {"id_pendaftar": "P13", "nama": "Maya Puspita", "ipk": 3.45, "nilai_alpro": 86, "pengalaman_organisasi": 0},
    {"id_pendaftar": "P14", "nama": "Naufal Hidayat", "ipk": 3.20, "nilai_alpro": 72, "pengalaman_organisasi": 0},
    {"id_pendaftar": "P15", "nama": "Olivia Siregar", "ipk": 3.75, "nilai_alpro": 80, "pengalaman_organisasi": 3},
]

# ==============================================================================
# 4. SIDEBAR: PENGATURAN PARAMETER AMBANG BATAS & DATA
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Parameter Himpunan")
    st.caption("Atur syarat batas untuk menentukan keanggotaan pendaftar.")

    threshold_alpro = st.slider(
        "Himpunan A (Min. Nilai Alpro)",
        min_value=50, max_value=100, value=80, step=1,
        help="Batas nilai mata kuliah Algoritma & Pemrograman"
    )

    threshold_org = st.slider(
        "Himpunan B (Min. Pengalaman Org)",
        min_value=0, max_value=5, value=2, step=1,
        help="Batas minimal periode kepanitiaan / organisasi"
    )

    threshold_ipk = st.slider(
        "Himpunan C (Min. IPK)",
        min_value=2.00, max_value=4.00, value=3.50, step=0.05,
        help="Batas Indeks Prestasi Kumulatif minimum"
    )

    st.markdown("---")
    st.markdown("### 📁 Sumber Data")
    uploaded_file = st.file_uploader("Unggah CSV Alternatif", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File CSV berhasil dimuat.")
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
            df = pd.DataFrame(DEFAULT_DATA)
    else:
        try:
            df = pd.read_csv("dataset.csv")
        except Exception:
            df = pd.DataFrame(DEFAULT_DATA)

# ==============================================================================
# 5. ENGINE TEORI HIMPUNAN (Set Theory Engine)
# ==============================================================================
set_U = set(df["id_pendaftar"].astype(str).tolist())
set_A = set(df[df["nilai_alpro"] >= threshold_alpro]["id_pendaftar"].astype(str).tolist())
set_B = set(df[df["pengalaman_organisasi"] >= threshold_org]["id_pendaftar"].astype(str).tolist())
set_C = set(df[df["ipk"] >= threshold_ipk]["id_pendaftar"].astype(str).tolist())

OPERASI_DICT = {
    "1. Koordinator Lab": {
        "formula": "A ∩ B ∩ C",
        "desc": "Kandidat berimbang: unggul di pemrograman, teruji di organisasi, dan prestasi akademik konsisten.",
        "result": set_A & set_B & set_C
    },
    "2. Asisten Modul Lanjut": {
        "formula": "A ∩ C",
        "desc": "Kandidat prioritas riset modul: nilai koding tinggi dan IPK tinggi (tanpa syarat organisasi).",
        "result": set_A & set_C
    },
    "3. Siap Operasional Lab": {
        "formula": "A ∪ B",
        "desc": "Pendaftar yang memiliki kemampuan teknis koding minimal ATAU memiliki kepemimpinan organisasi.",
        "result": set_A | set_B
    },
    "4. Asisten Riset / Bank Soal": {
        "formula": "(A ∩ C) − B",
        "desc": "Kandidat unggul teknis dan akademik murni, namun belum memiliki riwayat organisasi.",
        "result": (set_A & set_C) - set_B
    },
    "5. Programmer Murni": {
        "formula": "A − (B ∪ C)",
        "desc": "Kandidat yang hanya lolos kualifikasi pemrograman, tanpa memenuhi kriteria B maupun C.",
        "result": set_A - (set_B | set_C)
    },
    "6. Belum Memenuhi Syarat (Komplemen)": {
        "formula": "U − (A ∪ B ∪ C)",
        "desc": "Pendaftar yang belum menyentuh ambang batas pada kriteria A, B, maupun C.",
        "result": set_U - (set_A | set_B | set_C)
    }
}

# ==============================================================================
# 6. HEADER DASHBOARD
# ==============================================================================
st.markdown("""
<div class="header-box">
    <div>
        <h1 class="header-title">TalentSet</h1>
        <p class="header-sub">Sistem Klasifikasi Calon Asisten Lab Berbasis Teori Himpunan Diskrit</p>
    </div>
    <div class="header-badge">
        PJBL-2 • Pertemuan 5–7
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 7. METRIC CARDS (Slate Dark Theme)
# ==============================================================================
col_u, col_a, col_b, col_c = st.columns(4)

with col_u:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #94a3b8;">Himpunan Semesta (U)</div>
        <div class="metric-number" style="color: #f8fafc;">{len(set_U)}</div>
        <div class="metric-desc">Total pendaftar terdaftar</div>
    </div>
    """, unsafe_allow_html=True)

with col_a:
    pct_a = (len(set_A) / len(set_U) * 100) if len(set_U) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #a5b4fc;">Set A • Pemrograman</div>
        <div class="metric-number" style="color: #818cf8;">{len(set_A)}</div>
        <div class="metric-desc">Alpro ≥ {threshold_alpro} ({pct_a:.0f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    pct_b = (len(set_B) / len(set_U) * 100) if len(set_U) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #67e8f9;">Set B • Organisasi</div>
        <div class="metric-number" style="color: #22d3ee;">{len(set_B)}</div>
        <div class="metric-desc">Org ≥ {threshold_org} periode ({pct_b:.0f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    pct_c = (len(set_C) / len(set_U) * 100) if len(set_U) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #fde047;">Set C • Akademik</div>
        <div class="metric-number" style="color: #facc15;">{len(set_C)}</div>
        <div class="metric-desc">IPK ≥ {threshold_ipk:.2f} ({pct_c:.0f}%)</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 8. KONTROL OPERASI SELEKSI HIMPUNAN
# ==============================================================================
st.write("")
op_key = st.selectbox(
    "Pilih Kategori Penjaringan Berbasis Operasi Himpunan:",
    options=list(OPERASI_DICT.keys())
)

selected_op = OPERASI_DICT[op_key]
hasil_ids = selected_op["result"]

st.markdown(f"""
<div class="op-banner">
    <div class="op-title">{op_key}</div>
    <div class="op-formula">Notasi Matematis: {selected_op['formula']}</div>
    <div class="op-desc">{selected_op['desc']}</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 9. DUA KOLOM: TABEL HASIL PENJARINGAN & DIAGRAM VENN
# ==============================================================================
col_left, col_right = st.columns([1.15, 0.85], gap="large")

with col_left:
    st.markdown(f"##### 📋 Kandidat Terpilih ({len(hasil_ids)} Orang)")

    if len(hasil_ids) > 0:
        df_result = df[df["id_pendaftar"].astype(str).isin(hasil_ids)].copy()

        # Tandai keanggotaan
        df_result["Set A"] = df_result["id_pendaftar"].astype(str).isin(set_A)
        df_result["Set B"] = df_result["id_pendaftar"].astype(str).isin(set_B)
        df_result["Set C"] = df_result["id_pendaftar"].astype(str).isin(set_C)

        st.dataframe(
            df_result,
            column_config={
                "id_pendaftar": st.column_config.TextColumn("ID", width="small"),
                "nama": st.column_config.TextColumn("Nama Mahasiswa", width="medium"),
                "ipk": st.column_config.NumberColumn("IPK", format="%.2f"),
                "nilai_alpro": st.column_config.ProgressColumn(
                    "Alpro",
                    help="Nilai Algoritma & Pemrograman",
                    format="%d",
                    min_value=0,
                    max_value=100
                ),
                "pengalaman_organisasi": st.column_config.NumberColumn("Org (Periode)"),
                "Set A": st.column_config.CheckboxColumn("A", width="small"),
                "Set B": st.column_config.CheckboxColumn("B", width="small"),
                "Set C": st.column_config.CheckboxColumn("C", width="small"),
            },
            hide_index=True,
            width="stretch"
        )

        csv_data = df_result.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Hasil Seleksi (CSV)",
            data=csv_data,
            file_name=f"talentset_{op_key.split('.')[1].strip().lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Himpunan hasil evaluasi adalah himpunan kosong (∅). Tidak ada kandidat yang memenuhi kriteria operasi ini.")

with col_right:
    st.markdown("##### 📊 Visualisasi Diagram Venn")

    # Matplotlib styling menyatu dengan Dark Theme (#1e293b)
    fig, ax = plt.subplots(figsize=(5.4, 4.6), dpi=160)
    fig.patch.set_facecolor('#1e293b')
    ax.set_facecolor('#1e293b')

    # Diagram Venn 3 Himpunan dengan warna kontras & elegan
    v = venn3(
        subsets=(set_A, set_B, set_C),
        set_labels=('Set A (Koding)', 'Set B (Org)', 'Set C (IPK)'),
        set_colors=('#6366f1', '#06b6d4', '#f59e0b'),
        alpha=0.45,
        ax=ax
    )

    # Garis lingkaran pembatas rapi
    venn3_circles(
        subsets=(set_A, set_B, set_C),
        linestyle='solid',
        linewidth=1.2,
        color='#94a3b8',
        ax=ax
    )

    # Format tipografi label agar kontras dan mudah dibaca
    if v:
        for lbl in v.set_labels:
            if lbl:
                lbl.set_fontsize(9)
                lbl.set_fontweight('bold')
                lbl.set_color('#f8fafc')
        for sub in v.subset_labels:
            if sub:
                sub.set_fontsize(9.5)
                sub.set_fontweight('bold')
                sub.set_color('#ffffff')

    # Keterangan komplemen di luar lingkaran
    komplemen_count = len(set_U - (set_A | set_B | set_C))
    ax.text(
        0.5, -0.06,
        f"Luar Lingkaran (Komplemen U): {komplemen_count} Mahasiswa",
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes,
        fontsize=8.5,
        color='#94a3b8',
        fontweight='medium'
    )

    plt.tight_layout()
    st.pyplot(fig)

# ==============================================================================
# 10. COLLAPSIBLE TABEL SEMESTA LENGKAP
# ==============================================================================
st.write("")
with st.expander(f"🔍 Tampilkan Seluruh Data Semesta (U) • {len(df)} Record Terdaftar"):
    st.dataframe(df, width="stretch", hide_index=True)