import streamlit as st

def display_home():
    # Menampilkan judul dan deskripsi
    st.markdown("""
    <h1 style="text-align: center;">ALus</h1>
    <h2 style="text-align: center;">Artificial Lungs Disease Detection</h2>
    <p style="text-align: center;">Aplikasi klasifikasi gambar paru-paru berdasarkan model MobileNetV2.</p>
    """, unsafe_allow_html=True)

    # Menampilkan gambar di bawah deskripsi
    st.image("assets/image.png", use_container_width=True)

    # Teks justify
    st.markdown("""
    <p style="text-align: justify; font-size: 18px;">
        Kesehatan paru-paru sangat penting untuk kualitas hidup yang optimal. Penyakit paru seperti pneumonia dan infeksi akibat COVID-19 dapat
        mempengaruhi fungsi paru dan menyebabkan gangguan pernapasan. Dengan kemajuan teknologi, deteksi dini melalui gambar X-ray
        dapat membantu mendiagnosis penyakit paru lebih cepat dan lebih akurat.
    </p>
    <p style="text-align: justify; font-size: 18px;">
        COVID-19, yang disebabkan oleh virus SARS-CoV-2, dapat menular melalui udara dan menyebabkan gangguan serius pada paru-paru.
        Pneumonia adalah infeksi yang menyebabkan peradangan pada kantung udara di paru-paru, dan sering kali terkait dengan komplikasi
        dari infeksi seperti COVID-19.
    </p>
    <p style="text-align: justify; font-size: 18px;">
        ALus bertujuan untuk memberikan alat bantu dalam deteksi penyakit paru berdasarkan gambar X-ray, sehingga mempermudah diagnosis
        dan perawatan lebih cepat.
    </p>
    """, unsafe_allow_html=True)