import streamlit as st
import sqlite3

def form():
    st.title("Formulir Ujian")

    # Fungsi navigasi ke halaman lain
    def navigate_to(page):
        st.session_state.page = page

    # Form input
    nama = st.text_input("Nama", key="form_nama")
    kelas = st.text_input("Kelas", key="form_kelas")
    npm = st.text_input("NPM", key="form_npm")
    mata_pelajaran = st.text_input("Mata Pelajaran", key="form_mata_pelajaran")
    nama_dosen = st.text_input("Nama Dosen", key="form_nama_dosen")

    if st.button("Submit"):
        if not all([nama, kelas, npm, mata_pelajaran, nama_dosen]):
            st.error("Semua field harus diisi!")
        else:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO exam_results (nama, kelas, npm, mata_pelajaran, nama_dosen)
                VALUES (?, ?, ?, ?, ?)
            ''', (nama, kelas, npm, mata_pelajaran, nama_dosen))
            conn.commit()
            conn.close()
            st.success("Data berhasil disimpan!")

            # Pindah ke halaman exam
            navigate_to("exam")

    if st.button("Kembali ke Menu Utama"):
        navigate_to("home")
