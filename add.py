import sqlite3

def update_database():
    # Membuat koneksi ke database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Menghapus tabel 'questions' jika ada
    cursor.execute('DROP TABLE IF EXISTS questions')
    print("Tabel 'questions' berhasil dihapus.")

    # Membuat tabel 'questions' yang baru dengan struktur pilihan ganda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL
        )
    ''')
    print("Tabel 'questions' berhasil dibuat dengan struktur pilihan ganda.")

    # Menghapus tabel 'exam' jika ada
    cursor.execute('DROP TABLE IF EXISTS exam')
    print("Tabel 'exam' berhasil dihapus.")

    # Membuat tabel 'exam' yang baru
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exam (
            exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score REAL NOT NULL,
            date_taken TEXT NOT NULL
        )
    ''')
    print("Tabel 'exam' berhasil dibuat.")

    # Menghapus tabel 'user_answers' jika ada
    cursor.execute('DROP TABLE IF EXISTS user_answers')
    print("Tabel 'user_answers' berhasil dihapus.")

    # Membuat tabel 'user_answers' yang baru
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_answers (
            answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions (question_id)
        )
    ''')
    print("Tabel 'user_answers' berhasil dibuat.")

    # Menghapus tabel 'exam_results' jika ada
    cursor.execute('DROP TABLE IF EXISTS exam_results')
    print("Tabel 'exam_results' berhasil dihapus.")

    # Membuat tabel 'exam_results' yang baru
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exam_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kelas TEXT NOT NULL,
            npm TEXT NOT NULL,
            mata_pelajaran TEXT NOT NULL,
            nama_dosen TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("Tabel 'exam_results' berhasil dibuat.")

    # Menghapus tabel 'kisi_kisi' jika ada
    cursor.execute('DROP TABLE IF EXISTS kisi_kisi')
    print("Tabel 'kisi_kisi' berhasil dihapus.")

    # Membuat tabel 'kisi_kisi' yang baru
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kisi_kisi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topik TEXT NOT NULL,
            deskripsi TEXT NOT NULL
        )
    ''')
    print("Tabel 'kisi_kisi' berhasil dibuat.")

# Menambahkan kolom 'role' pada tabel 'users' jika belum ada
    try:
        cursor.execute('''
            ALTER TABLE user ADD COLUMN role TEXT DEFAULT 'user'
        ''')
        print("Kolom 'role' berhasil ditambahkan pada tabel 'users'.")
    except sqlite3.OperationalError:
        print("Kolom 'role' sudah ada di tabel 'users'.")


    # Menutup koneksi
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_database()
