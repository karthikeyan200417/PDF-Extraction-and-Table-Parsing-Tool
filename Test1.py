import os
import json
import pdfplumber
import streamlit as st
import tempfile
def extract_pdf_content(pdf_file):
    # Initialize PDF content dictionary
    pdf_data = {
        "headers": [],
        "list_items": [],
        "images": []
    }

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read()) 
        tmp_pdf_path = tmp_file.name
    with pdfplumber.open(tmp_pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            # Extract text from each page
            text = page.extract_text()
            if text:
                pdf_data["headers"].append({
                    "page_number": page_number + 1,
                    "text": text.strip().split("\n")[0]  
                })

                pdf_data["list_items"].append({
                    "page_number": page_number + 1,
                    "text": text.strip().split("\n")[1:]
                })

            tables = page.extract_tables()
            for table in tables:
                pdf_data["list_items"].append({
                    "page_number": page_number + 1,
                    "table_data": table 
                })

    os.remove(tmp_pdf_path)
    
    return pdf_data

def save_to_json(data):
    output_dir = "output" 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_json = os.path.join(output_dir, "extracted_pdf_data.json")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return output_json

def download_file(file_path):
    with open(file_path, 'rb') as file:
        st.download_button(
            label="Download Extracted Data",
            data=file,
            file_name="extracted_pdf_data.json",
            mime="application/json"
        )

def main():
    st.title("PDF Text and Table Extraction")

    uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_pdf is not None:
        extracted_data = extract_pdf_content(uploaded_pdf)
        
        output_json = save_to_json(extracted_data)
        
        st.success(f"Extraction complete. Data saved to {output_json}")
        
        with open(output_json, 'r') as f:
            json_data = json.load(f)
            st.json(json_data)  
        
        download_file(output_json)

if __name__ == "__main__":
    main()
