import streamlit as st
import sqlite3
from datetime import datetime
from reportlab.pdfgen import canvas
import os

def save_results_as_pdf(user_id, correct_count, total_questions, score):
    # Buat folder untuk menyimpan file PDF jika belum ada
    output_dir = "hasil_ujian"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Nama file PDF berdasarkan user_id dan waktu
    filename = os.path.join(output_dir, f"user_{user_id}_hasil_ujian.pdf")
    pdf = canvas.Canvas(filename)

    # Informasi header PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, "Hasil Ujian")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"ID Pengguna: {user_id}")
    pdf.drawString(50, 740, f"Jumlah Soal: {total_questions}")
    pdf.drawString(50, 720, f"Jawaban Benar: {correct_count}")
    pdf.drawString(50, 700, f"Skor: {score:.2f}%")
    pdf.drawString(50, 680, f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pdf.save()

    return filename

def calculate_and_display_results():
    st.title("Hasil Ujian")

    # Sambungkan ke database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Ambil jumlah soal
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]

    if total_questions == 0:
        st.warning("Tidak ada soal di database.")
        return

    # Ambil jawaban pengguna
    user_id = 1  # Ganti dengan logika untuk mengambil user_id sebenarnya
    cursor.execute("SELECT question_id, answer FROM user_answers WHERE user_id = ?", (user_id,))
    user_answers = cursor.fetchall()

    # Ambil jawaban benar dari tabel questions
    cursor.execute("SELECT question_id, correct_option FROM questions")
    correct_answers = {row[0]: row[1] for row in cursor.fetchall()}

    # Hitung jumlah jawaban benar
    correct_count = 0
    for question_id, user_answer in user_answers:
        if question_id in correct_answers and user_answer == correct_answers[question_id]:
            correct_count += 1

    # Hitung skor
    score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    # Tampilkan hasil
    st.subheader("Hasil Ujian Anda")
    st.write(f"Jumlah soal: {total_questions}")
    st.write(f"Jawaban benar: {correct_count}")
    st.write(f"Skor: {score:.2f}%")

    # Simpan hasil ke tabel exam
    date_taken = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(''' 
        INSERT INTO exam (user_id, score, date_taken)
        VALUES (?, ?, ?)
    ''', (user_id, score, date_taken))
    conn.commit()

    # Cetak hasil ke PDF
    pdf_file = save_results_as_pdf(user_id, correct_count, total_questions, score)

    # Tampilkan opsi download file PDF
    st.success("Hasil Anda telah disimpan!")
    st.write("Anda juga dapat mengunduh hasil ujian dalam format PDF.")
    with open(pdf_file, "rb") as file:
        st.download_button(
            label="Unduh Hasil Ujian (PDF)",
            data=file,
            file_name=pdf_file.split("/")[-1],
            mime="application/pdf",
        )

    # Tombol Kembali
    if st.button("Kembali ke Menu Utama"):
        st.session_state.page = "home"  # Mengarahkan kembali ke halaman utama

    # Tutup koneksi
    conn.close()

if __name__ == "__main__":
    calculate_and_display_results()
