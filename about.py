import streamlit as st

def display_about():
    st.title("Tentang Aplikasi")
    st.write("Aplikasi ini menggunakan model deep learning (InceptionV3) untuk mengklasifikasikan gambar X-ray paru-paru menjadi tiga kategori: COVID, Pneumonia, dan Normal.")
    st.write("### Pengembang:")
    st.markdown("- Wildan Miladji")
    st.markdown("- Robert William")
    st.markdown("- Rayhan Gading")
    st.markdown("- Yahya Bachtiar")
    st.markdown("- Siti Arwiyah")
    st.write("### Fitur Utama:")
    st.markdown("- **Klasifikasi gambar individu**: Unggah satu atau beberapa gambar X-ray untuk klasifikasi.")
    st.markdown("- **Klasifikasi file ZIP**: Unggah file ZIP berisi banyak gambar untuk klasifikasi.")
    st.markdown("- **Unduh hasil dalam PDF**: Hasil klasifikasi gambar dapat diunduh dalam bentuk PDF.")
    st.markdown("- **Deep Learning Model**: Menggunakan model InceptionV3 yang sudah dilatih.")
