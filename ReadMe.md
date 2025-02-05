# CORTEx Project

The final notebooks are `Pipeline_Groq.ipynb`.

## Prerequisites

- Python 3.x
- Google Cloud Vision API credentials
- Groq / OpenAI API key
- Required Python libraries (see `requirements.txt`)

## Setup

1. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - `VERTEXAI_PROJECT_ID`: Your Google Cloud project ID
   - `GROQ_API_KEY`: Your Groq API key
   - `OPENAI_API_KEY`: Your OpenAI API key

3. Prepare input data:
   - CSV file with image metadata (`data_stackoverflow.csv`)
   - Directory of input images

## Input CSV File Fields

The input CSV file (`data_stackoverflow.csv`) should contain:
- `id`: Unique identifier for the Stack Overflow question
- `image_name`: Name of the image file associated with the question
- `body`: The text of the Stack Overflow question
- `accepted_answer_body`: The text of the accepted answer for the question

## Usage

Update the following variables in the code :
- `img_dir`: Path to the directory containing input images
- `output_dir`: Path to the directory for output files

Run the notebook.

## Main Processing Steps

1. OCR and text extraction using Google Cloud Vision API
2. Text cleanup and paragraph merging
3. Line detection (vertical and horizontal) and image sectioning
4. Text formatting and layout preservation
5. Text highlighting based on citations
6. API interaction with Groq/OpenAI for text analysis

## Outputs

For each processed image, the code generates the following outputs in the specified output directory:

1. `unprocessed_text.txt`: Raw OCR text extracted from the image
2. `input.png`: Copy of the original input image
3. `highlighted.png`: Image with bounding boxes around detected text
4. `merged_highlighted.png`: Image with bounding boxes around merged text blocks
5. `removed.png`: Image with text removed
6. `merged_removed.png`: Image with merged text blocks removed
7. `line_numbers.png`: Image highlighting detected line numbers
8. `detected_vertical_lines.png`: Image showing detected vertical lines
9. `detected_horizontal_lines.png`: Image showing detected horizontal lines
10. `debug_sections.png`: Image displaying the created sections
11. `processed_text.txt`: Formatted text preserving layout - ***(Prefered output)***
12. `processed_text_tabs.txt`: Formatted text with relative tabs
13. `processed_text_ascii.txt`: Formatted text with ASCII characters only
14. `citations.csv`: CSV file containing question, answer, model response, and citation information
15. `citation_highlighted.png`: Image with highlighted text based on model citations

## Visualization
In the "VISUALIZATIONS" folder, there are two Streamlit apps to help visualize the results:

- Image Processing Pipeline (CORTEx) Visualization: This app allows you to explore the different stages of the image processing pipeline used to detect sections in the images.
- Citations Showcase: This app demonstrates the citations extracted from the processed text and how they relate to the original questions and answers.

To run these visualization apps, navigate to the "VISUALIZATIONS" folder and use the ``streamlit run`` command followed by the app's filename.

## Limitations & Areas for Improvement
**Text Formatting:** Text positioning (line breaks & tabs) within sections is determined by the mean of the section's characters' height and width. This method can lead to inaccuracies, resulting in unwanted behavior, especially when text of heterogeneous sizes is located in the same section. Enhancing this aspect could lead to better fidelity to the original text presentation, ensuring that layout and formatting are maintained more accurately. 

**Language Dependency:** The current method is tailored for English, as it relies on an English dictionary during a processing step where words are merged based on proximity. This limits its effectiveness with other languages.

**IDE Icons Interference:** Icons in the file explorer of IDEs can sometimes interfere with the detection of vertical lines, potentially impacting the accuracy of text processing. A simple CNN could help mask icons for the line detection.
