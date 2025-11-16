import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

# --- Configuration and Styling ---

st.set_page_config(
    page_title="Prism Flux Watermarker", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for the "Prism Flux" look: 
# 1. Hide Streamlit menu/footer.
# 2. Set dark mode background and primary color accent.
st.markdown(
    """
    <style>
    /* Hide the Streamlit header/footer/menu */
    #MainMenu, footer {visibility: hidden;}
    
    /* Set body and main container background color (dark theme) */
    .stApp {
        background-color: #1a1a1a;
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }

    /* Adjust Streamlit primary color to the accent blue/purple */
    :root {
        --primary-color: #5560e9; 
    }
    
    /* Style for the main header (large, centered) */
    .big-font {
        font-size: 50px !important;
        font-weight: 700;
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    
    /* Style for the tagline */
    .tagline {
        font-size: 18px;
        color: #aaaaaa;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 40px;
    }

    /* Style for primary call-to-action button */
    .stButton>button {
        background-color: #5560e9;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #727de9;
    }
    
    /* Center the file uploader */
    .stFileUploader {
        display: flex;
        justify-content: center;
    }
    .stFileUploader>div>div {
        min-width: 400px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --- 1. Header Section ---
st.markdown('<div class="big-font">PDF Watermark Forge</div>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Secure your documents with instant, custom watermarks—no servers, no waiting.</p>', unsafe_allow_html=True)

# --- 2. Main Content / Input Area ---
# Use columns to center the input elements
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### Upload Document")
    # FIX: Add a descriptive label (e.g., "PDF Uploader")
    uploaded_file = st.file_uploader("PDF Uploader", type=['pdf'], label_visibility="collapsed")
    
    st.markdown("### Watermark Text")
    # FIX: Add a descriptive label (e.g., "Watermark Text Input")
    watermark_text = st.text_input("Watermark Text Input", "CONFIDENTIAL", label_visibility="collapsed")
    
    # Simple placeholder to show where processing would occur
    if uploaded_file is None:
        st.info("Upload a PDF and enter your watermark text above to begin.")


# --- Watermarking Logic (Executed on upload/text change) ---

if uploaded_file is not None and watermark_text:
    st.divider()
    
    # Progress indicator
    with st.spinner('Processing PDF...'):
        try:
            # 1. Create the watermark PDF
            packet = io.BytesIO()
            # Set size based on standard letter
            c = canvas.Canvas(packet, pagesize=letter)
            
            c.setFont("Helvetica-Bold", 40)
            c.setFillColorRGB(1, 1, 1, alpha=0.10) # White text, highly transparent
            
            # Position the watermark diagonally across the page
            width, height = letter
            c.translate(width / 2, height / 2)
            c.rotate(45) 
            c.drawCentredString(0, 0, watermark_text)
            
            c.save()
            packet.seek(0)
            watermark_reader = PdfReader(packet)
            watermark_page = watermark_reader.pages[0]

            # 2. Read the input PDF
            input_pdf = PdfReader(uploaded_file)
            pdf_writer = PdfWriter()

            # 3. Apply watermark to every page
            for page in input_pdf.pages:
                page.merge_page(watermark_page)
                pdf_writer.add_page(page)

            # 4. Save the output PDF to a BytesIO buffer
            output_pdf_buffer = io.BytesIO()
            pdf_writer.write(output_pdf_buffer)
            output_pdf_buffer.seek(0)

            # --- 3. Output/Download Section ---
            st.success("✅ Watermarking successful!")
            
            # Use columns to center the download button
            d_col1, d_col2, d_col3 = st.columns([1, 1, 1])
            with d_col2:
                st.download_button(
                    label="Download Watermarked PDF",
                    data=output_pdf_buffer,
                    file_name="watermarked_" + uploaded_file.name,
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Please check if the uploaded file is a valid, unencrypted PDF.")
            
# --- 4. Footer Section (Mimics the bottom of the template) ---

st.divider()

f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
with f_col2:
    st.markdown(
        """
        <div style="text-align: center; color: #666666; padding: 20px 0;">
            <p>Built with Streamlit and Python. | Theme inspired by TemplateMo Prism Flux.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
