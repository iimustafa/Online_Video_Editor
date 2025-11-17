import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def get_dominant_colors(uploaded_file, n_colors=5):
    """
    Analyzes an image and returns the Hex codes of the N most dominant colors.
    """
    # 1. Open the image
    img = Image.open(uploaded_file)
    
    # 2. Resize the image for faster processing (optional but recommended)
    img = img.resize((150, 150))
    
    # 3. Convert image data to a numpy array of pixels
    # We reshape it to a list of (R, G, B) pixels
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 3)
    
    # 4. Use K-Means Clustering to find N dominant colors
    kmeans = KMeans(n_clusters=n_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    # The cluster centers are the dominant colors in RGB format
    dominant_rgb = kmeans.cluster_centers_.astype(int)
    
    # 5. Convert RGB to Hex codes
    hex_colors = []
    for rgb in dominant_rgb:
        hex_color = '#%02x%02x%02x' % tuple(rgb)
        hex_colors.append(hex_color)
        
    return hex_colors
