import streamlit as st
import sqlite3

def exam():
    # Menambahkan CSS untuk mempercantik tampilan
    st.markdown("""
    <style>
        .exam-container {
            background-color: #fafafa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .exam-title {
            text-align: center;
            color: #4CAF50;
            font-size: 32px;
            margin-bottom: 20px;
        }
        .question-container {
            background-color: #ffffff;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .stRadio>label {
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            background-color: #f0f0f0;
            margin-bottom: 10px;
            cursor: pointer;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Ujian")

    # Ambil soal dari database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question_id, question_text, option_a, option_b, option_c, option_d FROM questions")
    questions = cursor.fetchall()

    if not questions:
        st.warning("Belum ada soal tersedia. Silakan tambahkan soal terlebih dahulu.")
        return

    answers = {}

    # Tampilkan setiap soal
    st.markdown('<div class="exam-container">', unsafe_allow_html=True)
    st.markdown('<div class="exam-title">Ujian Pilihan Ganda</div>', unsafe_allow_html=True)

    for question in questions:
        question_id, question_text, option_a, option_b, option_c, option_d = question
        st.markdown(f'<div class="question-container">', unsafe_allow_html=True)
        st.subheader(f"**{question_text}**")

        # Pilihan jawaban
        choices = [option_a, option_b, option_c, option_d]
        answers[question_id] = st.radio(f"Pilih jawaban:", choices, key=f"q{question_id}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Tombol submit untuk mengirimkan jawaban
    submit_button = st.button("Submit Jawaban", key="submit_exam")
    if submit_button:
        if any(answer is None for answer in answers.values()):
            st.error("Pastikan semua soal telah dijawab sebelum mengirimkan.")
            return

        # Simpan jawaban yang dipilih oleh pengguna
        cursor.execute("DELETE FROM user_answers WHERE user_id = ?", (1,))  # Hapus jawaban sebelumnya untuk user_id 1
        for question_id, answer in answers.items():
            cursor.execute(''' 
                INSERT INTO user_answers (question_id, answer, user_id)
                VALUES (?, ?, ?)
            ''', (question_id, answer, 1))  # User ID diisi contoh 1

        conn.commit()
        conn.close()

        st.success("Jawaban berhasil disimpan!")

        # Pindah ke halaman hasil ujian
        st.session_state.page = "result"  # Sesuaikan dengan nama fungsi di `result.py`

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    exam()
