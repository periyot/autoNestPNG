import streamlit as st
from PIL import Image
from fpdf import FPDF
import base64
import io
import os
import pandas as pd

class UploadedImage:
    def __init__(self, file_name, image_data):
        self.file_name = file_name
        self.image_data = image_data

def main():
    st.title("PNGs To PDFs")

    uploaded_files = st.file_uploader("Upload Foto, Bisa lebih dari satu gambar", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files is not None:
        # Membuat direktori untuk menyimpan file yang diunggah
        save_directory = "uploaded_images"
        os.makedirs(save_directory, exist_ok=True)

        uploaded_images = []

        for uploaded_file in uploaded_files:
            # Membaca file yang diunggah ke dalam objek BytesIO
            image_data = io.BytesIO(uploaded_file.read())

            # Membuka gambar menggunakan PIL
            image = Image.open(image_data)

            # Menampilkan gambar
            # st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)

            # Membuat nama file unik dengan menambahkan nomor unik
            unique_file_name = get_unique_file_name(save_directory, uploaded_file.name)
            file_path = os.path.join(save_directory, unique_file_name)
            
            # Menyimpan gambar
            image.save(file_path)

            # Membuat objek UploadedImage
            uploaded_image = UploadedImage(file_name=unique_file_name, image_data=image_data)
            uploaded_images.append(uploaded_image)

            # st.success(f"Image '{uploaded_file.name}' saved successfully as '{unique_file_name}'")
        
        if st.button('Jadikan PDFs'):
            imageTopdf(save_directory)
        
        os.system(f'rm -dfr {save_directory}')



def get_unique_file_name(directory, file_name):
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    unique_file_name = file_name

    while os.path.exists(os.path.join(directory, unique_file_name)):
        unique_file_name = f"{base_name}_{counter}{extension}"
        counter += 1

    return unique_file_name

def imageTopdf(dirname):
    dir = os.listdir(dirname)
    pdf = FPDF()
    for i in dir:
        pdf.add_page()
        dr = os.path.join(dirname, i)
        pdf.image(dr, 60,60,120)
    
    def create_download_link(val, filename):
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")
    st.markdown(html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()