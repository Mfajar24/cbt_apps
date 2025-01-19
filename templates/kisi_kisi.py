import streamlit as st
import sqlite3

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    return sqlite3.connect('database.db')

# Fungsi untuk mendapatkan kisi-kisi dari database
def get_kisi_kisi():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM kisi_kisi ORDER BY id ASC')  # Ganti 'id' sesuai dengan kolom ID yang ada di tabel
    kisi_kisi_data = cursor.fetchall()
    conn.close()
    return kisi_kisi_data

# Halaman untuk menampilkan Kisi-Kisi
def kisi_kisi():
    st.title("📑 Kisi-Kisi Ujian")

    # Mendapatkan daftar kisi-kisi dari database
    kisi_kisi_data = get_kisi_kisi()

    if kisi_kisi_data:
        for kisi in kisi_kisi_data:
            topik = kisi[1]  # Ganti dengan kolom yang sesuai untuk topik
            deskripsi = kisi[2]  # Ganti dengan kolom yang sesuai untuk deskripsi

            st.subheader(topik)
            st.write(deskripsi)
            st.markdown("---")  # Pemisah antar kisi-kisi
    else:
        st.warning("Tidak ada kisi-kisi yang tersedia di database.")

    # Tombol untuk kembali ke menu utama
    if st.button("Kembali ke Menu Utama 🏠"):
        st.session_state.page = "home"  # Set session_state untuk berpindah ke halaman home

