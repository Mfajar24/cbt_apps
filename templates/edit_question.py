import streamlit as st
import sqlite3

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    return sqlite3.connect('database.db')

# Fungsi untuk mendapatkan soal berdasarkan ID
def get_question_by_id(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE question_id = ?', (question_id,))
    question = cursor.fetchone()
    conn.close()
    return question

# Fungsi untuk memperbarui soal di database
def update_question(question_id, new_text, new_option_a, new_option_b, new_option_c, new_option_d):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update soal dan pilihan di database
    cursor.execute('''
        UPDATE questions
        SET question_text = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?
        WHERE question_id = ?
    ''', (new_text, new_option_a, new_option_b, new_option_c, new_option_d, question_id))
    conn.commit()
    conn.close()

    st.success(f"Soal dengan ID {question_id} berhasil diperbarui!")

# Fungsi untuk halaman edit soal
def edit_question_page():
    st.title("Edit Soal")
    
    # Mendapatkan ID soal yang akan diedit dari session_state
    question_id = st.session_state.get("edit_question_id")
    
    if question_id is None:
        st.error("Tidak ada soal yang dipilih untuk diedit.")
        return
    
    # Mendapatkan data soal dari database
    question = get_question_by_id(question_id)
    
    if question:
        question_text, option_a, option_b, option_c, option_d = question[1], question[2], question[3], question[4], question[5]

        # Form untuk mengedit soal
        with st.form(key=f"edit_form_{question_id}"):
            new_text = st.text_area("Teks Soal", value=question_text)
            new_option_a = st.text_input("Pilihan A", value=option_a)
            new_option_b = st.text_input("Pilihan B", value=option_b)
            new_option_c = st.text_input("Pilihan C", value=option_c)
            new_option_d = st.text_input("Pilihan D", value=option_d)
            
            submit_button = st.form_submit_button("Simpan Perubahan")
            if submit_button:
                update_question(question_id, new_text, new_option_a, new_option_b, new_option_c, new_option_d)
                st.session_state.page = "home"  # Kembali ke halaman utama
    
    else:
        st.error(f"Soal dengan ID {question_id} tidak ditemukan.")
    
    # Tombol kembali ke halaman utama atau halaman sebelumnya
    if st.button("Kembali ke Halaman Utama 🏠"):
        st.session_state.page = "home"  # Mengatur kembali halaman utama
        # Tidak perlu rerun karena aplikasi akan secara otomatis berpindah ke halaman utama

if __name__ == "__main__":
    edit_question_page()
