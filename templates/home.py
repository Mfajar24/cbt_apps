import streamlit as st

def home():
    # Pastikan hanya pengguna yang login yang dapat mengakses halaman ini
    if not st.session_state.logged_in:
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"  # Redirect ke halaman login
        return

    st.title("Selamat Datang di CBT App")

    # Menambahkan background gambar
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.wallpapersden.com/image/download/abstract-shapes-2021-minimalist_bG1lZm6UmZqaraWkpJRmbmdmrWZlbWY.jpg");
            background-size: cover;
            background-position: center;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Fungsi navigasi untuk mengubah halaman yang aktif
    def navigate_to(page):
        st.session_state.page = page

    # Kolom untuk tombol pengaturan (di kiri) dan tombol aksi (di kanan)
    st.header("Pilih Aksi:")
    
    # Membuat layout kolom untuk tombol-tombol card yang berjejer rapi
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⚙ Pengaturan"):
            navigate_to("manage_questions")  # Navigasi ke halaman pengaturan

    with col2:
        if st.button("Mulai Ujian"):
            navigate_to("form")  # Navigasi ke halaman ujian

    with col3:
        if st.button("Lihat Kisi-Kisi"):
            navigate_to("kisi_kisi")  # Navigasi ke halaman kisi-kisi
