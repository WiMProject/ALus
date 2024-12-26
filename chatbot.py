import streamlit as st

# Aturan gejala dan certainty factors
rules = {
    "Flu": {
        "symptoms": ["batuk", "demam", "lelah"],
        "cf": 0.7
    },
    "COVID-19": {
        "symptoms": ["batuk", "demam", "hilang indra perasa atau penciuman"],
        "cf": 0.9
    },
    "Pneumonia": {
        "symptoms": ["batuk", "sesak napas", "nyeri dada"],
        "cf": 0.8
    },
    "Infeksi Saluran Pernapasan": {
        "symptoms": ["batuk", "sesak napas", "lelah"],
        "cf": 0.6
    },
    "TBC": {
        "symptoms": ["batuk", "sesak napas", "demam", "berturut-turut"],
        "cf": 0.85
    }
}

# Menghitung CF dan akurasi
def calculate_cf(user_symptoms):
    disease_cf = {}
    
    for disease, rule in rules.items():
        matching_symptoms = set(user_symptoms).intersection(set(rule["symptoms"]))
        if matching_symptoms:
            disease_cf[disease] = rule["cf"] * (len(matching_symptoms) / len(rule["symptoms"]))
    
    return disease_cf

# Fungsi untuk memberikan respons dari chatbot
def determine_diagnosis(user_symptoms):
    cf_results = calculate_cf(user_symptoms)
    
    if not cf_results:
        return None, None

    # Mengembalikan diagnosis dengan certainty factor tertinggi
    diagnosis = max(cf_results, key=cf_results.get)
    certainty = cf_results[diagnosis]
    
    return diagnosis, certainty

# Fungsi untuk memulai kuis
def start_quiz():
    # Menggunakan session state untuk menyimpan pertanyaan
    if "questions" not in st.session_state:
        st.session_state.questions = [
            "Apakah Anda mengalami batuk?",
            "Apakah Anda mengalami demam?",
            "Apakah Anda merasa lelah?",
            "Apakah Anda mengalami sesak napas?",
            "Apakah Anda mengalami nyeri dada?",
            "Apakah Anda kehilangan indra penciuman atau perasa?",
        ]
        st.session_state.current_question_index = 0
        st.session_state.user_symptoms = []
        st.session_state.finished = False

    if st.session_state.finished:
        diagnosis, certainty = determine_diagnosis(st.session_state.user_symptoms)
        if diagnosis:
            st.success(f"Gejala Anda mungkin menunjukkan **{diagnosis}** dengan tingkat kepastian **{certainty:.2f}**.")
        else:
            st.warning("Saya tidak dapat mengenali gejala tersebut.")

        if st.button("Mulai Ulang Percakapan"):
            st.session_state.finished = False
            st.session_state.current_question_index = 0
            st.session_state.user_symptoms = []
            st.session_state.questions = [
                "Apakah Anda mengalami batuk?",
                "Apakah Anda mengalami demam?",
                "Apakah Anda merasa lelah?",
                "Apakah Anda mengalami sesak napas?",
                "Apakah Anda mengalami nyeri dada?",
                "Apakah Anda kehilangan indra penciuman atau perasa?",
            ]
        
    else:
        question = st.session_state.questions[st.session_state.current_question_index]
        st.write(question)
        col1, col2 = st.columns(2)
        
        if col1.button("Ya"):
            st.session_state.user_symptoms.append(question.split()[2].lower())  # Menambahkan gejala yang sesuai
            st.session_state.current_question_index += 1
        if col2.button("Tidak"):
            st.session_state.current_question_index += 1
        
        if st.session_state.current_question_index >= len(st.session_state.questions):
            st.session_state.finished = True
            
def display_chatbot():
    st.title("Konsultasi Gejala Penyakit Paru")
    st.write("Tanyakan gejala yang Anda alami, jawab pertanyaan di bawah ini.")

    if st.button("Mulai Percakapan"):
        start_quiz()
    else:
        st.write("Tekan tombol di atas untuk mulai.")

# Menjalankan aplikasi Streamlit
if __name__ == "__main__":
    display_chatbot()
