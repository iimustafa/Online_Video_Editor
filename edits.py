import streamlit as st

# --- 1. Set Custom Page Configuration ---
st.set_page_config(
    page_title="Palette Genius",
    layout="wide", # Use wide for more space for the palette
    initial_sidebar_state="collapsed"
)

# --- 2. Custom CSS for UI (Creative/Simple UI) ---
# Inject CSS to give it a custom look
st.markdown("""
<style>
    /* Center the title */
    .block-container {
        padding-top: 2rem;
    }
    /* Style for the individual color box */
    .color-box {
        height: 150px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: flex-end;
        justify-content: center;
        padding-bottom: 10px;
        font-weight: bold;
        color: #fff; /* For contrast */
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Palette Genius: Your Mood, Your Colors")
st.caption("Generate harmonious 5-color palettes from an image or a creative prompt.")

# --- 3. Input Tabs (Organization) ---
tab1, tab2 = st.tabs(["🖼️ Image Uploader", "✍️ Text Prompt"])

with tab1:
    uploaded_file = st.file_uploader("Upload an image (PNG, JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        # Placeholder for image processing and color extraction logic
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        # Assuming your logic returns a list of hex codes
        # hex_colors = extract_dominant_colors(uploaded_file)
        hex_colors = ["#1F456E", "#8A9A5B", "#E3D0A3", "#C96D56", "#4A373A"] 
        
        st.subheader("Generated Palette")
        cols = st.columns(5) # Create 5 equal columns for the palette
        
        for i, color in enumerate(hex_colors):
            with cols[i]:
                # Use st.markdown with unsafe_allow_html to inject the custom color box
                # The onclick part is a simplified representation of click-to-copy
                st.markdown(
                    f"""
                    <div class='color-box' 
                         style='background-color: {color};' 
                         onclick="navigator.clipboard.writeText('{color}'); alert('Copied {color}!');">
                         {color}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
with tab2:
    text_prompt = st.text_input("Describe the mood or scene:", "Cozy Autumn Evening")
    
    if st.button("Generate Palette from Prompt"):
        # Placeholder for AI/Search logic
        st.info(f"Generating palette for: **{text_prompt}**")
        # You'd replace this with a lookup or a call to a model
        prompt_colors = ["#A1887F", "#4E342E", "#D7CCC8", "#8D6E63", "#FFCC80"]
        
        st.subheader("Generated Palette")
        prompt_cols = st.columns(5)
        
        for i, color in enumerate(prompt_colors):
            with prompt_cols[i]:
                st.markdown(
                    f"""
                    <div class='color-box' 
                         style='background-color: {color};' 
                         onclick="navigator.clipboard.writeText('{color}'); alert('Copied {color}!');">
                         {color}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
