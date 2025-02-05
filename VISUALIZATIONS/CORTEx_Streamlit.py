import os
import pandas as pd
import streamlit as st
from PIL import Image
import math
import base64
import io

# Set page config
st.set_page_config(page_title="Image and Text Viewer", layout="wide")

output_dir = './../outputs'

def get_folders_and_files():
    def get_folders():
        return [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]

    folders = get_folders()
    files_df = pd.DataFrame(columns=['folder', 'files'])

    for i, folder in enumerate(folders):
        files_in_folder = [
                'unprocessed_text.txt', 
                'input.png', 
                'debug_sections.png', 
                'highlighted.png', 
                'merged_highlighted.png', 
                'removed.png', 
                'merged_removed.png', 
                'line_numbers.png', 
                'detected_vertical_lines.png', 
                'detected_horizontal_lines.png', 
                'processed_text.txt', 
                'processed_text_tabs.txt', 
                'processed_text_ascii.txt', 
                'citations.csv', 
                'citation_highlighted.png' 
            ]
        files_df.loc[i] = [folder, files_in_folder]

    # Cast as int the 'folder' column
    # files_df['folder'] = files_df['folder'].astype(int)
    # Sort the dataframe by the 'folder' column
    files_df = files_df.sort_values('folder').reset_index(drop=True)
    # Cast the 'folder' column back to string
    # files_df['folder'] = files_df['folder'].astype(str)

    return files_df

# @st.cache_data
def load_image(image_path):
    return Image.open(image_path)

def format_file_name(file_name):
    name_without_extension = os.path.splitext(file_name)[0]
    name_without_path = os.path.basename(name_without_extension)
    name_without_underscores = name_without_path.replace('_', ' ')
    return name_without_underscores.capitalize()

def get_image_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def update_folder_index(direction):
    if direction == "next":
        st.session_state.folder_index = min(len(st.session_state.files_df) - 1, st.session_state.folder_index + 1)
    elif direction == "previous":
        st.session_state.folder_index = max(0, st.session_state.folder_index - 1)

def main():
    st.title("Image and Text Viewer")

    if 'files_df' not in st.session_state:
        st.session_state.files_df = get_folders_and_files()

    if 'folder_index' not in st.session_state:
        st.session_state.folder_index = 0

    files_df = st.session_state.files_df

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        scol1, scol2 = st.columns(2)
        with scol1:
            st.button("← Previous", on_click=update_folder_index, args=("previous",))
        with scol2:
            st.button("Next →", on_click=update_folder_index, args=("next",))
    with col2:
        search_col, dropdown_col = st.columns(2)
        with search_col:
            search_id = st.text_input("Search ID", key="search_id")
            if search_id:
                matching_folders = files_df[files_df['folder'].str.contains(search_id, case=False)]
                if not matching_folders.empty:
                    st.session_state.folder_index = files_df.index[files_df['folder'] == matching_folders.iloc[0]['folder']].tolist()[0]
                else:
                    st.warning("No matching ID found.")
        with dropdown_col:
            folder_names = files_df['folder'].tolist()
            selected_folder = st.selectbox("Select Folder", folder_names, index=st.session_state.folder_index, key='folder_select')
            st.session_state.folder_index = folder_names.index(selected_folder)
    with col3:
        images_per_row = st.slider("Images per row", min_value=1, max_value=5, value=2)

    current_folder = files_df.iloc[st.session_state.folder_index]
    images = [file for file in current_folder['files'] if file.endswith('.png')]
    text_files = [file for file in current_folder['files'] if file.endswith('.txt')]

    img_height = 400

    # Display images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(format_file_name(images[0]))
        img1 = load_image(os.path.join(output_dir, current_folder['folder'], images[0]))
        factor = img_height / img1.height
        img1 = img1.resize((int(img1.width * factor), int(img1.height * factor)))
        st.image(img1)
    with col2:
        st.subheader(format_file_name(images[1]))
        img2 = load_image(os.path.join(output_dir, current_folder['folder'], images[1]))
        factor = img_height / img2.height
        img2 = img2.resize((int(img2.width * factor), int(img2.height * factor)))
        st.image(img2)

    # Display text areas below images
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(format_file_name(text_files[0]))
        text_path = os.path.join(output_dir, current_folder['folder'], text_files[0])
        with open(text_path, 'r') as file:
            content = file.read()
        st.text_area("", content, height=img_height)

    with col2:
        # Create a dropdown menu for selecting text files for the second image
        section_text_files = [f for f in text_files if f != text_files[0]]
        selected_text_file = st.selectbox("Select text file for the second image", section_text_files, index=0)
        
        st.subheader(format_file_name(selected_text_file))
        text_path = os.path.join(output_dir, current_folder['folder'], selected_text_file)
        with open(text_path, 'r') as file:
            content = file.read()
        st.text_area("", content, height=img_height)

    # Display remaining images
    remaining_images = images[2:]
    num_remaining = len(remaining_images)
    rows = math.ceil(num_remaining / images_per_row)

    for row in range(rows):
        cols = st.columns(images_per_row)
        for col in range(images_per_row):
            idx = row * images_per_row + col
            if idx < num_remaining:
                image_file = remaining_images[idx]
                image_path = os.path.join(output_dir, current_folder['folder'], image_file)
                img = load_image(image_path)
                cols[col].subheader(format_file_name(image_file))
                cols[col].image(img, use_column_width=True)

if __name__ == "__main__":
    main()

