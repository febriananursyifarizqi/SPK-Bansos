import streamlit as st
import pandas as pd
import numpy as np
import os

# Normalisasi SAW
def normalize_saw(df):
    normalized_df = df.iloc[:, 1:].copy().astype(float)
    for col in df.columns:
        if col in criteria_types:
            if criteria_types[col] == "benefit":
                normalized_df[col] = df[col] / df[col].max()
            else:  # Cost criteria
                normalized_df[col] = df[col].min() / df[col]
    return normalized_df

# Normalisasi WP dengan pemangkatan bobot
def normalize_wp(df):
    normalized_df = df.iloc[:, 1:].copy().astype(float)
    for col in df.columns:
        if col in criteria_types:
            if criteria_types[col] == "cost":
                normalized_df[col] = 1 / df[col]
    return normalized_df

# Perhitungan SAW
def calculate_saw(df):
    normalized_df = normalize_saw(df)
    saw_scores = (normalized_df * list(weights.values())).sum(axis=1)  # Memastikan bobot diterapkan dengan benar
    return saw_scores

# Perhitungan WP
def calculate_wp(df):
    normalized_df = normalize_wp(df)
    wp_scores = np.prod(np.power(normalized_df, list(weights.values())), axis=1)  # Memastikan bobot diterapkan dengan eksponen
    return wp_scores

st.title("Sistem Pendukung Keputusan Penentuan Warga Penerima Bantuan Sosial📦")

# Load dataset dengan error handling
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = f"{script_dir}/datapenduduk.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("File data tidak ditemukan!")
    st.stop()

# Menampilkan data penduduk
st.subheader("Data Penduduk")
st.dataframe(df)

criteria_types = {
    "Usia (C1)": "benefit",
    "Pendidikan (C2)": "cost",
    "Pekerjaan (C3)": "cost",
    "Penghasilan (C4)": "cost",
    "Tanggungan (C5)": "benefit",
    "Tempat Tinggal (C6)": "cost",
    "Keluarga Sakit (C7)": "benefit",
    "Keluarga Lansia (C8)": "benefit",
}

# Sidebar untuk memasukkan bobot berdasarkan preferensi decision maker
with st.sidebar:
    st.image(f"{script_dir}/bansos.png")

    st.subheader("Masukkan Bobot Kriteria")
    weights = {}

    with st.form("Preferensi"):

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            weights["Usia (C1)"] = st.number_input("C1", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
            weights["Tanggungan (C5)"] = st.number_input("C5", min_value=0.0, max_value=1.0, value=0.20, step=0.01)

        with col2:
            weights["Pendidikan (C2)"] = st.number_input("C2", min_value=0.0, max_value=1.0, value=0.10, step=0.01)
            weights["Tempat Tinggal (C6)"] = st.number_input("C6", min_value=0.0, max_value=1.0, value=0.10, step=0.01)

        with col3:
            weights["Pekerjaan (C3)"] = st.number_input("C3", min_value=0.0, max_value=1.0, value=0.15, step=0.01)
            weights["Keluarga Sakit (C7)"] = st.number_input("C7", min_value=0.0, max_value=1.0, value=0.08, step=0.01)

        with col4:
            weights["Penghasilan (C4)"] = st.number_input("C4", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
            weights["Keluarga Lansia (C8)"] = st.number_input("C8", min_value=0.0, max_value=1.0, value=0.07, step=0.01)
        
        if st.form_submit_button("Simpan Preferensi"):
            if sum(weights.values())==1:
                st.success("Preferensi tersimpan")
            else:
                st.error("Total semua bobot harus sama dengan 1!")

st.subheader("Seleksi Warga Penerima Bantuan Sosial")

# Input jumlah penerima bantuan
n = st.number_input("Masukkan jumlah penerima bantuan:", min_value=1, max_value=len(df), value=10, step=1)
if n > len(df):
    st.error("Jumlah penerima bantuan melebihi jumlah penduduk!")

if st.button("Seleksi Penerima Bansos"):

    # Perhitungan skor SAW dan WP
    saw_scores = calculate_saw(df)
    wp_scores = calculate_wp(df)
    df["SAW Score"] = saw_scores
    df["WP Score"] = wp_scores

    # Peringkat berdasarkan skor SAW dan WP
    df_sorted_saw = df.sort_values(by="SAW Score", ascending=False)
    df_sorted_wp = df.sort_values(by="WP Score", ascending=False)

    # Menamapilkan hasil penerima bansos berdasarkan pemeringkatan
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Penerima Bantuan Sosial Berdasarkan Metode SAW")
        st.dataframe(df_sorted_saw[["Nama", "SAW Score"]].head(n))
    with col2:
        st.markdown("Penerima Bantuan Sosial Berdasarkan Metode WP")
        st.dataframe(df_sorted_wp[["Nama", "WP Score"]].head(n))