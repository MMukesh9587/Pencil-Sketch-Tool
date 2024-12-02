import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Function to apply pencil sketch filter
def pencil_sketch_filter(img, blur_ksize=21, scale=256):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_image = 255 - gray_image
    blurred = cv2.GaussianBlur(inverted_image, (blur_ksize, blur_ksize), 0)
    inverted_blurred = 255 - blurred
    sketch = cv2.divide(gray_image, inverted_blurred, scale=scale)
    return sketch

# Function to apply charcoal filter
def charcoal_filter(img, intensity=1.5):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 50, 150)
    blurred = cv2.GaussianBlur(edges, (5, 5), 0)
    charcoal = cv2.addWeighted(gray_image, 1, blurred, intensity, 0)
    return charcoal

# Function to apply colored pencil effect
def colored_pencil_filter(img, ksize=5):
    bilateral = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
    edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    colored_sketch = cv2.bitwise_and(bilateral, edges_colored)
    return colored_sketch

# Streamlit App UI
st.title("Image to Pencil Sketch Tool")
st.write("Upload an image and apply different sketch filters!")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    img = np.array(Image.open(uploaded_file))
    st.image(img, caption="Original Image", use_column_width=True)

    # Filter selection
    filter_type = st.sidebar.selectbox(
        "Select a filter",
        ("Pencil Sketch", "Charcoal", "Colored Pencil")
    )

    # Apply the selected filter
    if filter_type == "Pencil Sketch":
        blur_ksize = st.sidebar.slider("Blur Kernel Size", 1, 51, 21, 2)
        scale = st.sidebar.slider("Scale", 100, 300, 256, 10)
        result = pencil_sketch_filter(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), blur_ksize, scale)
        cmap = 'gray'
    elif filter_type == "Charcoal":
        intensity = st.sidebar.slider("Intensity", 0.5, 3.0, 1.5, 0.1)
        result = charcoal_filter(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), intensity)
        cmap = 'gray'
    elif filter_type == "Colored Pencil":
        ksize = st.sidebar.slider("Edge Thickness", 1, 11, 5, 2)
        result = colored_pencil_filter(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), ksize)
        cmap = None

    # Show the filtered image
    st.image(result, caption=f"{filter_type} Effect", use_column_width=True, channels="RGB" if cmap is None else "GRAY")

    # Download filtered image
    result_image = Image.fromarray(result if cmap is None else cv2.cvtColor(result, cv2.COLOR_GRAY2RGB))
    result_image.save("filtered_image.png")
    st.download_button(
        label="Download Filtered Image",
        data=open("filtered_image.png", "rb"),
        file_name="filtered_image.png",
        mime="image/png"
    )
    
