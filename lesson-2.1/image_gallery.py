import os
import streamlit as st
import base64
from PIL import Image
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Image Gallery App",
    page_icon="🖼️",
    layout="centered"
)

# Create a function to load and display images from a folder


def load_images(folder_path):
    """
    Load all images from the specified folder
    """
    images = []
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

    # Check if the folder exists
    if not os.path.exists(folder_path):
        return images

    # Get all files from the folder
    files = os.listdir(folder_path)

    # Filter image files
    for file in files:
        file_path = os.path.join(folder_path, file)
        file_ext = os.path.splitext(file)[1].lower()

        if os.path.isfile(file_path) and file_ext in valid_extensions:
            try:
                img = Image.open(file_path)
                images.append({
                    "name": file,
                    "path": file_path,
                    "image": img
                })
            except Exception as e:
                st.error(f"Error loading image {file}: {str(e)}")

    return images

# Function to get file download link


def get_image_download_link(img_path, file_name):
    """
    Generate a link to download the image
    """
    with open(img_path, "rb") as file:
        img_bytes = file.read()

    b64 = base64.b64encode(img_bytes).decode()
    # Get extension without the dot
    img_ext = os.path.splitext(file_name)[1][1:]
    href = f'<a href="data:image/{img_ext};base64,{b64}" download="{file_name}">Download {file_name}</a>'
    return href


# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1E88E5;
    margin-bottom: 1rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #424242;
    margin-bottom: 1rem;
}
.info-text {
    font-size: 1.1rem;
    color: #424242;
    margin-bottom: 1.5rem;
}
.success-box {
    background-color: #E3F2FD;
    border-left: 5px solid #1E88E5;
    padding: 1rem;
    border-radius: 5px;
    margin-bottom: 1rem;
}
.gallery-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
}
.image-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    margin: 10px;
    width: 300px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.image-title {
    font-weight: bold;
    text-align: center;
    padding: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<h1 class='main-header'>Image Gallery</h1>",
            unsafe_allow_html=True)
st.markdown("<p class='info-text'>Browse and view images from your collection.</p>",
            unsafe_allow_html=True)

# Set the path to the my_images folder
images_folder = os.path.join(os.path.dirname(__file__), "my_images")
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Upload section
st.markdown("<h2 class='sub-header'>Upload New Images</h2>",
            unsafe_allow_html=True)

uploaded_files = st.file_uploader("Choose image files", accept_multiple_files=True, type=[
                                  "jpg", "jpeg", "png", "gif", "bmp"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(images_folder, uploaded_file.name)

        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Saved: {uploaded_file.name}")

# View options
st.markdown("<h2 class='sub-header'>View Gallery</h2>", unsafe_allow_html=True)

view_options = ["Grid View", "Slideshow", "Detail View"]
view_mode = st.radio("Select view mode:", view_options)

# Load images
images = load_images(images_folder)

# Sort images by name
images.sort(key=lambda x: x["name"])

# Display number of images found
if images:
    st.markdown(f"<p>Found {len(images)} images</p>", unsafe_allow_html=True)
else:
    st.info("No images found in the gallery. Please upload some images.")

# Display images based on selected view mode
if images:
    if view_mode == "Grid View":
        # Display images in a grid using columns
        cols = st.columns(3)
        for i, img_data in enumerate(images):
            with cols[i % 3]:
                st.image(
                    img_data["image"], caption=img_data["name"], use_container_width=True)
                st.markdown(get_image_download_link(
                    img_data["path"], img_data["name"]), unsafe_allow_html=True)

    elif view_mode == "Slideshow":
        # Display images as a slideshow
        selected_index = st.slider("Select image", 0, len(images) - 1, 0)
        selected_image = images[selected_index]

        st.subheader(selected_image["name"])
        st.image(selected_image["image"], use_container_width=True)
        st.markdown(get_image_download_link(
            selected_image["path"], selected_image["name"]), unsafe_allow_html=True)

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous") and selected_index > 0:
                st.session_state["selected_index"] = selected_index - 1
                st.rerun()

        with col2:
            if st.button("Next") and selected_index < len(images) - 1:
                st.session_state["selected_index"] = selected_index + 1
                st.rerun()

    elif view_mode == "Detail View":
        # Display one image at a time with details
        image_names = [img["name"] for img in images]
        selected_image_name = st.selectbox(
            "Select an image to view", image_names)

        # Find the selected image
        selected_image = next(
            (img for img in images if img["name"] == selected_image_name), None)

        if selected_image:
            st.subheader(selected_image["name"])
            st.image(selected_image["image"], use_container_width=True)

            # Display image details
            file_stats = os.stat(selected_image["path"])
            image_size = selected_image["image"].size

            st.markdown("### Image Details")
            st.markdown(f"**Filename:** {selected_image['name']}")
            st.markdown(
                f"**Dimensions:** {image_size[0]} x {image_size[1]} pixels")
            st.markdown(f"**File Size:** {file_stats.st_size / 1024:.2f} KB")
            st.markdown(f"**Format:** {selected_image['image'].format}")
            st.markdown(f"**Mode:** {selected_image['image'].mode}")

            st.markdown(get_image_download_link(
                selected_image["path"], selected_image["name"]), unsafe_allow_html=True)

# Image management
st.markdown("<h2 class='sub-header'>Image Management</h2>",
            unsafe_allow_html=True)

if images:
    delete_options = ["None"] + [img["name"] for img in images]
    delete_image = st.selectbox("Select image to delete", delete_options)

    if delete_image != "None" and st.button("Delete Selected Image"):
        try:
            delete_path = os.path.join(images_folder, delete_image)
            if os.path.exists(delete_path):
                os.remove(delete_path)
                st.success(f"Deleted: {delete_image}")
                st.rerun()
            else:
                st.error("Image file not found.")
        except Exception as e:
            st.error(f"Error deleting image: {str(e)}")

# Instructions
with st.expander("How to use this app"):
    st.markdown("""
    1. Upload images using the file uploader at the top of the page
    2. View your images in different modes:
       - Grid View: See all images in a grid layout
       - Slideshow: Navigate through images one at a time
       - Detail View: View detailed information about each image
    3. Download any image by clicking its download link
    4. Delete unwanted images using the Image Management section
    """)

# Display app information in sidebar
with st.sidebar:
    st.markdown("## About")
    st.markdown(
        "This app allows you to create and manage your own image gallery.")
    st.markdown("### Features")
    st.markdown("- Upload multiple images")
    st.markdown("- View images in different layouts")
    st.markdown("- Download images")
    st.markdown("- Delete unwanted images")

    # Show folder location
    st.markdown("## Gallery Location")
    st.code(images_folder)

    # Add import demo images button
    st.markdown("## Demo Images")
    if st.button("Add Demo Images"):
        # Create demo images folder if it doesn't exist
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        # Create a simple demo image using PIL
        for i in range(1, 4):
            img = Image.new('RGB', (300, 200), color=(
                64*i, 100+20*i, 200-30*i))
            img_path = os.path.join(images_folder, f"demo_image_{i}.png")
            img.save(img_path)

        st.success("Demo images added to gallery!")
        st.rerun()

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")
