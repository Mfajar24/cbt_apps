import streamlit as st
from templates.home import home
from templates.form import form
from templates.kisi_kisi import kisi_kisi
from templates.exam import exam
from templates.manage_questions import manage_questions
from templates.upload_questions import upload_questions
from templates.result import calculate_and_display_results  # Pastikan result.py sudah ada

def main():
    # Inisialisasi state halaman jika belum ada
    if "page" not in st.session_state:
        st.session_state.page = "home"  # Set halaman default ke 'home'

    # Routing halaman berdasarkan state 'page'
    pages = {
        "home": home,
        "form": form,
        "kisi_kisi": kisi_kisi,
        "exam": exam,
        "manage_questions": manage_questions,
        "upload_questions": upload_questions,
        "result": calculate_and_display_results,
    }

    # Panggil fungsi berdasarkan halaman saat ini
    if st.session_state.page in pages:
        pages[st.session_state.page]()  # Panggil fungsi sesuai halaman
    else:
        st.error("Halaman tidak ditemukan!")  # Jika halaman tidak valid

    # Tambahkan tombol navigasi kembali ke halaman utama jika bukan di 'home'
    if st.session_state.page != "home":
        if st.button("Kembali ke Home"):
            st.session_state.page = "home"  # Atur halaman menjadi 'home'

if __name__ == "__main__":
    main()
