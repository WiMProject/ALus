import streamlit as st
from tensorflow.keras.models import load_model  # type: ignore
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array  # type: ignore
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import io
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from datetime import datetime

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
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Menampilkan gambar asli
    ax[0].imshow(image)
    ax[0].axis('off')
    ax[0].set_title("Input X-Ray Image", fontsize=14, weight='bold')

    # Menampilkan probabilitas prediksi dengan plot horizontal
    sns.barplot(x=predictions, y=categories, ax=ax[1], palette='coolwarm')
    ax[1].set_xlim(0, 1)
    ax[1].set_xlabel("Probability", fontsize=12)
    ax[1].set_title("Predicted Class Probabilities", fontsize=14, weight='bold')

    plt.tight_layout()
    st.pyplot(fig)

# Fungsi untuk klasifikasi gambar
def classify_image(image, model):
    try:
        img = image.resize((224, 224))
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)[0]
        categories = ['COVID-19', 'Normal', 'Pneumonia']
        class_idx = np.argmax(pred)
        label = categories[class_idx]
        confidence = pred[class_idx]

        return label, confidence, pred, categories
    except Exception as e:
        st.error(f"Error during image classification: {str(e)}")
        logging.error(f"Error during image classification: {str(e)}")
        return None, None, None, None

# Fungsi untuk menambahkan deskripsi penyakit dan tips kesehatan pada PDF
def add_disease_description_and_tips(c, label, y_position):
    descriptions = {
        "COVID-19": "COVID-19 adalah penyakit yang disebabkan oleh virus SARS-CoV-2, yang dapat menyebabkan infeksi pernapasan akut.",
        "Pneumonia": "Pneumonia adalah infeksi paru-paru yang menyebabkan peradangan pada kantung udara, yang dapat terisi cairan atau nanah.",
        "Normal": "Paru-paru Anda dalam kondisi normal. Tetap jaga kesehatan paru-paru Anda dengan menghindari merokok, menjaga kualitas udara, dan rutin berolahraga."
    }

    tips = {
        "COVID-19": "Kenapa COVID-19? Virus SARS-CoV-2 dapat menyebar melalui droplet dan kontak langsung. Pastikan untuk selalu memakai masker, menjaga jarak, dan mencuci tangan.",
        "Pneumonia": "Kenapa Pneumonia? Pneumonia dapat disebabkan oleh infeksi bakteri, virus, atau jamur. Risiko meningkat pada perokok, orang dengan sistem imun lemah, atau paparan polusi udara.",
        "Normal": "Tips: Hindari merokok, lakukan olahraga secara teratur, makan makanan bergizi, dan lakukan pemeriksaan kesehatan rutin."
    }

    if label in descriptions:
        # Mengatur ukuran font lebih kecil untuk deskripsi
        c.setFont("Helvetica", 10)
        c.drawString(40, y_position, "Deskripsi Penyakit:")
        y_position -= 20
        text = descriptions[label]
        # Membagi teks menjadi beberapa baris dan menambahkannya
        for line in text.split('. '):
            c.drawString(60, y_position, f"- {line.strip()}.")
            y_position -= 20

        # Menambahkan tips kesehatan dengan ukuran font yang sama
        c.drawString(40, y_position, "Tips Kesehatan:")
        y_position -= 20
        tip_text = tips[label]
        for line in tip_text.split('. '):
            c.drawString(60, y_position, f"- {line.strip()}.")
            y_position -= 20

    return y_position


# Fungsi untuk membuat PDF dengan format medical check-up
def create_pdf_with_images(results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 50, "Hasil Medical Check-Up With ALus Diagnosa")
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 70, f"Tanggal: {datetime.now().strftime('%d-%m-%Y')}")

    # Informasi Institusi
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 100, "ALus Diagnosa")
    c.drawString(40, height - 115, "Jl. Kesehatan No. 123, Bandung")
    c.drawString(40, height - 130, "Telp: (021) 123-4567 | Email: info@rsxyz.co.id")

    y_position = height - 160

    for file_name, label, confidence, image, predictions, categories in results:
        # Menambahkan nama file dan hasil diagnosa
        c.setFont("Helvetica", 12)
        c.drawString(40, y_position, f"Nama File: {file_name}")
        y_position -= 20
        c.drawString(40, y_position, f"Prediksi: {label} ({confidence * 100:.2f}%)")
        y_position -= 20

        # Menambahkan deskripsi penyakit dan tips kesehatan
        y_position = add_disease_description_and_tips(c, label, y_position)

        # Menambahkan tabel probabilitas
        table_data = [["Kelas", "Probabilitas (%)"]] + list(zip(categories, [f"{p * 100:.2f}" for p in predictions]))
        table = Table(table_data, colWidths=[200, 150])
        table.setStyle(TableStyle([  
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table_width, table_height = table.wrap(0, 0)
        if y_position - table_height < 100:
            c.showPage()
            y_position = height - 160
        table.drawOn(c, 40, y_position - table_height)
        y_position -= table_height + 20

        # Menambahkan gambar
        img = ImageReader(image)
        img_width, img_height = 200, 200
        if y_position - img_height < 100:
            c.showPage()
            y_position = height - 160
        c.drawImage(img, 40, y_position - img_height, width=img_width, height=img_height)
        y_position -= img_height + 20

        if y_position < 100:
            c.showPage()
            y_position = height - 160

    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(40, 50, "Dokumen ini diterbitkan oleh ALus Diagnosa sebagai hasil analisis X-Ray.")
    c.drawString(40, 35, "Untuk informasi lebih lanjut, silakan hubungi dokter Anda.")

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
    st.write("Gunakan aplikasi ini untuk menganalisis gambar X-Ray paru-paru dan mendeteksi penyakit terkait seperti COVID-19, Normal, atau Pneumonia.")
    
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
