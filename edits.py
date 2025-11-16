import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

# --- Configuration ---
st.set_page_config(
    page_title="Tuwaiq Academy", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Initialize session state for mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False # Default to light mode

# --- CSS Styling Function ---

def get_css(is_dark):
    """Generates the appropriate CSS based on the mode."""
    if is_dark:
        bg_color = "#1a1a1a"    # Dark background
        text_color = "#e0e0e0"  # Light text
        header_color = "#ffffff" # White headers
        tagline_color = "#aaaaaa" # Lighter gray tagline
        
    else: # Light Mode (Chain App Dev style)
        bg_color = "#f7f7f7"    # Very light gray background
        text_color = "#333333"  # Dark text
        header_color = "#333333" # Dark headers
        tagline_color = "#666666" # Medium gray tagline

    # The accent color (orange/coral) remains constant for both modes
    accent_color = "#ff6600" 
    
    return f"""
    <style>
    /* Global Styles */
    #MainMenu, footer {{visibility: hidden;}}
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'Poppins', sans-serif;
    }}

    /* Streamlit Primary Color Override (for default widgets) */
    :root {{
        --primary-color: {accent_color}; 
    }}
    
    /* Main Header Style */
    .big-font {{
        font-size: 56px !important;
        font-weight: 700;
        color: {header_color};
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }}
    
    /* Tagline Style */
    .tagline {{
        font-size: 20px;
        color: {tagline_color};
        text-align: center;
        margin-top: 5px;
        margin-bottom: 50px;
    }}
    
    /* Accent Button Style */
    .stButton>button {{
        background-color: {accent_color}; /* Orange */
        color: white;
        border-radius: 25px;
        border: none;
        padding: 12px 30px;
        font-size: 18px;
        font-weight: 600;
        transition: background-color 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #e65c00; /* Darker orange on hover */
    }}
    
    /* Center input containers */
    .stFileUploader, .stTextInput {{
        margin-bottom: 25px;
    }}
    
    </style>
    """

# Apply the dynamic CSS
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)


# --- 1. Header Section ---
# Add mode toggle in a narrow column to the top right
t_col1, t_col2 = st.columns([10, 1])
with t_col2:
    if st.checkbox('🌙 Dark Mode', value=st.session_state.dark_mode, key='mode_toggle'):
        st.session_state.dark_mode = True
    else:
        st.session_state.dark_mode = False

# Re-run the app to apply CSS if the state changed
if st.session_state.mode_toggle != st.session_state.dark_mode:
    st.experimental_rerun()


# Main title section
h_col1, h_col2, h_col3 = st.columns([1, 4, 1])
with h_col2:
    st.markdown('<div class="big-font">ChainApp: PDF Security Tool</div>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">The fastest way to secure your documents with military-grade, non-removable watermarks.</p>', unsafe_allow_html=True)
    st.markdown("---") 


# --- 2. Main Content / Input Area ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("## 📥 Upload Your Document")
    uploaded_file = st.file_uploader("PDF Uploader", type=['pdf'], label_visibility="collapsed")
    
    st.markdown("## ✍️ Enter Watermark Text")
    watermark_text = st.text_input("Watermark Text Input", "CHAIN APP DEV CONFIDENTIAL", label_visibility="collapsed")
    
    if uploaded_file is None:
        st.info("Upload a PDF and customize your watermark text above.")


# --- Watermarking Logic ---

if uploaded_file is not None and watermark_text:
    st.markdown("---")
    
    with st.spinner('Processing PDF and applying watermark...'):
        try:
            # 1. Create the watermark PDF
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=letter)
            
            c.setFont("Helvetica-Bold", 48)
            # Adjust watermark color based on mode for optimal contrast
            wm_color = (1, 1, 1, 0.10) if st.session_state.dark_mode else (0, 0, 0, 0.10)
            c.setFillColorRGB(*wm_color[:3], alpha=wm_color[3]) 
            
            width, height = letter
            c.translate(width / 2, height / 2)
            c.rotate(30)
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
