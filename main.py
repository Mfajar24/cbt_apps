import streamlit as st
from templates.home import home
from templates.form import form
from templates.kisi_kisi import kisi_kisi
from templates.exam import exam
from templates.edit_question import edit_question_page
from templates.manage_questions import manage_questions
from templates.upload_questions import upload_questions
from templates.result import calculate_and_display_results
from templates.login import login
from templates.register import register

def main():
    # Inisialisasi session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.username = None
        st.session_state.role = None  # Pastikan peran disetel di session_state

    # Daftar halaman
    pages = {
        "home": home,
        "form": form,
        "kisi_kisi": kisi_kisi,
        "exam": exam,
        "manage_questions": manage_questions,
        "upload_questions": upload_questions,
        "result": calculate_and_display_results,
        "login": login,
        "register": register,
        "edit_question": edit_question_page,
    }

    # Logika untuk pengguna yang belum login
    if not st.session_state.logged_in:
        st.sidebar.title("Navigasi")
        page = st.sidebar.radio("Pilih Halaman", ["Login", "Daftar Akun Baru"])
        st.session_state.page = "login" if page == "Login" else "register"

    # Menjaga hanya admin yang bisa mengakses halaman manage_questions
    if st.session_state.logged_in and st.session_state.page == "manage_questions":
        if st.session_state.get("role") != "admin":
            st.error("Hanya admin yang dapat mengakses halaman ini!")
            st.session_state.page = "home"  # Redirect ke halaman home

    # Panggil halaman berdasarkan state
    if st.session_state.page in pages:
        pages[st.session_state.page]()
    else:
        st.error("Halaman tidak ditemukan!")

    # Tambahkan tombol logout jika sudah login
    if st.session_state.logged_in:
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.page = "login"
            st.success("Berhasil logout.")

if __name__ == "__main__":
    main()
