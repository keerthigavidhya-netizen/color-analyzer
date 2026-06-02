import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Color Distribution Analyzer")

st.title("🎨 Color Distribution Analyzer")

st.write(
    "Upload an image and get percentage distribution of colors."
)

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

COLOR_CATEGORIES = [
    "White",
    "Black",
    "Red",
    "Green",
    "Yellow",
    "Blue",
    "Brown",
    "Purple",
    "Pink",
    "Orange",
    "Gray"
]

def classify_color(h, s, v):

    if v < 50:
        return "Black"

    if s < 30:
        if v > 200:
            return "White"
        return "Gray"

    if 0 <= h <= 10 or 170 <= h <= 180:
        return "Red"

    if 11 <= h <= 20:
        if v < 180:
            return "Brown"
        return "Orange"

    if 21 <= h <= 30:
        return "Orange"

    if 31 <= h <= 40:
        return "Yellow"

    if 41 <= h <= 85:
        return "Green"

    if 86 <= h <= 130:
        return "Blue"

    if 131 <= h <= 150:
        return "Purple"

    if 151 <= h <= 169:
        return "Pink"

    return "Gray"


if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    img = np.array(image)

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    counts = {color: 0 for color in COLOR_CATEGORIES}

    pixels = hsv.reshape(-1, 3)

    for pixel in pixels:

        h, s, v = pixel

        category = classify_color(h, s, v)

        counts[category] += 1

    total_pixels = len(pixels)

    percentages = {}

    for color, count in counts.items():

        percent = (count / total_pixels) * 100

        if percent > 0:
            percentages[color] = round(percent, 2)

    st.subheader("Color Percentage Distribution")

    st.dataframe(
        {
            "Color": list(percentages.keys()),
            "Percentage": list(percentages.values())
        }
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        percentages.values(),
        labels=percentages.keys(),
        autopct="%1.1f%%"
    )

    ax.set_title("Color Distribution")

    st.pyplot(fig)
