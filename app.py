import streamlit as st

# Menetapkan konfigurasi halaman agar tidak ada sidebar
st.set_page_config(page_title="ALus", page_icon=":lungs:", layout="wide", initial_sidebar_state="collapsed")

from home import display_home
from diagnose import display_diagnosis
from about import display_about
from chatbot import display_chatbot

# Navbar dengan radio button di bagian atas
menu = ["Beranda", "Konsultasi", "Diagnosa", "Tentang"]
choice = st.radio("Navigasi", menu, horizontal=True)

# Tampilkan halaman sesuai pilihan dari radio button
if choice == "Beranda":
    display_home()

elif choice == "Konsultasi":
    display_chatbot()

elif choice == "Diagnosa":
    display_diagnosis()

elif choice == "Tentang":
    display_about()
