METHODS = [
    "1. Image Negative",
    "2. Gamma Correction",
    "3. Logarithmic Transformation",
    "4. Contrast Stretching",
    "5. Histogram Equalization",
    "6. Intensity Level Slicing",
    "7. Bit Plane Slicing",
]


METHOD_CAPTIONS = {
    "1. Image Negative": "Image Negative: s = 255 - r",
    "2. Gamma Correction": "Gamma Correction: s = c x (r/255)^g x 255",
    "3. Logarithmic Transformation": "Logarithmic Transform: s = c x log(1 + r)",
    "4. Contrast Stretching": "Contrast Stretching: s = ((r - r_min) / (r_max - r_min)) x 255",
    "5. Histogram Equalization": "Histogram Equalization: Contrast enhancement using CDF-based remapping",
    "6. Intensity Level Slicing": "Intensity Slicing: Highlight intensities within [min, max] range",
    "7. Bit Plane Slicing": "Bit Plane Slicing: plane = (pixel >> bit_plane) & 1",
}
