import streamlit as st
import json

# Setel konfigurasi halaman di awal, sebelum ada kode lain
st.set_page_config(page_title="Chatbot Penyakit Paru", page_icon=":lungs:", layout="centered")

# Muat file JSON yang berisi respons
with open('model/responses.json', 'r', encoding='utf-8') as file:
    responses = json.load(file)

# Fungsi untuk memberikan respons berdasarkan input pengguna
def respond(user_input):
    user_input = user_input.strip().lower()
    response = responses.get(user_input, "Maaf, saya tidak mengerti pertanyaan Anda.")
    return response

# Streamlit UI
def display_chatbot():
    # Tampilan header dengan logo atau ikon
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Chatbot Penyakit Paru</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #808080;'>Tanya jawab mengenai penyakit paru, seperti COVID-19 dan pneumonia.</h3>", unsafe_allow_html=True)
    
    # Menambahkan gambar atau ikon di header (opsional)
    st.image("Lung.png", width=150)
    
    # Input pengguna dengan tampilan lebih cantik
    st.markdown("<h4>Silakan ajukan pertanyaan mengenai penyakit paru:</h4>", unsafe_allow_html=True)
    user_input = st.text_input("Anda: ", "", placeholder="Contoh: Gejala COVID-19")
    
    # Menambahkan respons chatbot dengan tampilan yang lebih menarik
    if user_input:
        response = respond(user_input)
        st.markdown(f"<div style='background-color: #f1f1f1; padding: 10px; border-radius: 5px; color: #333;'><strong>Chatbot: </strong>{response}</div>", unsafe_allow_html=True)
    
    # Menambahkan footer atau keterangan
    st.markdown("<br><br><p style='text-align: center; color: #808080;'>Aplikasi ini dibangun untuk memberikan informasi seputar penyakit paru. Dapatkan informasi lebih lanjut dengan bertanya!</p>", unsafe_allow_html=True)

# Menjalankan aplikasi dengan Streamlit
if __name__ == "__main__":
    display_chatbot()
