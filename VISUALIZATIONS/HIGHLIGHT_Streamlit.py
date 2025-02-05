import streamlit as st
import os
import pandas as pd
from PIL import Image
import ast

def load_image(image_path):
    try:
        return Image.open(image_path)
    except:
        return None

def count_failed_folders(root_folder):
    failed_folders = 0
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        if os.path.isdir(folder_path):
            csv_path = os.path.join(folder_path, "citations.csv")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                if not df.empty and df['response'].iloc[0] == "Error infering LLM":
                    failed_folders += 1
    return failed_folders

def get_valid_folders(root_folder):
    valid_folders = []
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        if os.path.isdir(folder_path):
            csv_path = os.path.join(folder_path, "citations.csv")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                if not df.empty and df['response'].iloc[0] != "Error infering LLM":
                    valid_folders.append(folder)
    return valid_folders

def main():
    st.set_page_config(layout="wide")

    root_folder = "./../outputs"
    folders = sorted(get_valid_folders(root_folder))

    failed_folders_count = count_failed_folders(root_folder)
    st.write(f"Number of images that failed LLM inference: {failed_folders_count}")

    st.sidebar.title("Folder Selection")
    
    if 'folder_index' not in st.session_state:
        st.session_state.folder_index = 0

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.folder_index = max(0, st.session_state.folder_index - 1)
    with col2:
        if st.button("Next"):
            st.session_state.folder_index = min(len(folders) - 1, st.session_state.folder_index + 1)

    selected_folder = st.sidebar.selectbox("Choose a folder", folders, index=st.session_state.folder_index, key='folder_select')
    st.session_state.folder_index = folders.index(selected_folder)

    st.title(f"Folder: {selected_folder}")

    folder_path = os.path.join(root_folder, selected_folder)

    input_image = load_image(os.path.join(folder_path, "input.png"))
    citation_highlighted = load_image(os.path.join(folder_path, "citation_highlighted.png"))
    debug_sections = load_image(os.path.join(folder_path, "debug_sections.png"))
    highlighted_merged = load_image(os.path.join(folder_path, "merged_highlighted.png"))

    csv_path = os.path.join(folder_path, "citations.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=['question', 'accepted_answer', 'response', 'citations', 'citation_matches'])

    unprocessed_text = ""
    processed_text = ""
    try:
        with open(os.path.join(folder_path, "unprocessed_text.txt"), "r") as f:
            unprocessed_text = f.read()
    except FileNotFoundError:
        unprocessed_text = "File not found"

    try:
        with open(os.path.join(folder_path, "processed_text.txt"), "r") as f:
            processed_text = f.read()
    except FileNotFoundError:
        processed_text = "File not found"

    col1, col2 = st.columns(2)
    with col1:
        st.image(input_image, caption="Input Image", use_column_width=True)
    with col2:
        st.image(citation_highlighted, caption="Citation Highlighted", use_column_width=True)

    st.subheader("Question and Answer")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Question", df['question'].iloc[0] if not df.empty else "", height=200)
    with col2:
        st.text_area("Accepted Answer", df['accepted_answer'].iloc[0] if not df.empty else "", height=200)
    
    st.text_area("Response", df['response'].iloc[0] if not df.empty else "", height=150)
    
    st.subheader("Citations and Matches")
    if not df.empty and 'citations' in df.columns and 'citation_matches' in df.columns:
        citations = ast.literal_eval(df['citations'].iloc[0])
        citation_matches = ast.literal_eval(df['citation_matches'].iloc[0])
        
        citation_data = []
        for citation, match in zip(citations, citation_matches):
            citation_data.append({
                "Citation": citation,
                "Match Text": match['match_text'],
                "Similarity": match['similarity']
            })
        
        citation_df = pd.DataFrame(citation_data)
        st.table(citation_df)
    else:
        st.write("No citations or matches available")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.image(debug_sections, caption="Debug Sections", use_column_width=True)
    with col2:
        st.image(highlighted_merged, caption="Highlighted Merged", use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Unprocessed Text")
        st.text_area("", unprocessed_text, height=300)
    with col2:
        st.subheader("Processed Text")
        st.text_area("", processed_text, height=300)

if __name__ == "__main__":
    main()