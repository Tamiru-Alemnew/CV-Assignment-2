import cv2
import numpy as np


def apply_negative(image: np.ndarray) -> np.ndarray:
    if image is None:
        return image
    return (255 - image).astype(np.uint8)


def apply_gamma(image: np.ndarray, gamma: float, c: float = 1.0) -> np.ndarray:
    if image is None:
        return image
    normalized = image.astype(np.float64) / 255.0
    corrected = c * np.power(normalized, gamma)
    corrected = np.clip(corrected, 0.0, 1.0)
    return (corrected * 255).astype(np.uint8)


def apply_log_transform(image: np.ndarray) -> np.ndarray:
    if image is None:
        return image
    img_float = image.astype(np.float64)
    max_value = float(np.max(img_float))
    if max_value == 0.0:
        return image.astype(np.uint8)
    c = 255.0 / np.log(1.0 + max_value)
    output = c * np.log(1.0 + img_float)
    return np.clip(output, 0, 255).astype(np.uint8)


def apply_contrast_stretching(image: np.ndarray) -> np.ndarray:
    if image is None or image.size == 0:
        return image

    if image.ndim == 2:
        image_float = image.astype(np.float64)
        r_min = np.min(image_float)
        r_max = np.max(image_float)
        if r_min == r_max:
            return image.astype(np.uint8)
        stretched = ((image_float - r_min) / (r_max - r_min)) * 255.0
        return np.clip(stretched, 0, 255).astype(np.uint8)

    stretched_rgb = np.zeros_like(image, dtype=np.float64)
    for channel_idx in range(image.shape[2]):
        channel = image[:, :, channel_idx].astype(np.float64)
        r_min = np.min(channel)
        r_max = np.max(channel)
        if r_min == r_max:
            stretched_rgb[:, :, channel_idx] = channel
        else:
            stretched_rgb[:, :, channel_idx] = ((channel - r_min) / (r_max - r_min)) * 255.0
    return np.clip(stretched_rgb, 0, 255).astype(np.uint8)


def apply_histogram_equalization(image: np.ndarray) -> np.ndarray:
    if image is None or image.size == 0:
        return image

    if image.ndim == 2:
        return cv2.equalizeHist(image.astype(np.uint8))

    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    yuv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    bgr_equalized = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    return cv2.cvtColor(bgr_equalized, cv2.COLOR_BGR2RGB).astype(np.uint8)


def apply_intensity_slicing(
    image: np.ndarray, min_val: int, max_val: int, preserve_background: bool = True
) -> np.ndarray:
    if image is None or image.size == 0:
        return image

    min_val = int(np.clip(min_val, 0, 255))
    max_val = int(np.clip(max_val, 0, 255))

    if image.ndim == 2:
        mask = (image >= min_val) & (image <= max_val)
        if preserve_background:
            output = image.copy()
            output[mask] = 255
        else:
            output = np.zeros_like(image)
            output[mask] = 255
        return output.astype(np.uint8)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    mask = (gray >= min_val) & (gray <= max_val)
    if preserve_background:
        output = image.copy()
        output[mask] = [255, 255, 255]
    else:
        output = np.zeros_like(image)
        output[mask] = image[mask]
    return output.astype(np.uint8)


def apply_bit_plane_slicing(image: np.ndarray, bit_plane: int) -> np.ndarray:
    if image is None or image.size == 0:
        return image

    bit_plane = int(np.clip(bit_plane, 0, 7))
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image
    plane = (gray >> bit_plane) & 1
    return (plane * 255).astype(np.uint8)


def process_image(image: np.ndarray, method: str, **params) -> np.ndarray | None:
    if image is None:
        return None
    if method == "1. Image Negative":
        return apply_negative(image)
    if method == "2. Gamma Correction":
        return apply_gamma(image, params.get("gamma", 1.0))
    if method == "3. Logarithmic Transformation":
        return apply_log_transform(image)
    if method == "4. Contrast Stretching":
        return apply_contrast_stretching(image)
    if method == "5. Histogram Equalization":
        return apply_histogram_equalization(image)
    if method == "6. Intensity Level Slicing":
        return apply_intensity_slicing(
            image,
            params.get("min_val", 100),
            params.get("max_val", 200),
            params.get("preserve_bg", True),
        )
    if method == "7. Bit Plane Slicing":
        return apply_bit_plane_slicing(image, params.get("bit_plane", 7))
    return None
