# ==============================================================
# 📊 DASHBOARD ANALISIS POLUTAN UDARA BERBASIS STREAMLIT
# ==============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point

# --------------------------------------------------------------
# 🧭 PENGATURAN AWAL
# --------------------------------------------------------------
st.set_page_config(page_title="Dashboard Analisis Polutan Udara Kota Changping", layout="wide")
sns.set(style='whitegrid')

# --------------------------------------------------------------
# 📥 BACA DATA
# --------------------------------------------------------------
# Data berisi kolom [year, month, day, hour, PM2.5, PM10, SO2, NO2, CO, O3]
prsa_df = pd.read_csv("main_data.csv")

# Gabungkan kolom tanggal
prsa_df["datetime"] = pd.to_datetime(prsa_df[["year", "month", "day"]])

# Daftar polutan
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]

# --------------------------------------------------------------
# 🏙️ JUDUL UTAMA
# --------------------------------------------------------------
st.title("Konsentrasi Rata-Rata Polutan Udara di Kota Changping")
st.markdown("### Periode pengamatan: Maret 2013 – Februari 2017")
st.markdown("---")

# --------------------------------------------------------------
# 🧩 TABS LAYOUT
# --------------------------------------------------------------
tab1, tab2, tab3, tab4= st.tabs([
    "Rata-Rata Harian",
    "Rata-Rata Tahunan",
    "Rata-Rata Bulanan",
    "Rata-Rata Per Jam"
])

# ==============================================================
# TAB 1 — Rata-Rata Harian
# ==============================================================
with tab1:
    st.subheader("📅 Konsentrasi Rata-Rata Harian")

    # Filter waktu
    min_date = prsa_df["datetime"].min()
    max_date = prsa_df["datetime"].max()

    start_date, end_date = st.date_input(
        "Pilih rentang waktu:",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    filtered_df = prsa_df[
        (prsa_df["datetime"] >= pd.to_datetime(start_date)) &
        (prsa_df["datetime"] <= pd.to_datetime(end_date))
    ]

    # Pilih polutan
    selected_pollutant = st.radio("Pilih polutan:", pollutants, horizontal=True)

    # Hitung rata-rata harian
    daily_avg = filtered_df.groupby("datetime")[selected_pollutant].mean().reset_index()

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(daily_avg["datetime"], daily_avg[selected_pollutant], color='purple', linewidth=2)
    plt.title(f"Konsentrasi Rata-Rata Harian {selected_pollutant}", fontsize=14)
    plt.xlabel("Tanggal")
    plt.ylabel(f"Konsentrasi rata-rata {selected_pollutant} (µg/m³)")
    plt.tight_layout()
    st.pyplot(plt)

# ==============================================================
# TAB 2 — Rata-Rata Tahunan
# ==============================================================
with tab2:
    st.subheader("📆 Konsentrasi Rata-Rata Tahunan")

    selected_pollutant = st.radio("Pilih polutan:", pollutants, horizontal=True, key="year_pollutant")
    yearly_avg = prsa_df.groupby("year")[selected_pollutant].mean().reset_index()

    plt.figure(figsize=(10, 5))
    sns.barplot(x="year", y=selected_pollutant, data=yearly_avg, color="mediumorchid")
    plt.title(f"Konsentrasi Rata-Rata {selected_pollutant} per Tahun", fontsize=14)
    plt.xlabel("Tahun")
    plt.ylabel(f"Konsentrasi rata-rata {selected_pollutant} (µg/m³)")
    plt.tight_layout()
    st.pyplot(plt)

# ==============================================================
# TAB 3 — Rata-Rata Bulanan
# ==============================================================
with tab3:
    st.subheader("🗓️ Konsentrasi Rata-Rata Bulanan")

    selected_pollutant = st.radio("Pilih polutan:", pollutants, horizontal=True, key="month_pollutant")
    monthly_avg = prsa_df.groupby("month")[selected_pollutant].mean().reset_index()

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    monthly_avg["month"] = monthly_avg["month"].map(dict(zip(range(1, 13), months)))

    plt.figure(figsize=(10, 5))
    sns.barplot(x="month", y=selected_pollutant, data=monthly_avg, color="violet")
    plt.title(f"Konsentrasi Rata-Rata {selected_pollutant} per Bulan", fontsize=14)
    plt.xlabel("Bulan")
    plt.ylabel(f"Konsentrasi rata-rata {selected_pollutant} (µg/m³)")
    plt.tight_layout()
    st.pyplot(plt)

# ==============================================================
# TAB 4 — Rata-Rata Per Jam
# ==============================================================
with tab4:
    st.subheader("⏰ Konsentrasi Rata-Rata per Jam")

    selected_pollutant = st.radio("Pilih polutan:", pollutants, horizontal=True, key="hour_pollutant")
    hourly_avg = prsa_df.groupby("hour")[selected_pollutant].mean().reset_index()
    hourly_avg["hour_label"] = hourly_avg["hour"].apply(lambda x: f"{x:02d}.00")

    plt.figure(figsize=(10, 6))
    sns.barplot(y="hour_label", x=selected_pollutant, data=hourly_avg, color="plum")
    plt.title(f"Konsentrasi Rata-Rata {selected_pollutant} per Jam", fontsize=14)
    plt.xlabel(f"Konsentrasi rata-rata {selected_pollutant} (µg/m³)")
    plt.ylabel("Pukul")
    plt.tight_layout()
    st.pyplot(plt)

