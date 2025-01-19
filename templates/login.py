import streamlit as st
import sqlite3

def login():
    st.title("Login")

    # Form input untuk login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            # Koneksi ke database
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                # Simpan informasi login dan role ke session state
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = user[3]  # Mengambil nilai role dari hasil query (kolom ke-4 misalnya)
                st.session_state["page"] = "home"  # Halaman utama setelah login
                st.success(f"Login berhasil! Selamat datang, {username}.")
            else:
                st.error("Username atau password salah!")
            conn.close()
        else:
            st.error("Harap mengisi semua kolom!")

# Jalankan fungsi login
if __name__ == "__main__":
    login()
