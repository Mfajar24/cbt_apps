import streamlit as st
import sqlite3
import pandas as pd

# Fungsi untuk menambah soal melalui formulir
def add_question_from_form():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.header("Tambah Soal Pilihan Ganda (Formulir)")

    # Input untuk soal dan pilihan
    question_text = st.text_input("Soal")
    option_a = st.text_input("Pilihan A")
    option_b = st.text_input("Pilihan B")
    option_c = st.text_input("Pilihan C")
    option_d = st.text_input("Pilihan D")
    
    # Menyediakan opsi untuk memilih jawaban yang benar
    correct_option = st.selectbox("Jawaban yang benar", [option_a, option_b, option_c, option_d])

    if st.button("Tambah Soal"):
        if question_text and option_a and option_b and option_c and option_d and correct_option:
            # Menyimpan soal ke database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, correct_option)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (question_text, option_a, option_b, option_c, option_d, correct_option))
            conn.commit()
            conn.close()
            st.success("Soal berhasil ditambahkan!")
        else:
            st.error("Semua kolom harus diisi!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Fungsi untuk menambah soal melalui Excel
def add_question_from_excel():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.header("Tambah Soal Pilihan Ganda (Melalui Excel)")

    # Menampilkan informasi format Excel
    st.markdown("""
    ### Format Excel
    Untuk mengupload soal melalui Excel, pastikan file Anda mengikuti format berikut:
    
    | question_text | option_a | option_b | option_c | option_d | correct_option |
    |---------------|----------|----------|----------|----------|----------------|
    | 1+1           | 2        | 1        | 3        | 4        | 2              |
    """)
    
    uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])
    
    if uploaded_file is not None:
        # Membaca file Excel
        df = pd.read_excel(uploaded_file)

        # Menampilkan preview data
        st.write("Data yang diunggah:", df)

        if st.button("Tambah Soal dari Excel"):
            # Menyimpan data soal ke database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            for index, row in df.iterrows():
                cursor.execute(''' 
                    INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, correct_option)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['question_text'], row['option_a'], row['option_b'], row['option_c'], row['option_d'], row['correct_option']))
            
            conn.commit()
            conn.close()
            st.success("Soal berhasil ditambahkan dari Excel!")

    st.markdown('</div>', unsafe_allow_html=True)

# Fungsi untuk menambah kisi-kisi melalui formulir
def add_kisi_kisi_from_form():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.header("Tambah Kisi-Kisi (Formulir)")

    topik = st.text_input("Topik")
    deskripsi = st.text_area("Deskripsi")

    if st.button("Tambah Kisi-Kisi"):
        if topik and deskripsi:
            # Menyimpan kisi-kisi ke database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO kisi_kisi (topik, deskripsi)
                VALUES (?, ?)
            ''', (topik, deskripsi))
            conn.commit()
            conn.close()
            st.success("Kisi-Kisi berhasil ditambahkan!")
        else:
            st.error("Semua kolom harus diisi!")

    st.markdown('</div>', unsafe_allow_html=True)

# Fungsi untuk menambah kisi-kisi melalui Excel
def add_kisi_kisi_from_excel():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.header("Tambah Kisi-Kisi (Melalui Excel)")

    # Menampilkan informasi format Excel
    st.markdown("""
    ### Format Excel
    Untuk mengupload kisi-kisi melalui Excel, pastikan file Anda mengikuti format berikut:
    
    | topik        | deskripsi                             |
    |--------------|---------------------------------------|
    | Matematika   | Integrasi dan Turunan                |
    | Fisika       | Hukum Newton dan Dinamika            |
    """)
    
    uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])
    
    if uploaded_file is not None:
        # Membaca file Excel
        df = pd.read_excel(uploaded_file)

        # Menampilkan preview data
        st.write("Data yang diunggah:", df)

        if st.button("Tambah Kisi-Kisi dari Excel"):
            # Menyimpan data kisi-kisi ke database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            for index, row in df.iterrows():
                cursor.execute(''' 
                    INSERT INTO kisi_kisi (topik, deskripsi)
                    VALUES (?, ?)
                ''', (row['topik'], row['deskripsi']))
            
            conn.commit()
            conn.close()
            st.success("Kisi-Kisi berhasil ditambahkan dari Excel!")

    st.markdown('</div>', unsafe_allow_html=True)

# Fungsi utama untuk upload soal dan kisi-kisi
def upload_questions():
    st.markdown("""
    <style>
        .form-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .form-container h1 {
            text-align: center;
            color: #4CAF50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True)

    # Pilihan untuk menambah soal atau kisi-kisi
    option = st.sidebar.selectbox("Pilih cara menambah soal atau kisi-kisi", ["Soal", "Kisi-Kisi"])

    if option == "Soal":
        add_option = st.selectbox("Pilih cara menambah soal", ["Formulir", "Excel"])

        if add_option == "Formulir":
            add_question_from_form()
        elif add_option == "Excel":
            add_question_from_excel()

    elif option == "Kisi-Kisi":
        add_option = st.selectbox("Pilih cara menambah kisi-kisi", ["Formulir", "Excel"])

        if add_option == "Formulir":
            add_kisi_kisi_from_form()
        elif add_option == "Excel":
            add_kisi_kisi_from_excel()

    # Menambahkan tombol kembali
    if st.button("Kembali"):
        st.session_state.page = "home"  # Mengarahkan kembali ke halaman utama

if __name__ == "__main__":
    upload_questions()
