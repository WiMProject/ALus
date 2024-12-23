import streamlit as st
from tensorflow.keras.models import load_model  # type: ignore
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array  # type: ignore
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import matplotlib.pyplot as plt
import logging

# Mengatur logging untuk debug
logging.basicConfig(level=logging.DEBUG)

# Fungsi untuk memuat model
@st.cache_resource
def load_mobilenet_model():
    try:
        model = load_model('model/mobilenetv2_final_model.keras')
        return model
    except Exception as e:
        st.error(f"Gagal memuat model: {str(e)}")
        logging.error(f"Error loading model: {str(e)}")
        return None

model = load_mobilenet_model()

# Fungsi untuk membuat plot hasil prediksi
def plot_prediction(image, predictions, categories):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # Menampilkan gambar asli
    ax[0].imshow(image)
    ax[0].axis('off')

    # Menampilkan probabilitas prediksi
    ax[1].barh(categories, predictions, color='skyblue')
    ax[1].set_xlim(0, 1)
    ax[1].set_title("Predicted Class Probabilities")

    st.pyplot(fig)

# Fungsi untuk klasifikasi gambar
def classify_image(image, model):
    try:
        img = image.resize((224, 224))
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)[0]
        categories = ['covid', 'normal', 'pneumonia']
        class_idx = np.argmax(pred)
        label = categories[class_idx]
        confidence = pred[class_idx]

        return label, confidence, pred, categories
    except Exception as e:
        st.error(f"Error during image classification: {str(e)}")
        logging.error(f"Error during image classification: {str(e)}")
        return None, None, None, None

# Fungsi untuk membuat PDF dengan gambar dan hasil prediksi
def create_pdf_with_images(results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    y_position = height - 40

    c.drawString(40, y_position, "Hasil Diagnosa Gambar Paru-Paru")
    y_position -= 20
    c.drawString(40, y_position, "----------------------------------")
    y_position -= 20
    
    for file_name, label, confidence, image, predictions, categories in results:
        c.drawString(40, y_position, f"{file_name}: {label} ({confidence * 100:.2f}%)")
        y_position -= 20

        img = ImageReader(image)
        if y_position < 240:
            c.showPage()
            y_position = height - 40
        c.drawImage(img, 40, y_position - 200, width=200, height=200)
        y_position -= 220
        if y_position < 40:
            c.showPage()
            y_position = height - 40

    c.save()
    buffer.seek(0)
    return buffer

# Fungsi untuk memproses file ZIP
def process_zip_file(zip_file):
    results = []
    try:
        with zipfile.ZipFile(zip_file) as z:
            for file_name in z.namelist():
                if file_name.endswith(('.jpg', '.jpeg', '.png')):
                    with z.open(file_name) as f:
                        image = Image.open(f).convert('RGB')
                        label, confidence, predictions, categories = classify_image(image, model)
                        if label is not None:
                            results.append((file_name, label, confidence, image, predictions, categories))
                else:
                    st.warning(f"File {file_name} diabaikan karena bukan gambar.")
                    logging.warning(f"File {file_name} diabaikan karena bukan gambar.")
    except zipfile.BadZipFile:
        st.error("File ZIP tidak valid atau rusak.")
        logging.error("Bad ZIP file uploaded.")
        return []
    except Exception as e:
        st.error(f"Kesalahan saat memproses file ZIP: {str(e)}")
        logging.error(f"Error processing ZIP file: {str(e)}")
        return []
    
    return results

def display_diagnosis():
    st.title("Diagnosa Penyakit Paru-Paru dengan Mobilenetv2")
    
    option = st.radio("Pilih metode unggah:", ["Unggah beberapa gambar", "Unggah file ZIP"])

    results = []
    if option == "Unggah beberapa gambar":
        uploaded_files = st.file_uploader(
            "Unggah satu atau beberapa gambar",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            st.write("### Hasil Diagnosa")
            if len(uploaded_files) > 20:
                st.warning("Anda hanya dapat mengunggah maksimal 20 file sekaligus.")
                return

            for uploaded_file in uploaded_files:
                try:
                    image = Image.open(uploaded_file).convert('RGB')
                    st.image(image, caption=f"Gambar: {uploaded_file.name}", width=300)

                    label, confidence, predictions, categories = classify_image(image, model)
                    if label is not None:
                        st.write(f"**{uploaded_file.name}**: {label} ({confidence * 100:.2f}%)")
                        plot_prediction(image, predictions, categories)
                        results.append((uploaded_file.name, label, confidence, image, predictions, categories))
                    else:
                        st.write(f"Kesalahan dalam klasifikasi gambar {uploaded_file.name}.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses gambar {uploaded_file.name}: {str(e)}")
                    logging.error(f"Error processing image {uploaded_file.name}: {str(e)}")

    elif option == "Unggah file ZIP":
        zip_file = st.file_uploader("Unggah file ZIP berisi gambar", type=["zip"])
        if zip_file:
            st.write("### Hasil Diagnosa")
            results = process_zip_file(zip_file)
            for file_name, label, confidence, image, predictions, categories in results:
                st.image(image, caption=f"Gambar: {file_name}", width=300)
                st.write(f"**{file_name}**: {label} ({confidence * 100:.2f}%)")
                plot_prediction(image, predictions, categories)

    if results:
        pdf_buffer = create_pdf_with_images(results)
        st.download_button(
            label="Unduh Hasil Diagnosa (PDF)",
            data=pdf_buffer,
            file_name="hasil_diagnosa.pdf",
            mime="application/pdf"
        )
