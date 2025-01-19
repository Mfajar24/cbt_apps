import streamlit as st
import sqlite3

def register():
    st.title("Daftar Akun Baru")

    # Form input untuk registrasi
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Konfirmasi Password", type="password")
    role = st.selectbox("Pilih Role", ["user", "admin"])  # Menambahkan pemilihan role

    if st.button("Daftar"):
        if username and password and confirm_password:
            if password == confirm_password:
                # Koneksi ke database
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    st.error("Username sudah terdaftar!")
                else:
                    cursor.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)", (username, password, role))
                    conn.commit()
                    st.success("Akun berhasil dibuat! Silakan login.")
                    st.session_state.page = "login"  # Arahkan ke halaman login
                conn.close()
            else:
                st.error("Password dan konfirmasi password tidak cocok!")
        else:
            st.error("Harap mengisi semua kolom!")
