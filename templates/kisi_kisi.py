import streamlit as st

def kisi_kisi():
    st.title("Kisi-Kisi Ujian")

    # Contoh kisi-kisi
    kisi_kisi_data = [
        {"topik": "Matematika", "deskripsi": "Integrasi dan Turunan"},
        {"topik": "Fisika", "deskripsi": "Hukum Newton dan Dinamika"},
        {"topik": "Kimia", "deskripsi": "Ikatan Kimia dan Stoikiometri"},
    ]

    for kisi in kisi_kisi_data:
        st.subheader(kisi["topik"])
        st.write(kisi["deskripsi"])

    # Tombol kembali ke menu utama
    if st.button("Kembali ke Menu Utama"):
        st.session_state.page = "home"
