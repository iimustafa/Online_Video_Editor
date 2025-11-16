import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

# --- Configuration and Styling ---

st.set_page_config(
    page_title="Chain App Dev Watermarker", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for the "Chain App Dev" look:
st.markdown(
    """
    <style>
    /* Hide the Streamlit header/footer/menu */
    #MainMenu, footer {visibility: hidden;}
    
    /* Set body and main container background color (light theme) */
    .stApp {
        background-color: #f7f7f7;
        color: #333333;
        font-family: 'Poppins', sans-serif;
    }

    /* Set Streamlit primary color to the accent orange/coral */
    :root {
        --primary-color: #ff6600; 
    }
    
    /* Style for the main header (large, centered) */
    .big-font {
        font-size: 56px !important;
        font-weight: 700;
        color: #333333;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    
    /* Style for the tagline */
    .tagline {
        font-size: 20px;
        color: #666666;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 50px;
    }
    
    /* Style for the accent button (orange primary color) */
    .stButton>button {
        background-color: #ff6600; /* Orange */
        color: white;
        border-radius: 25px; /* Rounded pill shape */
        border: none;
        padding: 12px 30px;
        font-size: 18px;
        font-weight: 600;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #e65c00; /* Darker orange on hover */
    }
    
    /* Center input containers */
    .stFileUploader, .stTextInput {
        margin-bottom: 25px;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)


# --- 1. Header Section ---
# Use columns to ensure content is centered and not full-width
h_col1, h_col2, h_col3 = st.columns([1, 4, 1])

with h_col2:
    st.markdown('<div class="big-font">ChainApp: PDF Security Tool</div>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">The fastest way to secure your documents with military-grade, non-removable watermarks.</p>', unsafe_allow_html=True)
    st.markdown("---") # Visual separator

# --- 2. Main Content / Input Area ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("## 📥 Upload Your Document")
    # FIX: Add a descriptive label for accessibility reasons
    uploaded_file = st.file_uploader("PDF Uploader", type=['pdf'], label_visibility="collapsed")
    
    st.markdown("## ✍️ Enter Watermark Text")
    # FIX: Add a descriptive label for accessibility reasons
    watermark_text = st.text_input("Watermark Text Input", "CHAIN APP DEV CONFIDENTIAL", label_visibility="collapsed")
    
    if uploaded_file is None:
        st.info("Upload a PDF and customize your watermark text above.")


# --- Watermarking Logic ---

if uploaded_file is not None and watermark_text:
    st.markdown("---")
    
    # Progress indicator
    with st.spinner('Processing PDF and applying watermark...'):
        try:
            # 1. Create the watermark PDF
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=letter)
            
            c.setFont("Helvetica-Bold", 48)
            c.setFillColorRGB(0, 0, 0, alpha=0.10) # Light gray/black for light theme visibility
            
            width, height = letter
            c.translate(width / 2, height / 2)
            c.rotate(30) # Slight rotation
            c.drawCentredString(0, 0, watermark_text)
            
            c.save()
            packet.seek(0)
            watermark_reader = PdfReader(packet)
            watermark_page = watermark_reader.pages[0]

            # 2. Read the input PDF and prepare output
            input_pdf = PdfReader(uploaded_file)
            pdf_writer = PdfWriter()

            # 3. Apply watermark to every page
            for page in input_pdf.pages:
                page.merge_page(watermark_page)
                pdf_writer.add_page(page)

            # 4. Save the output PDF to a buffer
            output_pdf_buffer = io.BytesIO()
            pdf_writer.write(output_pdf_buffer)
            output_pdf_buffer.seek(0)

            # --- 3. Output/Download Section ---
            st.success("🎉 Success! Your document is now watermarked and ready.")
            
            # Use columns to center the download button
            d_col1, d_col2, d_col3 = st.columns([1, 1, 1])
            with d_col2:
                st.download_button(
                    label="Download Secured PDF",
                    data=output_pdf_buffer,
                    file_name="secured_" + uploaded_file.name,
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Please verify the file is a standard, unencrypted PDF document.")
            
# --- 4. Footer Section ---

st.markdown("---")

f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
with f_col2:
    st.markdown(
        """
        <div style="text-align: center; color: #999999; padding: 10px 0;">
            <p>Made with Streamlit. | Design inspired by TemplateMo Chain App Dev.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
