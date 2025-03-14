# Sistem Pendukung Keputusan Penentuan Warga Penerima Bantuan Sosial

Aplikasi ini merupakan sistem pendukung keputusan (DSS) berbasis Streamlit yang menerapkan metode **Simple Additive Weighting (SAW)** dan **Weighted Product (WP)** untuk menentukan warga penerima bantuan sosial berdasarkan kriteria tertentu.

## 📌 Fitur Utama
- Memuat dan menampilkan data penduduk dari file CSV.
- Melakukan normalisasi data menggunakan metode SAW dan WP.
- Menghitung skor peringkat berdasarkan metode SAW dan WP.
- Menampilkan daftar penerima bantuan sosial berdasarkan metode SAW dan WP.
- Memungkinkan pengguna untuk memasukkan bobot kriteria melalui sidebar.

## 🛠️ Instalasi dan Menjalankan Aplikasi
### 1. Clone Repository (Opsional)
Jika kode ini ada dalam repository, clone terlebih dahulu:
```bash
git clone https://github.com/febriananursyifarizqi/SPK-Bansos.git
```

### 2. Persyaratan Sistem
Pastikan Python telah terinstal (disarankan versi 3.8 atau lebih baru).

### 3. Install Dependencies
Jalankan perintah berikut untuk menginstal semua dependensi yang diperlukan:
```bash
pip install streamlit pandas numpy
```

### 4. Menjalankan Aplikasi
Jalankan perintah berikut di terminal atau command prompt:
```bash
streamlit run app.py
```
Pastikan Anda berada di direktori yang benar sebelum menjalankan perintah tersebut.