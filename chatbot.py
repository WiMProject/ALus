import json
import numpy as np
import tensorflow as tf
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Muat model yang telah dilatih dan tokenizer
model = load_model('model/chatbot_ai_lstm_model.h5')

with open('model/chatbot_tokenizer.json', 'r') as file:
    tokenizer_data = json.load(file)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_data)

# Define MAX_LEN (panjang input yang diinginkan)
MAX_LEN = 20

# Encoder-Decoder model (diambil dari model utama)
encoder_inputs = model.input[0]  # Input untuk encoder
encoder_outputs, state_h, state_c = model.layers[2].output  # Output dan state dari LSTM encoder
encoder_states = [state_h, state_c]

decoder_inputs = model.input[1]  # Input untuk decoder
decoder_lstm = model.layers[4]  # LSTM decoder
decoder_dense = model.layers[5]  # Dense layer output dari decoder

# Membuat model encoder dan decoder terpisah untuk inference
encoder_model = tf.keras.models.Model(encoder_inputs, encoder_states)

decoder_state_input_h = tf.keras.Input(shape=(256,))
decoder_state_input_c = tf.keras.Input(shape=(256,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

decoder_lstm_outputs, state_h, state_c = decoder_lstm(
    decoder_inputs, initial_state=decoder_states_inputs
)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_lstm_outputs)

decoder_model = tf.keras.models.Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs] + decoder_states
)

# Encode dan decode fungsi untuk chatbot
def respond(input_text):
    # Preprocessing input pengguna
    input_seq = pad_sequences(tokenizer.texts_to_sequences([input_text]), maxlen=MAX_LEN, padding='post')

    # Inference dengan encoder model
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
