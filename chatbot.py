import streamlit as st

class Disease:
    def __init__(self, name, cf):
        self.name = name
        self.cf = cf

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

# Fungsi untuk menghitung certainty factor dan akurasi
def calculate_cf(user_symptoms):
    disease_cf = {}
    
    for disease, rule in rules.items():
        matching_symptoms = set(user_symptoms).intersection(set(rule["symptoms"]))
        if matching_symptoms:
            # Menghitung CF berdasarkan jumlah gejala yang cocok
            disease_cf[disease] = rule["cf"] * (len(matching_symptoms) / len(rule["symptoms"]))
    
    return disease_cf

# Fungsi untuk memberikan respons dari chatbot
def chatbot_response(user_input):
    user_symptoms = user_input.lower().split(",")  # Memisahkan input gejala
    user_symptoms = [symptom.strip() for symptom in user_symptoms if symptom.strip() != ""]

    # Menghitung certainty factor
    cf_results = calculate_cf(user_symptoms)

    if not cf_results:
        return ("Saya tidak dapat mengenali gejala tersebut. "
                "Harap coba sebutkan gejala lain atau konsultasikan dengan dokter.")

    # Mengembalikan diagnosis dengan certainty factor tertinggi
    diagnosis = max(cf_results, key=cf_results.get)
    certainty = cf_results[diagnosis]

    response = f"Gejala Anda mungkin menunjukkan **{diagnosis}** dengan tingkat kepastian **{certainty:.2f}**.\n\n"
    
    if diagnosis == "TBC":
        response += ("TBC (Tuberkulosis) adalah infeksi serius yang menyerang paru-paru. "
                     "Segera lakukan pemeriksaan lebih lanjut dan konsultasikan dengan dokter.")
    elif diagnosis == "COVID-19":
        response += ("COVID-19 adalah penyakit yang disebabkan oleh virus SARS-CoV-2. "
                     "Segera lakukan tes COVID-19.")
    elif diagnosis == "Flu":
        response += ("Flu adalah infeksi virus yang biasanya sembuh sendiri dalam beberapa hari. "
                     "Pastikan Anda beristirahat cukup.")
    # Tambahan untuk diagnosis lainnya dapat ditambahkan di sini...

    return response

# Fungsi untuk tampilan chatbot
def display_chatbot():
    st.title("Konsultasi Gejala Penyakit Paru")
    st.write("Tanyakan gejala yang Anda alami, pisahkan dengan koma jika lebih dari satu.")

    # List percakapan
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Menangani input dan output chatbot
    user_input = st.text_input("Gejala Anda (pisahkan dengan koma):", "")

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

# Menjalankan aplikasi Streamlit
if __name__ == "__main__":
    display_chatbot()
