import streamlit as st

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

def calculate_cf(user_symptoms):
    disease_cf = {}
    
    for disease, rule in rules.items():
        matching_symptoms = set(user_symptoms).intersection(set(rule["symptoms"]))
        disease_cf[disease] = rule["cf"] * (len(matching_symptoms) / len(rule["symptoms"])) if matching_symptoms else 0
    
    return disease_cf

def determine_diagnosis(user_symptoms):
    cf_results = calculate_cf(user_symptoms)
    
    if not cf_results or all(cf == 0 for cf in cf_results.values()):
        return None, 0.0  # Tidak ada diagnosa

    diagnosis = max(cf_results, key=cf_results.get)
    certainty = cf_results[diagnosis]
    
    return diagnosis, certainty

def start_quiz():
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
            st.warning("Saya tidak dapat mengenali gejala tersebut. Silakan konsultasikan dengan dokter Anda.")

        if st.button("Mulai Ulang Percakapan"):
            st.session_state.finished = False
            st.session_state.current_question_index = 0
            st.session_state.user_symptoms = []
            st.experimental_rerun()  # Restart the app to reset everything

    else:
        question = st.session_state.questions[st.session_state.current_question_index]
        st.subheader(f"Pertanyaan {st.session_state.current_question_index + 1}:")
        st.write(question)

        col1, col2 = st.columns(2)
        
        if col1.button("Ya"):
            st.session_state.user_symptoms.append(question.split()[2].lower())
            st.session_state.current_question_index += 1
            st.experimental_rerun()  # Refresh the app to show the next question
            
        if col2.button("Tidak"):
            st.session_state.current_question_index += 1
            st.experimental_rerun()  # Refresh the app to show the next question
        
        if st.session_state.current_question_index >= len(st.session_state.questions):
            st.session_state.finished = True

# Menjalankan aplikasi Streamlit
def display_chatbot():
    st.title("Konsultasi Gejala Penyakit Paru")
    st.write("Selamat datang! Mari kita cari tahu gejala yang Anda alami.")

    if st.button("Mulai Percakapan"):
        start_quiz()
    else:
        st.write("Tekan tombol di atas untuk mulai.")

# Menjalankan fungsi utama
if __name__ == "__main__":
    display_chatbot()
