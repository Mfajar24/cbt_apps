import streamlit as st

def home():
    st.title("Selamat Datang di CBT App")
    
    # Fungsi navigasi ke halaman lain
    def navigate_to(page):
        st.session_state.page = page

    # Tombol Pengaturan di sebelah kiri atas
    col1, col2 = st.columns([1, 9])  # Membagi layout: kolom pertama lebih kecil
    with col1:
        if st.button("⚙ Pengaturan"):
            navigate_to("manage_questions")

    st.header("Pilih Aksi:")
    if st.button("Mulai Ujian"):
        navigate_to("form")
    if st.button("Lihat Kisi-Kisi"):
        navigate_to("kisi_kisi")
