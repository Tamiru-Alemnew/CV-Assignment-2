import matplotlib.pyplot as plt
import streamlit as st
import cv2

from .constants import METHOD_CAPTIONS, METHODS
from .transforms import process_image
from .utils import (
    display_image_info,
    image_to_png_bytes,
    is_effectively_grayscale,
    load_uploaded_image,
    plot_histogram,
)


def run_app() -> None:
    st.set_page_config(
        page_title="Digital Image Processing - Elementary Methods",
        page_icon="🖼️",
        layout="wide",
    )

    st.title("Digital Image Processing: Elementary Methods")
    st.write(
        "Upload an image and apply various point processing techniques. "
        "Supports both RGB and Grayscale images."
    )

    st.sidebar.header("Controls")
    uploaded_file = st.sidebar.file_uploader(
        "Upload an Image",
        type=["png", "jpg", "jpeg", "bmp", "tiff"],
    )
    if uploaded_file is None:
        st.info("Please upload an image using the sidebar to get started.")
        return

    uploaded_image_rgb = load_uploaded_image(uploaded_file)
    if uploaded_image_rgb is None:
        return

    convert_to_grayscale = st.sidebar.checkbox("Convert to Grayscale", value=False)
    image_is_effectively_grayscale = is_effectively_grayscale(uploaded_image_rgb)
    if convert_to_grayscale:
        working_image = cv2.cvtColor(uploaded_image_rgb, cv2.COLOR_RGB2GRAY)
        image_mode_label = "grayscale"
    else:
        working_image = uploaded_image_rgb
        image_mode_label = "grayscale" if image_is_effectively_grayscale else "rgb"

    st.session_state["original_image_rgb"] = uploaded_image_rgb
    st.session_state["working_image"] = working_image
    st.session_state["image_mode"] = image_mode_label

    selected_method = st.sidebar.selectbox("Select Method", METHODS)
    processing_params = {}
    if selected_method == "2. Gamma Correction":
        gamma_value = st.sidebar.slider("Gamma Value (γ)", 0.1, 5.0, 1.0, 0.1)
        st.sidebar.info("γ < 1.0 → Brightens image | γ = 1.0 → No change | γ > 1.0 → Darkens image")
        processing_params["gamma"] = gamma_value
    elif selected_method == "6. Intensity Level Slicing":
        min_intensity = st.sidebar.slider("Min Intensity", 0, 255, 100)
        max_intensity = st.sidebar.slider("Max Intensity", 0, 255, 200)
        preserve_background = st.sidebar.checkbox("Preserve Background", value=True)
        if min_intensity > max_intensity:
            st.sidebar.warning("Min Intensity was greater than Max Intensity. Values were swapped.")
            min_intensity, max_intensity = max_intensity, min_intensity
        processing_params["min_val"] = min_intensity
        processing_params["max_val"] = max_intensity
        processing_params["preserve_bg"] = preserve_background
    elif selected_method == "7. Bit Plane Slicing":
        bit_plane = st.sidebar.slider("Bit Plane (0=LSB, 7=MSB)", 0, 7, 7, 1)
        st.sidebar.info("Higher bit planes (7,6,5) carry structural info. Lower planes (0,1,2) carry noise/fine detail.")
        processing_params["bit_plane"] = bit_plane

    processed_image = process_image(working_image, selected_method, **processing_params)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📷 Original Image")
        if working_image.ndim == 2:
            st.image(working_image, use_container_width=True, clamp=True, channels="GRAY")
        else:
            st.image(working_image, use_container_width=True)
        fig_orig = plot_histogram(working_image, "Original Histogram")
        st.pyplot(fig_orig)
        plt.close(fig_orig)
        display_image_info(working_image, "Original Image")

    with col2:
        st.subheader("🔧 Processed Image")
        st.write("Select a method to process")
        if processed_image is None:
            st.info("Method not yet implemented. Coming in Phase 2/3.")
            st.caption(METHOD_CAPTIONS.get(selected_method, ""))
            return

        if processed_image.ndim == 2:
            st.image(processed_image, use_container_width=True, clamp=True, channels="GRAY")
        else:
            st.image(processed_image, use_container_width=True)
        fig_proc = plot_histogram(processed_image, "Processed Histogram")
        st.pyplot(fig_proc)
        plt.close(fig_proc)
        if selected_method == "7. Bit Plane Slicing":
            st.caption("Binary image: only 0 and 255 values")
        st.caption(METHOD_CAPTIONS.get(selected_method, ""))
        display_image_info(processed_image, "Processed Image")
        png_bytes = image_to_png_bytes(processed_image)
        if png_bytes is not None:
            st.download_button(
                "Download Processed Image",
                data=png_bytes,
                file_name="processed.png",
                mime="image/png",
            )
        else:
            st.warning("Could not prepare image for download.")
