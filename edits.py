import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import warnings
import requests
from io import BytesIO

# Suppress K-Means initialization warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# --- HELPER FUNCTIONS ---

def get_dominant_colors(image_file, n_colors=5):
    """
    Analyzes an image file (BytesIO or UploadedFile) and returns the Hex codes 
    of the N most dominant colors using K-Means Clustering.
    """
    img = Image.open(image_file).convert("RGB")
    # Resize for faster processing
    img = img.resize((150, 150))
    
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 3)
    
    # K-Means Clustering
    kmeans = KMeans(n_clusters=n_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    dominant_rgb = kmeans.cluster_centers_.astype(int)
    
    # Convert RGB to Hex codes
    hex_colors = []
    for rgb in dominant_rgb:
        hex_color = '#%02x%02x%02x' % tuple(rgb)
        hex_colors.append(hex_color)
        
    return hex_colors

def fetch_image_from_url(url):
    """Fetches image content from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching image from URL: {e}")
        return None

def render_color_box(color_hex):
    """
    Renders the color box and the copyable Hex code using Streamlit's native features.
    """
    # 1. Display the color box (using HTML/CSS for visual appeal)
    st.markdown(
        f"""
        <div style="background-color: {color_hex}; 
                    height: 150px; 
                    border-radius: 12px; 
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # 2. Display the Hex code using st.code, which has built-in copy functionality
    # The language='text' ensures a clean, monospaced look
    st.code(color_hex, language='text', line_numbers=False)


# --- UI SETUP: DARK/LIGHT MODE TOGGLE ---

# Initialize session state for the theme
if 'dark_mode' not in st.session_state:
    # Set default based on Streamlit's default theme (assuming default is light)
    st.session_state.dark_mode = True # Start with dark mode for high contrast

def toggle_theme():
    """Toggles the dark_mode state and reruns the app to apply CSS."""
    st.session_state.dark_mode = not st.session_state.dark_mode
    # Use st.rerun() to force the script to restart and apply the new CSS class
    st.rerun()

# --- STREAMLIT PAGE CONFIG AND CUSTOM CSS ---

st.set_page_config(
    page_title="Palette Genius",
    layout="wide",
    initial_sidebar_state="expanded" # Set sidebar to expanded
)

# Apply the appropriate CSS class to the main container
theme_class = "dark-mode-container" if st.session_state.dark_mode else "light-mode-container"

st.markdown(f'<div class="{theme_class}">', unsafe_allow_html=True) # Open main container div

# 2. Custom CSS for Dark/Light Mode and Widget Styling
st.markdown(f"""
<style>
    /* Base Streamlit overrides */
    .stApp {{
        background-color: {'#1c1f24' if st.session_state.dark_mode else '#f0f2f6'};
        color: {'#e0e0e0' if st.session_state.dark_mode else '#111111'};
    }}
    .st-emotion-cache-1kyxreqf {{ /* Sidebar background */
        background-color: {'#2c3038' if st.session_state.dark_mode else '#ffffff'};
    }}
    h1, h2, h3, .stMarkdown p, .st-emotion-cache-qbevgv {{
        color: {'#e0e0e0' if st.session_state.dark_mode else '#111111'} !important;
    }}

    /* Code Block Styling (for Hex codes) */
    div[data-testid="stCodeBlock"] {{
        border: none;
        padding: 0 !important;
        margin-top: -10px;
    }}
    div[data-testid="stCodeBlock"] pre {{
        background-color: transparent !important;
        color: {'#e0e0e0' if st.session_state.dark_mode else '#111111'} !important;
        font-weight: bold;
        text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (THEME TOGGLE) ---

with st.sidebar:
    st.title("Settings")
    
    mode_text = "🌙 Dark Mode" if st.session_state.dark_mode else "☀️ Light Mode"
    
    st.button(
        f"Toggle to {mode_text}", 
        on_click=toggle_theme, 
        use_container_width=True
    )
    st.markdown("---")
    st.info("Palette Genius finds the most dominant colors in any image you provide.")

# --- MAIN APP CONTENT ---

st.title("🎨 Palette Genius")
st.caption("Extract harmonious 5-color palettes from uploaded images or web URLs.")

st.divider()

# 4. Split Features into 2 Boxes (Columns)
col1, col2 = st.columns(2)

# --- BOX 1: IMAGE UPLOADER ---
with col1:
    with st.container(border=True): # Use a container with a border for the "box" effect
        st.header("🖼️ From Your Device")
        st.markdown("Upload a photo and analyze its core color scheme.")
        uploaded_file = st.file_uploader("Choose an image (PNG, JPG)", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Source Image", use_column_width=True)
            st.subheader("Generated Palette")
            
            try:
                hex_colors = get_dominant_colors(uploaded_file, n_colors=5)
                palette_cols = st.columns(5)
                
                for i, color in enumerate(hex_colors):
                    with palette_cols[i]:
                        render_color_box(color)
                
            except Exception:
                st.error("Error processing image file. Please check the file format.")

# --- BOX 2: IMAGE URL (Creative Alternative) ---
with col2:
    with st.container(border=True): # Use a container with a border for the "box" effect
        st.header("🌐 From the Web")
        st.markdown("Paste an image URL to extract its color palette instantly.")
        image_url = st.text_input("Image URL:", placeholder="e.g., https://unsplash.com/photos/...")
        
        if image_url:
            with st.spinner("Fetching and analyzing image..."):
                image_bytes = fetch_image_from_url(image_url)
                
            if image_bytes:
                st.image(image_bytes, caption="Image from URL", use_column_width=True)
                st.subheader("Generated Palette")
                
                try:
                    hex_colors = get_dominant_colors(image_bytes, n_colors=5)
                    palette_cols = st.columns(5)
                    
                    for i, color in enumerate(hex_colors):
                        with palette_cols[i]:
                            render_color_box(color)
                            
                except Exception:
                    st.error("Error processing image data from URL.")
            
# Close the main container div applied at the beginning
st.markdown('</div>', unsafe_allow_html=True)
