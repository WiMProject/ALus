import streamlit as st
import json

# Muat file JSON yang berisi respons
with open('model/responses.json', 'r', encoding='utf-8') as file:
    responses = json.load(file)

# Fungsi untuk memberikan respons berdasarkan input pengguna
def respond(user_input):
    user_input = user_input.strip().lower()
    response = responses.get(user_input, "Maaf, saya tidak mengerti pertanyaan Anda.")
    return response

def display_chatbot():
    st.title("Chatbot Penyakit Paru")
    st.subheader("Tanya jawab mengenai penyakit paru, seperti COVID-19 dan pneumonia.")
    
    user_input = st.text_input("Anda: ", "")
    
    if user_input:
        response = respond(user_input)
        st.write(f"Chatbot: {response}")
