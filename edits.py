import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import warnings

# Suppress K-Means initialization warning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# --- FUNCTION 1: DYNAMIC COLOR EXTRACTION LOGIC ---
def get_dominant_colors(uploaded_file, n_colors=5):
    """
    Analyzes an image and returns the Hex codes of the N most dominant colors 
    using K-Means Clustering.
    """
    img = Image.open(uploaded_file).convert("RGB")
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


# --- FUNCTION 2: RENDER COLOR BOX (The UI Fix) ---
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
    st.code(color_hex, language='text', line_numbers=False)


# --- MAIN APP LOGIC ---

# 1. Set Custom Page Configuration
st.set_page_config(
    page_title="Palette Genius",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for base styles
st.markdown("""
<style>
    /* Custom Streamlit layout adjustments */
    .block-container {
        padding-top: 2rem;
    }
    /* Hide the code block header and border for a cleaner look */
    div[data-testid="stCodeBlock"] {
        border: none;
        padding: 0 !important;
        margin-top: -10px; /* Adjust spacing between box and code */
    }
    div[data-testid="stCodeBlock"] pre {
        background-color: transparent !important;
        color: var(--text-color) !important;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


st.title("🎨 Palette Genius: Your Mood, Your Colors")
st.caption("Generate harmonious 5-color palettes from an image or a creative prompt.")

st.divider()

# 3. Input Tabs
tab1, tab2 = st.tabs(["🖼️ Image Uploader", "✍️ Text Prompt"])

# --- TAB 1: IMAGE UPLOADER ---
with tab1:
    st.markdown("Upload a photo and we'll extract the 5 most dominant colors.")
    uploaded_file = st.file_uploader("Choose an image (PNG, JPG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        
        st.image(uploaded_file, caption="Source Image", use_column_width=True)
        st.subheader("Generated Palette")
        
        try:
            hex_colors = get_dominant_colors(uploaded_file, n_colors=5)
            cols = st.columns(5)
            
            for i, color in enumerate(hex_colors):
                with cols[i]:
                    # Call the fixed render function
                    render_color_box(color)
            
        except Exception as e:
            st.error(f"An error occurred during color extraction. Please try a different image. Details: {e}")

# --- TAB 2: TEXT PROMPT ---
with tab2:
    st.markdown("Describe a mood or a scene and generate a corresponding color palette.")
    text_prompt = st.text_input("Describe the mood or scene:", "Cozy Autumn Evening")
    
    if st.button("Generate Palette from Prompt"):
        
        st.info(f"Using a placeholder palette for the prompt: **{text_prompt}**")
        
        # Static palette matching the "Cozy Autumn Evening" vibe
        prompt_colors = ["#A1887F", "#4E342E", "#D7CCC8", "#8D6E63", "#FFCC80"]
        
        st.subheader("Generated Palette")
        prompt_cols = st.columns(5)
        
        for i, color in enumerate(prompt_colors):
            with prompt_cols[i]:
                # Call the fixed render function
                render_color_box(color)
