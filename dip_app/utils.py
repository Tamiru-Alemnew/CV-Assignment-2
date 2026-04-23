import cv2
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def plot_histogram(image: np.ndarray, title: str = "Histogram"):
    fig, ax = plt.subplots(figsize=(5, 3))

    if image is None or image.size == 0:
        ax.set_title(title)
        ax.set_xlabel("Pixel Intensity")
        ax.set_ylabel("Frequency")
        ax.text(0.5, 0.5, "No image data", ha="center", va="center", transform=ax.transAxes)
        plt.tight_layout()
        return fig

    if image.ndim == 2:
        ax.hist(image.ravel(), bins=256, range=[0, 256], color="gray", alpha=0.7)
    else:
        colors = ["red", "green", "blue"]
        labels = ["Red", "Green", "Blue"]
        for channel_idx in range(3):
            ax.hist(
                image[:, :, channel_idx].ravel(),
                bins=256,
                range=[0, 256],
                color=colors[channel_idx],
                alpha=0.4,
                label=labels[channel_idx],
            )
        ax.legend()

    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Frequency")
    ax.set_title(title)
    plt.tight_layout()
    return fig


def display_image_info(image: np.ndarray, label: str) -> None:
    if image is None:
        st.text(f"{label} info unavailable.")
        return

    image_shape = image.shape
    image_dtype = image.dtype
    min_pixel_value = int(np.min(image))
    max_pixel_value = int(np.max(image))
    if image.ndim == 2:
        channel_count = 1
        image_mode = "Grayscale"
    else:
        channel_count = image.shape[2]
        image_mode = "RGB" if channel_count == 3 else f"{channel_count}-channel"

    info_text = (
        f"{label} Info\n"
        f"Shape: {image_shape}\n"
        f"Data type: {image_dtype}\n"
        f"Min pixel value: {min_pixel_value}\n"
        f"Max pixel value: {max_pixel_value}\n"
        f"Number of channels: {channel_count}\n"
        f"Mode: {image_mode}"
    )
    st.text(info_text)


def is_effectively_grayscale(rgb_image: np.ndarray) -> bool:
    if rgb_image is None or rgb_image.ndim != 3 or rgb_image.shape[2] != 3:
        return False
    return np.array_equal(rgb_image[:, :, 0], rgb_image[:, :, 1]) and np.array_equal(
        rgb_image[:, :, 1], rgb_image[:, :, 2]
    )


def load_uploaded_image(uploaded_file) -> np.ndarray | None:
    try:
        file_bytes = uploaded_file.read()
        if not file_bytes:
            st.error("Uploaded file is empty. Please try another image.")
            return None
        np_buffer = np.frombuffer(file_bytes, np.uint8)
        decoded_bgr = cv2.imdecode(np_buffer, cv2.IMREAD_COLOR)
        if decoded_bgr is None:
            st.error("Could not decode the uploaded image. The file may be corrupted.")
            return None
        return cv2.cvtColor(decoded_bgr, cv2.COLOR_BGR2RGB)
    except Exception as error:
        st.error(f"Failed to read image: {error}")
        return None


def image_to_png_bytes(image: np.ndarray) -> bytes | None:
    if image is None:
        return None
    if image.ndim == 2:
        success, encoded = cv2.imencode(".png", image)
    else:
        success, encoded = cv2.imencode(".png", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    if not success:
        return None
    return encoded.tobytes()
