import streamlit as st
import random
import re

# Aturan gejala dan penyakit
rules = {
    "Flu": {
        "symptoms": ["batuk", "demam", "lelah", "nyeri otot", "pegal-pegal"],
        "cf": 0.5,
        "description": "Flu adalah infeksi virus yang menyerang sistem pernapasan."
    },
    "COVID-19": {
        "symptoms": ["batuk", "demam", "hilang indra perasa atau penciuman", "sesak napas"],
        "cf": 0.7,
        "description": "COVID-19 adalah penyakit yang disebabkan oleh virus SARS-CoV-2."
    },
    "Pneumonia": {
        "symptoms": ["batuk", "sesak napas", "nyeri dada", "demam tinggi"],
        "cf": 0.8,
        "description": "Pneumonia adalah infeksi yang membuat kantung udara di dalam paru-paru meradang."
    },
    "Infeksi Saluran Pernapasan": {
        "symptoms": ["batuk", "sesak napas", "lelah", "demam"],
        "cf": 0.4,
        "description": "Infeksi saluran pernapasan bisa disebabkan oleh virus atau bakteri."
    },
    "TBC": {
        "symptoms": ["batuk", "sesak napas", "demam", "berat badan turun", "keringat malam"],
        "cf": 0.9,
        "description": "TBC adalah infeksi serius yang umumnya menyerang paru-paru dan disebabkan oleh bakteri."
    }
}

# Variasi respons untuk masukan keluhan
responses = {
    "batuk": [
        "Batuk bisa disebabkan oleh flu, alergi, atau infeksi pernapasan lainnya.",
        "Selama berapa lama Anda mengalami batuk ini?",
    ],
    "demam": [
        "Demam biasanya menandakan adanya infeksi dalam tubuh.",
        "Apakah Anda bisa memberikan angka suhu tubuh tertinggi yang tercatat?",
    ],
    "lelah": [
        "Kelelahan kronis bisa disebabkan oleh beberapa alasan, termasuk infeksi.",
        "Istirahat yang cukup adalah cara terbaik untuk mengatasi kelelahan.",
    ],
    "sesak napas": [
        "Sesak napas harus ditangani dengan serius dan bisa berhubungan dengan banyak penyakit.",
        "Apakah Anda mengalami sesak napas yang parah dan cepat?",
    ],
    "nyeri dada": [
        "Nyeri dada bisa berhubungan dengan beberapa kondisi medis.",
        "Segera hubungi dokter jika Anda mengalami nyeri dada yang parah.",
    ],
    "hilang indra perasa atau penciuman": [
        "Hilangnya indra penciuman sering dikaitkan dengan COVID-19.",
        "Melakukan tes COVID-19 adalah langkah bijak."
    ]
}

def analyze_symptoms(user_input):
    """Analisis input pengguna dan cari gejala menggunakan regex"""
    user_input = user_input.lower()
    detected_symptoms = re.findall(r'\b\w+\b', user_input)
    return detected_symptoms

def determine_disease(detected_symptoms):
    """Menentukan penyakit berdasarkan gejala yang cocok"""
    cf_results = {disease: 0 for disease in rules.keys()}
    
    for disease, rule in rules.items():
        matching_symptoms = set(detected_symptoms).intersection(set(rule["symptoms"]))
        if matching_symptoms:
            # Hitung skor basis CF dikalikan dengan jumlah gejala yang cocok
            cf = rule["cf"] * (len(matching_symptoms) / len(rule["symptoms"]))
            cf_results[disease] = cf

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

            # Diagnosa akan dilakukan jika 3 gejala atau lebih terdeteksi
            if len(detected_symptoms) >= 3:
                diagnosis_cf = determine_disease(detected_symptoms)
                if diagnosis_cf:
                    # Tentukan penyakit berdasarkan skor tertinggi
                    diagnosis = max(diagnosis_cf, key=diagnosis_cf.get)
                    final_certainty = diagnosis_cf[diagnosis] * 100  # menghitung dalam persen
                    result_message = f"💡 Gejala Anda mungkin menunjukkan **{diagnosis}** dengan tingkat kepastian **{final_certainty:.2f}%**."
                    st.success(result_message)
                    st.session_state.conversation.append(f"Bot: {result_message}")
                    st.write(f"**Deskripsi:** {rules[diagnosis]['description']}")

                else:
                    warning_message = "⚠️ Saya tidak dapat mengenali gejala tersebut."
                    st.warning(warning_message)
                    st.session_state.conversation.append(f"Bot: {warning_message}")
            else:
                st.write("😕 Anda perlu menyebutkan setidaknya 3 gejala untuk memberikan diagnosis yang akurat.")
                st.session_state.conversation.append("Bot: Anda perlu menyebutkan setidaknya 3 gejala untuk memberikan diagnosis yang akurat.")

            # Memberikan respons berdasarkan gejala yang terdeteksi
            for symptom in detected_symptoms:
                if symptom in responses:
                    response = random.choice(responses[symptom])
                    st.session_state.conversation.append(f"Bot: {response}")
                    st.write(response)

        else:
            st.error("❗ Tolong masukkan keluhan Anda.")

    st.write("---")
    st.write("### Riwayat Percakapan:")
    
    for message in st.session_state.conversation:
        st.write(message)

# Menjalankan fungsi utama
if __name__ == "__main__":
    display_chatbot()
