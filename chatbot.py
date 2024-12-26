import streamlit as st
import random
import re

# Aturan gejala dan penyakit
rules = {
    "Flu": {
        "symptoms": ["batuk", "demam", "lelah"],
        "cf": 0.9
    },
    "COVID-19": {
        "symptoms": ["batuk", "demam", "hilang indra perasa atau penciuman"],
        "cf": 0.9
    },
    "Pneumonia": {
        "symptoms": ["batuk", "sesak napas", "nyeri dada"],
        "cf": 0.9
    },
    "Infeksi Saluran Pernapasan": {
        "symptoms": ["batuk", "sesak napas", "lelah"],
        "cf": 0.9
    },
    "TBC": {
        "symptoms": ["batuk", "sesak napas", "demam", "berat badan turun"],
        "cf": 0.9
    }
}

# Variasi respons untuk masukan keluhan
responses = {
    "batuk": [
        "Batuk bisa disebabkan oleh flu, alergi, atau infeksi pernapasan lainnya.",
        "Selama berapa lama Anda mengalami batuk ini?",
        "Batuk kronis membutuhkan perhatian medis segera."
    ],
    "demam": [
        "Demam biasanya menandakan adanya infeksi dalam tubuh.",
        "Apakah Anda bisa memberikan angka suhu tubuh tertinggi yang tercatat?",
    ],
    "lelah": [
        "Kelelahan kronis bisa disebabkan oleh beberapa alasan, termasuk infeksi.",
        "Sering istirahat dan tidur cukup sangat dianjurkan.",
    ],
    "sesak napas": [
        "Sesak napas adalah gejala medis yang serius.",
        "Apakah Anda mengalami tekanan di dada bersamaan dengan sesak napas?",
    ],
    "nyeri dada": [
        "Nyeri dada bisa berhubungan dengan masalah jantung atau paru-paru.",
        "Penting untuk tidak mengabaikan gejala ini, segera periksa ke dokter.",
    ],
    "hilang indra perasa atau penciuman": [
        "Hilangnya indra penciuman sering dikaitkan dengan COVID-19.",
        "Melakukan tes COVID-19 adalah langkah bijak."
    ]
}

def analyze_symptoms(user_input):
    """Analisis input pengguna dan cari gejala menggunakan regex"""
    user_input = user_input.lower()
    detected_symptoms = []

    for symptom in responses.keys():
        if re.search(r'\b' + symptom + r'\b', user_input):
            detected_symptoms.append(symptom)

    return detected_symptoms

def determine_disease(detected_symptoms):
    """Menentukan penyakit berdasarkan gejala yang cocok"""
    cf_results = {}
    
    for disease, rule in rules.items():
        matching_symptoms = set(detected_symptoms).intersection(set(rule["symptoms"]))
        if matching_symptoms:
            cf_results[disease] = rule["cf"] * (len(matching_symptoms) / len(rule["symptoms"]))

    return cf_results

def display_chatbot():
    st.title("Chatbot Kesehatan")
    st.write("🩺 **Selamat datang di Chatbot Kesehatan!**")
    st.write("Silakan ceritakan keluhan Anda dan saya akan membantu memberikan informasi.")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    user_input = st.text_area("Keluhan Anda:", height=100)

    if st.button("Kirim"):
        if user_input:
            detected_symptoms = analyze_symptoms(user_input)
            st.session_state.conversation.append(f"Anda: {user_input}")

            if detected_symptoms:
                diagnosis_cf = determine_disease(detected_symptoms)
                for symptom in detected_symptoms:
                    response = random.choice(responses[symptom])
                    st.session_state.conversation.append(f"Bot: {response}")
                    st.write(response)

                if diagnosis_cf:
                    diagnosis = max(diagnosis_cf, key=diagnosis_cf.get)
                    certainty = diagnosis_cf[diagnosis]
                    result_message = f"💡 Gejala Anda mungkin menunjukkan **{diagnosis}** dengan tingkat kepastian **{certainty:.2f}**."
                    st.success(result_message)
                    st.session_state.conversation.append(f"Bot: {result_message}")

                else:
                    warning_message = "⚠️ Saya tidak dapat mengenali gejala tersebut."
                    st.warning(warning_message)
                    st.session_state.conversation.append(f"Bot: {warning_message}")

            else:
                error_message = "😕 Maaf, saya tidak dapat menemukan gejala yang relevan dalam keluhan Anda."
                st.write(error_message)
                st.session_state.conversation.append(f"Bot: {error_message}")
        else:
            st.error("❗ Tolong masukkan keluhan Anda.")

    st.write("---")
    st.write("### Riwayat Percakapan:")
    
    for message in st.session_state.conversation:
        st.write(message)

# Menjalankan fungsi utama
if __name__ == "__main__":
    display_chatbot()
