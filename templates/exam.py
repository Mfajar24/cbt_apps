import streamlit as st
import sqlite3

def exam():
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
    for question in questions:
        question_id, question_text, option_a, option_b, option_c, option_d = question
        st.subheader(f"**{question_text}**")

        # Pilihan jawaban
        choices = [option_a, option_b, option_c, option_d]
        answers[question_id] = st.radio(f"Pilih jawaban:", choices, key=f"q{question_id}")

    # Tombol submit untuk mengirimkan jawaban
    if st.button("Submit Jawaban"):
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

if __name__ == "__main__":
    exam()
