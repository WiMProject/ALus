import streamlit as st
from tensorflow.keras.models import load_model # type: ignore
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array # type: ignore
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

# Fungsi untuk memuat model
@st.cache_resource
def load_mobilenet_model():
    model = load_model('model/mobilenetv2_final_model.keras')
    return model

model = load_mobilenet_model()

# Fungsi untuk klasifikasi gambar
def classify_image(image, model):
    img = image.resize((224, 224))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    class_idx = np.argmax(pred, axis=1)[0]
    categories = ['covid', 'normal', 'pneumonia']
    label = categories[class_idx]
    confidence = np.max(pred)
    return label, confidence

# Fungsi untuk membuat PDF dengan gambar
def create_pdf_with_images(results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    y_position = height - 40

    c.drawString(40, y_position, "Hasil Klasifikasi Gambar Paru-Paru")
    y_position -= 20
    c.drawString(40, y_position, "----------------------------------")
    y_position -= 20
    
    for file_name, label, confidence, image in results:
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
    with zipfile.ZipFile(zip_file) as z:
        for file_name in z.namelist():
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                with z.open(file_name) as f:
                    image = Image.open(f).convert('RGB')
                    label, confidence = classify_image(image, model)
                    results.append((file_name, label, confidence, image))
    return results

def display_diagnosis():
    st.title("Klasifikasi Gambar Paru-Paru")
    option = st.radio("Pilih metode unggah:", ["Unggah beberapa gambar", "Unggah file ZIP"])

    results = []
    if option == "Unggah beberapa gambar":
        uploaded_files = st.file_uploader(
            "Unggah satu atau beberapa gambar",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            st.write("### Hasil Klasifikasi")
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file).convert('RGB')
                st.image(image, caption=f"Gambar: {uploaded_file.name}", use_container_width=True)

                label, confidence = classify_image(image, model)
                st.write(f"**{uploaded_file.name}**: {label} ({confidence * 100:.2f}%)")
                results.append((uploaded_file.name, label, confidence, image))

    elif option == "Unggah file ZIP":
        zip_file = st.file_uploader("Unggah file ZIP berisi gambar", type=["zip"])
        if zip_file:
            st.write("### Hasil Klasifikasi")
            results = process_zip_file(zip_file)
            for file_name, label, confidence, image in results:
                st.image(image, caption=f"Gambar: {file_name}", use_container_width=True)
                st.write(f"**{file_name}**: {label} ({confidence * 100:.2f}%)")

    if results:
        pdf_buffer = create_pdf_with_images(results)
        st.download_button(
            label="Unduh Hasil Klasifikasi (PDF)",
            data=pdf_buffer,
            file_name="hasil_klasifikasi.pdf",
            mime="application/pdf"
        )
