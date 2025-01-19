import streamlit as st
import sqlite3

def form():
    # Menambahkan CSS untuk mempercantik tampilan
    st.markdown("""
    <style>
        .form-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .form-container h1 {
            text-align: center;
            color: #4CAF50;
            font-size: 24px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput input {
            font-size: 16px;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Formulir Ujian")

    # Fungsi navigasi ke halaman lain
    def navigate_to(page):
        st.session_state.page = page

    # Form input
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    nama = st.text_input("Nama", key="form_nama")
    kelas = st.text_input("Kelas", key="form_kelas")
    npm = st.text_input("NPM", key="form_npm")
    mata_pelajaran = st.text_input("Mata Pelajaran", key="form_mata_pelajaran")
    nama_dosen = st.text_input("Nama Dosen", key="form_nama_dosen")

    st.markdown('</div>', unsafe_allow_html=True)

    # Button untuk submit
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

    # Button kembali ke menu utama
    if st.button("Kembali ke Menu Utama"):
        navigate_to("home")

