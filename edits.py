import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import io

# --- FUNCTION 1: DYNAMIC COLOR EXTRACTION LOGIC ---
def get_dominant_colors(uploaded_file, n_colors=5):
    """
    Analyzes an image and returns the Hex codes of the N most dominant colors 
    using K-Means Clustering.
    """
    # Read the file from the Streamlit UploadedFile object
    img = Image.open(uploaded_file)
    
    # Resize and convert to RGB for consistency and faster processing
    img = img.convert("RGB")
    # Resize to a smaller image (e.g., 150x150) to speed up clustering
    img = img.resize((150, 150))
    
    # Convert image data to a numpy array of pixels: (width * height, 3)
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 3)
    
    # Use K-Means Clustering to find N dominant colors
    kmeans = KMeans(n_clusters=n_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    # The cluster centers are the dominant colors in RGB format
    dominant_rgb = kmeans.cluster_centers_.astype(int)
    
    # Convert RGB to Hex codes
    hex_colors = []
    for rgb in dominant_rgb:
        hex_color = '#%02x%02x%02x' % tuple(rgb)
        hex_colors.append(hex_color)
        
    return hex_colors


# --- FUNCTION 2: MAIN APP LOGIC ---

# 1. Set Custom Page Configuration
st.set_page_config(
    page_title="Palette Genius",
    layout="wide", # Use wide for more space for the palette
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for Creative UI
# Injects CSS to style the color boxes and add the click-to-copy JavaScript
st.markdown("""
<style>
    /* Custom Streamlit layout adjustments */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Style for the individual color box container */
    .color-box {
        height: 150px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: flex-end;
        justify-content: center;
        padding-bottom: 10px;
        font-weight: bold;
        color: #fff; 
        font-family: monospace;
        transition: transform 0.2s;
    }
    
    /* Add a hover effect */
    .color-box:hover {
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)


# --- JAVASCRIPT FOR CLICK-TO-COPY (Streamlit friendly) ---
# A helper function to add a copy button that runs JavaScript
def copy_to_clipboard_js(color_hex):
    """Generates the HTML/JS for a click-to-copy action."""
    return f"""
    <script>
        function copyText(hex) {{
            navigator.clipboard.writeText(hex)
                .then(() => {{
                    // Simple visual feedback could be implemented here if a custom component was used
                }})
                .catch(err => {{
                    console.error('Could not copy text: ', err);
                }});
        }}
    </script>
    <div class='color-box' 
         style='background-color: {color_hex};' 
         onclick="copyText('{color_hex}')">
         <span style="color: #000; background: rgba(255, 255, 255, 0.7); padding: 2px 6px; border-radius: 4px; user-select: none; cursor: pointer;" title="Click to Copy">{color_hex}</span>
    </div>
    """


st.title("🎨 Palette Genius: Your Mood, Your Colors")
st.caption("Generate harmonious 5-color palettes from an image or a creative prompt.")

st.divider()

# 3. Input Tabs (Organization)
tab1, tab2 = st.tabs(["🖼️ Image Uploader", "✍️ Text Prompt"])

# --- TAB 1: IMAGE UPLOADER ---
with tab1:
    st.markdown("Upload a photo and we'll extract the 5 most dominant colors.")
    uploaded_file = st.file_uploader("Choose an image (PNG, JPG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        
        # Display the uploaded image
        st.image(uploaded_file, caption="Source Image", use_column_width=True)
        
        st.subheader("Generated Palette")
        try:
            # Call the dynamic function
            hex_colors = get_dominant_colors(uploaded_file, n_colors=5)
            
            cols = st.columns(5) # Create 5 equal columns for the palette
            
            for i, color in enumerate(hex_colors):
                with cols[i]:
                    # Display the color box with click-to-copy functionality
                    st.markdown(
                        copy_to_clipboard_js(color), 
                        unsafe_allow_html=True
                    )
            st.success("Palette generated! Click any Hex code to copy it.")
            
        except Exception as e:
            st.error(f"An error occurred during color extraction. Please try a different image. Details: {e}")

# --- TAB 2: TEXT PROMPT (Placeholder for Future Expansion) ---
with tab2:
    st.markdown("Describe a mood or a scene and generate a corresponding color palette.")
    text_prompt = st.text_input("Describe the mood or scene:", "Cozy Autumn Evening")
    
    if st.button("Generate Palette from Prompt"):
        
        # Placeholder Logic: In a real app, this would use an API or a pre-defined mapping.
        st.info(f"Using a placeholder palette for the prompt: **{text_prompt}**")
        
        # A static palette matching the "Cozy Autumn Evening" vibe
        prompt_colors = ["#A1887F", "#4E342E", "#D7CCC8", "#8D6E63", "#FFCC80"]
        
        st.subheader("Generated Palette")
        prompt_cols = st.columns(5)
        
        for i, color in enumerate(prompt_colors):
            with prompt_cols[i]:
                st.markdown(
                    copy_to_clipboard_js(color), 
                    unsafe_allow_html=True
                )
        st.success("Palette generated! Click any Hex code to copy it.")
