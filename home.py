import os
import streamlit as st

def display_home():
    # Menampilkan judul dan deskripsi
    st.markdown("""
    <h1 style="text-align: center;">ALus</h1>
    <h2 style="text-align: center;">Artificial Lungs Disease Detection</h2>
    <p style="text-align: center;">Aplikasi klasifikasi gambar paru-paru berdasarkan model MobileNetV2.</p>
    """, unsafe_allow_html=True)

    # Mendapatkan path absolut untuk file gambar
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "Lung.png")

    # Memeriksa apakah file gambar ada
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.error("Gambar tidak ditemukan. Pastikan file 'Lung.png' ada di folder yang benar.")

    # Teks justify
    st.markdown("""
    <p style="text-align: justify; font-size: 18px;">
        Kesehatan paru-paru merupakan komponen vital dalam menjaga kualitas hidup yang optimal. Paru-paru memainkan peran penting dalam 
        sistem pernapasan manusia, yang bertanggung jawab untuk mengalirkan oksigen ke seluruh tubuh dan mengeluarkan karbon dioksida 
        dari aliran darah. Gangguan pada paru-paru, seperti pneumonia dan COVID-19, dapat menurunkan fungsi ini secara signifikan, yang 
        pada akhirnya memengaruhi kesehatan dan aktivitas sehari-hari seseorang.
    </p>
    <p style="text-align: justify; font-size: 18px;">
        Penyakit COVID-19, yang disebabkan oleh virus SARS-CoV-2, merupakan pandemi global yang telah memengaruhi jutaan jiwa. Virus ini 
        menyerang sistem pernapasan, khususnya paru-paru, dan dapat menyebabkan komplikasi serius seperti sindrom gangguan pernapasan akut 
        (ARDS). Deteksi dini COVID-19 melalui analisis gambar X-ray memungkinkan diagnosis cepat dan intervensi medis yang lebih efektif.
    </p>
    <p style="text-align: justify; font-size: 18px;">
        Selain COVID-19, pneumonia juga menjadi salah satu penyebab utama morbiditas dan mortalitas di dunia. Pneumonia adalah infeksi yang 
        menyebabkan peradangan pada kantung udara di paru-paru, yang sering kali dipenuhi dengan cairan atau nanah. Gejala seperti sesak 
        napas, batuk berdahak, dan demam tinggi memerlukan diagnosis yang tepat untuk memberikan pengobatan yang sesuai.
    </p>
    <p style="text-align: justify; font-size: 18px;">
        Dalam era modern ini, teknologi kecerdasan buatan (AI) memberikan solusi baru dalam bidang kesehatan. ALus adalah aplikasi berbasis 
        AI yang dirancang untuk membantu dokter dan profesional medis dalam menganalisis gambar X-ray paru-paru. Dengan menggunakan model 
        MobileNetV2 yang canggih, aplikasi ini dapat mengklasifikasikan kondisi paru-paru menjadi tiga kategori utama: normal, pneumonia, 
        dan COVID-19. Teknologi ini tidak hanya mempercepat proses diagnosis, tetapi juga meningkatkan akurasi dalam menentukan jenis 
        penyakit yang diderita oleh pasien.
    </p>
    <p style="text-align: justify; font-size: 18px;">
        ALus bertujuan untuk menjadi alat bantu yang handal dalam mendiagnosis penyakit paru-paru secara cepat dan efisien. Dengan memanfaatkan 
        data X-ray, algoritma yang digunakan dalam aplikasi ini mampu mendeteksi pola-pola yang mungkin sulit diidentifikasi oleh mata manusia. 
        Hal ini diharapkan dapat mendukung pengambilan keputusan medis yang lebih baik, memberikan peluang lebih besar untuk pemulihan pasien, 
        dan mengurangi beban kerja para tenaga medis.
    </p>
    """, unsafe_allow_html=True)
