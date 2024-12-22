import streamlit as st

# Fungsi untuk menangani percakapan chatbot
def chatbot_response(user_input):
    # Daftar respons berdasarkan gejala
    responses = {
        "batuk": "Batuk bisa menjadi gejala awal dari berbagai penyakit, termasuk flu, pneumonia, atau COVID-19. Jika batuk disertai demam atau sesak napas, segera periksa ke dokter.",
        "demam": "Demam bisa menjadi gejala infeksi seperti flu atau COVID-19. Jika disertai dengan sesak napas atau nyeri dada, segera lakukan pemeriksaan lebih lanjut.",
        "sesak napas": "Sesak napas adalah gejala serius yang perlu ditangani segera. Ini bisa menunjukkan pneumonia atau infeksi saluran pernapasan lain, termasuk COVID-19. Pastikan untuk segera mendapat perhatian medis.",
        "nyeri dada": "Nyeri dada bisa disebabkan oleh berbagai kondisi, termasuk masalah jantung atau pneumonia. Jika nyeri dada disertai dengan sesak napas, segera hubungi dokter.",
        "lelah": "Kelelahan bisa disebabkan oleh banyak hal, termasuk infeksi pernapasan seperti COVID-19 atau pneumonia. Jika gejala berlanjut, periksa lebih lanjut ke dokter.",
        "mual": "Mual bisa disebabkan oleh banyak faktor, namun jika disertai gejala pernapasan, bisa jadi itu merupakan tanda infeksi paru-paru.",
        "pusing": "Pusing bisa menjadi tanda masalah kesehatan lain yang perlu diperiksa lebih lanjut. Jika disertai sesak napas atau batuk, periksa kondisi paru-paru Anda.",
        "hilang indra perasa atau penciuman": "Hilangnya indra perasa atau penciuman sering dikaitkan dengan infeksi COVID-19. Jika Anda memiliki gejala ini, pastikan untuk melakukan tes COVID-19.",
        "normal": "Gejala Anda tidak menunjukkan tanda-tanda penyakit serius. Namun, tetap perhatikan kesehatan Anda dan lakukan pemeriksaan rutin jika diperlukan."
    }
    
    # Mengembalikan respons berdasarkan input pengguna
    return responses.get(user_input.lower(), "Saya tidak dapat mengenali gejala tersebut. Harap coba sebutkan gejala lain atau konsultasikan dengan dokter.")

# Fungsi untuk tampilan chatbot
def display_chatbot():
    st.title("Konsultasi Gejala Penyakit Paru")
    st.write("Tanyakan gejala yang Anda alami dan saya akan memberikan informasi terkait gejala tersebut.")

    # List percakapan
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Menangani input dan output chatbot
    user_input = st.text_input("Gejala Anda:", "")

    if user_input:
        # Menambahkan pesan pengguna ke sesi
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Mendapatkan respons dari chatbot
        response = chatbot_response(user_input)
        st.session_state.messages.append({"role": "bot", "content": response})

    # Menampilkan percakapan
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**Anda**: {message['content']}")
        else:
            st.markdown(f"**Dokter**: {message['content']}")

    # Memberikan tombol untuk restart percakapan
    if st.button("Mulai Ulang Percakapan"):
        st.session_state.messages = []
