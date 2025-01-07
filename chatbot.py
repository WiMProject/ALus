import json
import numpy as np
import tensorflow as tf
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Muat model yang telah dilatih dan tokenizer
model = load_model('/path/to/your/chatbot_ai_lstm_model.h5')

with open('/path/to/your/chatbot_tokenizer.json', 'r') as file:
    tokenizer_data = json.load(file)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_data)

# Define MAX_LEN (panjang input yang diinginkan)
MAX_LEN = 20

# Encode dan decode fungsi untuk chatbot
def respond(input_text):
    # Preprocessing input pengguna
    input_seq = pad_sequences(tokenizer.texts_to_sequences([input_text]), maxlen=MAX_LEN, padding='post')

    # Model inference
    encoder_model = model.get_layer('encoder_model')
    decoder_model = model.get_layer('decoder_model')

    states_value = encoder_model.predict(input_seq)

    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = tokenizer.word_index['startseq']

    stop_condition = False
    decoded_sentence = ''

    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_word = tokenizer.index_word.get(sampled_token_index, '')

        decoded_sentence += ' ' + sampled_word

        if sampled_word == 'endseq' or len(decoded_sentence.split()) > MAX_LEN:
            stop_condition = True

        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index
        states_value = [h, c]

    return decoded_sentence.replace('endseq', '').strip()

# Streamlit UI
st.title("Chatbot Penyakit Paru")
st.subheader("Tanya jawab mengenai penyakit paru, seperti COVID-19 dan pneumonia.")

user_input = st.text_input("Anda: ", "")

if user_input:
    response = respond(user_input)
    st.write("Chatbot: ", response)

# Menjalankan fungsi utama
if __name__ == "__main__":
    display_chatbot()
