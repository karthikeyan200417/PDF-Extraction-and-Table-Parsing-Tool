import os
import json
import pdfplumber
import streamlit as st
import tempfile

# Function to extract content from the PDF using pdfplumber
def extract_pdf_content(pdf_file):
    # Initialize PDF content dictionary
    pdf_data = {
        "headers": [],
        "list_items": [],
        "images": []
    }

    # Use a temporary file to save the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())  # Save the uploaded file to the temporary file
        tmp_pdf_path = tmp_file.name

    # Read the PDF using pdfplumber
    with pdfplumber.open(tmp_pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            # Extract text from each page
            text = page.extract_text()
            if text:
                pdf_data["headers"].append({
                    "page_number": page_number + 1,
                    "text": text.strip().split("\n")[0]  # First line is treated as header
                })

                # Extract remaining text as list items
                pdf_data["list_items"].append({
                    "page_number": page_number + 1,
                    "text": text.strip().split("\n")[1:]
                })

            # Extract tables using pdfplumber
            tables = page.extract_tables()
            for table in tables:
                pdf_data["list_items"].append({
                    "page_number": page_number + 1,
                    "table_data": table  # Store table data as a list of lists
                })

    # Clean up the temporary file after processing
    os.remove(tmp_pdf_path)
    
    return pdf_data

# Function to save the extracted data to a JSON file
def save_to_json(data):
    output_dir = "output"  # Folder where JSON will be saved
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_json = os.path.join(output_dir, "extracted_pdf_data.json")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return output_json

# Function to allow the user to download the extracted JSON file
def download_file(file_path):
    with open(file_path, 'rb') as file:
        st.download_button(
            label="Download Extracted Data",
            data=file,
            file_name="extracted_pdf_data.json",
            mime="application/json"
        )

# Streamlit app for file upload
def main():
    st.title("PDF Text and Table Extraction")

    # File uploader widget
    uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_pdf is not None:
        # Read PDF file from the uploaded file
        extracted_data = extract_pdf_content(uploaded_pdf)
        
        # Save extracted data to JSON file
        output_json = save_to_json(extracted_data)
        
        st.success(f"Extraction complete. Data saved to {output_json}")
        
        # Display JSON data in Streamlit
        with open(output_json, 'r') as f:
            json_data = json.load(f)
            st.json(json_data)  # Display the JSON content in a formatted way
        
        # Provide the option to download the JSON file
        download_file(output_json)

if __name__ == "__main__":
    main()
