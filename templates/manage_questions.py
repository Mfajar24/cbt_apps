import streamlit as st
import sqlite3

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    return sqlite3.connect('database.db')

# Fungsi untuk mendapatkan soal dari database
def get_questions(search_text="", sort_by="question_id"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Menambahkan query pencarian
    query = f"SELECT * FROM questions WHERE question_text LIKE ? ORDER BY {sort_by} ASC"
    cursor.execute(query, ('%' + search_text + '%',))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Fungsi untuk menghapus soal
def delete_question(question_id):
    conn = get_db_connection()
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
    st.title("📋 Pengelolaan Soal")

    # Fitur pencarian soal
    search_text = st.text_input("Cari Soal (Ketik teks soal)", "")

    # Fitur sortir soal
    sort_by = st.selectbox("Urutkan Berdasarkan", ["question_id", "question_text"])

    # Mendapatkan daftar soal dari database dengan filter dan sorting
    questions = get_questions(search_text, sort_by)

    if not questions:
        st.warning("Tidak ada soal yang ditemukan berdasarkan pencarian.")
    
    # Menampilkan soal dengan tata letak rapi
    for question in questions:
        question_id = question[0]  # ID soal
        question_text = question[1]  # Teks soal
        option_a = question[2]  # Pilihan A
        option_b = question[3]  # Pilihan B
        option_c = question[4]  # Pilihan C
        option_d = question[5]  # Pilihan D

        st.markdown(f"### Soal Nomor {question_id}")
        st.markdown(f"**Soal**: {question_text}")
        st.markdown(f"**Pilihan A**: {option_a}")
        st.markdown(f"**Pilihan B**: {option_b}")
        st.markdown(f"**Pilihan C**: {option_c}")
        st.markdown(f"**Pilihan D**: {option_d}")
        
        col1, col2 = st.columns(2)
        with col1:
            # Tombol hapus soal
            if st.button(f"❌ Hapus Soal Nomor {question_id}", key=f"delete_{question_id}"):
                delete_question(question_id)
                st.rerun()  # Memaksa refresh halaman setelah menghapus soal

        with col2:
            # Tombol edit soal
            if st.button(f"✏️ Edit Soal Nomor {question_id}", key=f"edit_{question_id}"):
                # Menyimpan ID soal yang akan diedit di session_state
                st.session_state["edit_question_id"] = question_id
                # Pindah ke halaman edit
                st.session_state.page = "edit_question"
                st.rerun()  # Memaksa aplikasi untuk berpindah ke halaman edit

    # Tombol untuk menavigasi ke halaman tambah soal
    if st.button("➕ Tambahkan Soal Baru"):
        st.session_state.page = "upload_questions"  # Set state untuk pindah ke tambah soal
        st.rerun()  # Memaksa halaman berpindah setelah menekan tombol

    # Tombol untuk kembali ke halaman utama
    if st.button("🏠 Kembali ke Home"):
        st.session_state.page = "home"  # Atur halaman menjadi 'home'
        st.rerun()  # Memaksa halaman berpindah ke halaman utama

# Memastikan halaman ini bisa dipanggil oleh main.py
if __name__ == "__main__":
    manage_questions()
