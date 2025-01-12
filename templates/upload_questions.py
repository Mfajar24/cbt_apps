import streamlit as st
import sqlite3
import pandas as pd

def add_question_from_form():
    st.title("Tambah Soal Pilihan Ganda (Formulir)")

    question_text = st.text_input("Soal")
    option_a = st.text_input("Pilihan A")
    option_b = st.text_input("Pilihan B")
    option_c = st.text_input("Pilihan C")
    option_d = st.text_input("Pilihan D")
    
    # Menyediakan opsi untuk memilih jawaban yang benar berdasarkan teks
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

def add_question_from_excel():
    st.title("Tambah Soal Pilihan Ganda (Melalui Excel)")
    
    # Menampilkan informasi format Excel
    st.markdown("""
    ### Format Excel
    Untuk mengupload soal melalui Excel, pastikan file Anda mengikuti format berikut:
    
    | question_text       | option_a      | option_b      | option_c      | option_d      | correct_option |
    |---------------------|---------------|---------------|---------------|---------------|----------------|
    | 1+1                 | 2             | 1             |  3            | 4             | 2              |
    
    Pastikan file Excel Anda memiliki kolom berikut:
    - `question_text`: Teks soal
    - `option_a`: Pilihan A
    - `option_b`: Pilihan B
    - `option_c`: Pilihan C
    - `option_d`: Pilihan D
    - `correct_option`: Jawaban yang benar 
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

def upload_questions():
    # Pilihan untuk menambah soal
    option = st.selectbox("Pilih cara menambah soal", ["Formulir", "Excel"])

    if option == "Formulir":
        add_question_from_form()
    elif option == "Excel":
        add_question_from_excel()

    # Menambahkan tombol kembali
    if st.button("Kembali"):
        # Mengatur halaman yang ingin kembali
        st.session_state.page = "manage_questions"  # Sesuaikan dengan halaman sebelumnya

if __name__ == "__main__":
    upload_questions()
