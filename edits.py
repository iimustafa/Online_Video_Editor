import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

# --- Configuration ---
st.set_page_config(
    page_title="Cyber-Flux Watermarker", 
    layout="wide", 
    initial_sidebar_state="expanded" # Start with sidebar open
)

# Initialize session state for mode and module selection
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True 
if 'module' not in st.session_state:
    st.session_state.module = "Watermark Forge" 

# --- CSS Styling Function ---

def get_css(is_dark):
    """Generates the Cyber-Vaporwave CSS based on the mode."""
    
    # --- Theme Colors ---
    if is_dark:
        # Dark Theme Colors
        bg_color = "#12023d"     # Deep Purple/Blue
        card_bg = "#1f0756"      # Slightly lighter purple for the card
        text_color = "#f2f2f2"   # Near white
        accent_color = "#ff33ff" # Neon Pink
        tagline_color = "#99ccff" # Light blue accent
        shadow_color = "rgba(255, 51, 255, 0.5)" # Pink glow
        divider_color = "#4c059a" # Divider color
        sidebar_bg = "#100030"  # Slightly darker sidebar
        
    else:
        # Light Theme Colors
        bg_color = "#f0f2f6"     # Soft light gray
        card_bg = "#ffffff"      # White card
        text_color = "#333333"   # Dark text
        accent_color = "#00bcd4" # Cyan/Teal
        tagline_color = "#00796b" # Dark teal
        shadow_color = "rgba(0, 188, 212, 0.5)" # Cyan glow
        divider_color = "#cccccc" # Divider color
        sidebar_bg = "#e5e5e5"  # Slightly darker sidebar
        
    return f"""
    <style>
    /* Global Styles */
    #MainMenu, footer {{visibility: hidden;}}
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'Space Mono', monospace;
    }}
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
    }}

    /* Streamlit Primary Color Override (for default widgets) */
    :root {{
        --primary-color: {accent_color}; 
    }}
    
    /* Main Header Style (Large, Glowing) */
    .hero-font {{
        font-size: 60px !important;
        font-weight: 900;
        color: {accent_color};
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 0 10px {shadow_color}, 0 0 20px {shadow_color};
        letter-spacing: 2px;
    }}
    
    /* Tagline Style */
    .tagline {{
        font-size: 24px;
        color: {tagline_color};
        text-align: center;
        margin-top: 5px;
        margin-bottom: 50px;
        font-style: italic;
    }}
    
    /* Input Card Container (Main Content Area) */
    .stContainer {{
        background-color: {card_bg};
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 0 15px {shadow_color};
        margin-top: 20px;
        margin-bottom: 20px;
    }}
    
    /* Custom divider color */
    .stApp hr {{
        border-top: 3px solid {divider_color};
    }}

    /* Accent Button Style */
    .stButton>button {{
        background-color: {accent_color};
        color: {bg_color};
        border-radius: 12px;
        border: none;
        padding: 12px 35px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 10px {shadow_color};
    }}
    .stButton>button:hover {{
        background-color: {tagline_color};
        box-shadow: 0 6px 15px {shadow_color};
    }}

    /* Creative Mode Toggle Buttons (Sidebar) */
    .mode-toggle-button {{
        width: 100%;
        margin: 5px 0;
        padding: 10px 0;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.2s, color 0.2s;
    }}
    
    /* Active Dark Button */
    .mode-toggle-button.dark-active {{
        background-color: #ff33ff; /* Neon Pink */
        color: #12023d; /* Deep Purple */
    }}
    /* Inactive Dark Button */
    .mode-toggle-button.dark-inactive {{
        background-color: {sidebar_bg};
        color: #99ccff;
        border: 1px solid #99ccff;
    }}

    /* Active Light Button */
    .mode-toggle-button.light-active {{
        background-color: #00bcd4; /* Cyan */
        color: #333333;
    }}
    /* Inactive Light Button */
    .mode-toggle-button.light-inactive {{
        background-color: {sidebar_bg};
        color: {text_color};
        border: 1px solid {text_color};
    }}
    
    </style>
    """

# Apply the dynamic CSS
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# --- Utility Functions ---

def watermarker_section():
    """Implements the PDF Watermarker (Protocol 47)."""
    st.markdown('<h2 style="color: #ff33ff;">🔒 Protocol 47: Watermark Forge</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("## 💾 DATA INGESTION: UPLOAD FILE")
        uploaded_file = st.file_uploader("PDF Uploader (Watermark)", type=['pdf'], label_visibility="collapsed", key="wm_uploader")
        
        st.markdown("## ✍️ WATERMARK TEXT: SET TAG")
        watermark_text = st.text_input("Watermark Text Input", "CYBER-FLUX ACCESS DENIED", label_visibility="collapsed", key="wm_text")
        
        if uploaded_file is None:
            st.info("Upload your document and define the security tag.")
            return

        st.markdown("---")
        
        with st.spinner('INITIATING SECURITY PROTOCOL...'):
            try:
                # Watermark Logic (unchanged)
                packet = io.BytesIO()
                c = canvas.Canvas(packet, pagesize=letter)
                c.setFont("Helvetica-Bold", 48)
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

                input_pdf = PdfReader(uploaded_file)
                pdf_writer = PdfWriter()

                for page in input_pdf.pages:
                    page.merge_page(watermark_page)
                    pdf_writer.add_page(page)

                output_pdf_buffer = io.BytesIO()
                pdf_writer.write(output_pdf_buffer)
                output_pdf_buffer.seek(0)

                st.success("PROTOCOL SUCCESSFUL: DOCUMENT SECURED.")
                
                d_col1, d_col2, d_col3 = st.columns([1, 1, 1])
                with d_col2:
                    st.download_button(
                        label="DOWNLOAD SECURED DATA",
                        data=output_pdf_buffer,
                        file_name="SECURED_" + uploaded_file.name,
                        mime="application/pdf"
                    )

            except Exception as e:
                st.error(f"PROTOCOL FAILURE: {e}")
                st.info("Ensure the data file is a valid, unencrypted PDF format.")


def page_counter_section():
    """Implements the simple PDF Page Counter (Diagnostic Module)."""
    st.markdown('<h2 style="color: #ff33ff;">🔬 Diagnostic Module: Page Counter</h2>', unsafe_allow_html=True)

    with st.container():
        st.markdown("## 📥 FILE ACCESS: UPLOAD PDF")
        
        uploaded_file = st.file_uploader("PDF Uploader (Counter)", type=['pdf'], label_visibility="collapsed", key="pc_uploader")
        
        if uploaded_file is None:
            st.info("Upload a PDF to run the diagnostic module.")
            return

        st.markdown("---")

        with st.spinner('RUNNING DIAGNOSTIC...'):
            try:
                # Read PDF
                reader = PdfReader(uploaded_file)
                page_count = len(reader.pages)

                st.success("DIAGNOSTIC COMPLETE.")
                st.markdown(f"""
                <div style="padding: 15px; border: 2px solid {st.get_option('theme.primaryColor')}; border-radius: 10px; text-align: center;">
                    <h3 style="color: {st.get_option('theme.primaryColor')}; margin: 0;">TOTAL PAGES DETECTED</h3>
                    <p style="font-size: 50px; font-weight: bold; margin: 5px 0 0 0;">{page_count}</p>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"DIAGNOSTIC ERROR: {e}")
                st.info("The file could not be read. Please check the PDF integrity.")


# --- Sidebar Setup ---

with st.sidebar:
    st.markdown('<h2 style="color: #ff33ff;">// SYSTEM CONTROL //</h2>', unsafe_allow_html=True)
    st.divider()

    # --- Mode Toggle (Creative Buttons) ---
    st.markdown('<h3 style="color: #99ccff;">DISPLAY MODE</h3>', unsafe_allow_html=True)
    
    col_d, col_l = st.columns(2)
    
    with col_d:
        dark_class = "dark-active" if st.session_state.dark_mode else "dark-inactive"
        if st.markdown(f'<div class="mode-toggle-button {dark_class}">🌙 DARK</div>', unsafe_allow_html=True):
            if not st.session_state.dark_mode:
                st.session_state.dark_mode = True
                st.experimental_rerun()
    
    with col_l:
        light_class = "light-active" if not st.session_state.dark_mode else "light-inactive"
        if st.markdown(f'<div class="mode-toggle-button {light_class}">☀️ LIGHT</div>', unsafe_allow_html=True):
            if st.session_state.dark_mode:
                st.session_state.dark_mode = False
                st.rerun()
    
    st.divider()

    # --- Task Selection ---
    st.markdown('<h3 style="color: #99ccff;">MODULE SELECTION</h3>', unsafe_allow_html=True)
    
    # Use radio buttons for clear task selection
    selected_module = st.radio(
        label="Select Task Module",
        options=["Watermark Forge", "Diagnostic Module"],
        index=0 if st.session_state.module == "Watermark Forge" else 1,
        key="module_radio",
        label_visibility="collapsed"
    )
    st.session_state.module = selected_module
    
    st.divider()

    # --- Tuwaiq Academy Mission Section (Branding moved to sidebar) ---
    st.markdown('<h3 style="color: #ff33ff;">// ACADEMY PROTOCOL //</h3>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <p style="font-size: 14px; color: #99ccff;">
        This utility is part of the core mission of 
        <strong style="color: #ff33ff;">Tuwaiq Academy</strong>: developing the next generation of Saudi engineers in Cyber Security and Programming, aligned with Vision 2030.
        </p>
        <p style="font-size: 12px; text-align: right; color: #6a5acd;">
        — *Powered by SAFCSP*
        </p>
        """, 
        unsafe_allow_html=True
    )


# --- Main Content Area ---
h_col1, h_col2, h_col3 = st.columns([1, 4, 1])
with h_col2:
    st.markdown('<div class="hero-font">SECURE.PDF // CYBER-FLUX</div>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">A Data Integrity Console.</p>', unsafe_allow_html=True)

st.divider()

# --- Display selected module content ---
col_main = st.columns([0.5, 4, 0.5])
with col_main[1]:
    if st.session_state.module == "Watermark Forge":
        watermarker_section()
    elif st.session_state.module == "Diagnostic Module":
        page_counter_section()


# --- Footer Section ---
st.markdown("---")

f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
with f_col2:
    st.markdown(
        """
        <div style="text-align: center; color: #6a5acd; padding: 10px 0;">
            <p>DESIGNED & DEPLOYED // STATUS: ONLINE //</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
