import streamlit as st
from PIL import Image, ImageOps
from rembg import remove
import io

# --- Set page config ---
st.set_page_config(page_title="Image Background Remover", layout="centered")

# --- Title and styling ---
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: gray;
    }
    </style>
    <div class="main-title">Image Background Remover</div>
""", unsafe_allow_html=True)

# --- Upload image ---
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")

    # --- Remove background ---
    with st.spinner("Removing background..."):
        output = remove(image)

    st.subheader("Preview")
    st.image(output, caption="Background Removed", use_column_width=True)

    # --- Options ---
    st.subheader("Edit Options")
    color_mode = st.radio("Color Mode", ["Color", "Black & White"], horizontal=True)

    if color_mode == "Black & White":
        output = ImageOps.grayscale(output).convert("RGBA")

    # --- Download format ---
    format = st.selectbox("Download Format", ["PNG", "JPG", "WEBP"])
    output_buffer = io.BytesIO()

    if format == "JPG":
        output = output.convert("RGB")
        output.save(output_buffer, format="JPEG")
    else:
        output.save(output_buffer, format=format)

    st.download_button(
        label=f" Download as {format}",
        data=output_buffer.getvalue(),
        file_name=f"edited_image.{format.lower()}",
        mime=f"image/{format.lower()}"
    )

# --- Footer ---
st.markdown('<div class="footer">Made by <b>Anand Mohan A M</b></div>', unsafe_allow_html=True)
