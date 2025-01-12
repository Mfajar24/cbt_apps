import streamlit as st
import sqlite3

def get_questions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions ORDER BY question_id ASC')  # Urutkan berdasarkan ID
    questions = cursor.fetchall()
    conn.close()
    return questions

def delete_question(question_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Hapus soal berdasarkan ID
    cursor.execute('DELETE FROM questions WHERE question_id = ?', (question_id,))
    conn.commit()
    
    # Reset ulang nomor soal
    cursor.execute('''
        UPDATE questions
        SET question_id = question_id - 1
        WHERE question_id > ?
    ''', (question_id,))
    conn.commit()
    conn.close()

    # Tandai perubahan untuk memaksa pemuatan ulang halaman
    st.session_state["questions_updated"] = True
    st.success(f"Soal dengan ID {question_id} berhasil dihapus!")

def manage_questions():
    st.title("Pengelolaan Soal")

    # Memastikan pembaruan hanya terjadi setelah interaksi
    if "questions_updated" in st.session_state and st.session_state["questions_updated"]:
        st.session_state["questions_updated"] = False

    # Mendapatkan daftar soal dari database
    questions = get_questions()

    for question in questions:
        question_id = question[0]  # ID soal
        question_text = question[1]  # Teks soal
        option_a = question[2]  # Pilihan A
        option_b = question[3]  # Pilihan B
        option_c = question[4]  # Pilihan C
        option_d = question[5]  # Pilihan D

        # Menampilkan soal dan pilihan jawaban
        st.write(f"Nomor: {question_id} - {question_text}")
        st.write(f"Pilihan A: {option_a}")
        st.write(f"Pilihan B: {option_b}")
        st.write(f"Pilihan C: {option_c}")
        st.write(f"Pilihan D: {option_d}")
        
        # Tombol hapus soal
        if st.button(f"Hapus Soal Nomor {question_id}", key=f"delete_{question_id}"):
            delete_question(question_id)
            # Pemindahan logika ke state untuk mereset tampilan
            return

    # Tombol untuk menavigasi ke halaman tambah soal
    if st.button("Tambahkan Soal Baru"):
        st.session_state.page = "upload_questions"  # Set state untuk pindah ke tambah soal

if __name__ == "__main__":
    if "questions_updated" not in st.session_state:
        st.session_state["questions_updated"] = False  # Inisialisasi state
    manage_questions()
