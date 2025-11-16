import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

st.set_page_config(layout="wide")
st.title("📝 Simple Streamlit PDF Watermarker")

# --- User Inputs ---
uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])
watermark_text = st.text_input("Enter Watermark Text:", "CONFIDENTIAL")

# --- Main Logic ---
if uploaded_file is not None and watermark_text:
    
    # 1. Create the watermark PDF
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    
    # Configure watermark appearance
    c.setFont("Helvetica", 40)
    c.setFillColorRGB(0, 0, 0, alpha=0.15) # Light gray with transparency
    
    # Position the watermark diagonally across the page
    width, height = letter
    c.translate(width / 2, height / 2)
    c.rotate(45) # Rotate 45 degrees
    c.drawCentredString(0, 0, watermark_text)
    
    c.save()
    packet.seek(0)
    watermark_reader = PdfReader(packet)
    watermark_page = watermark_reader.pages[0]

    # 2. Read the input PDF
    input_pdf = PdfReader(uploaded_file)
    pdf_writer = PdfWriter()

    st.info(f"Adding watermark '{watermark_text}' to {len(input_pdf.pages)} pages...")

    # 3. Apply watermark to every page
    for page in input_pdf.pages:
        # Merge the watermark page onto the existing page
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    # 4. Save the output PDF to a BytesIO buffer
    output_pdf_buffer = io.BytesIO()
    pdf_writer.write(output_pdf_buffer)
    output_pdf_buffer.seek(0)

    st.success("PDF Watermarking complete!")

    # 5. Provide Download Button
    st.download_button(
        label="Download Watermarked PDF",
        data=output_pdf_buffer,
        file_name="watermarked_" + uploaded_file.name,
        mime="application/pdf"
    )
