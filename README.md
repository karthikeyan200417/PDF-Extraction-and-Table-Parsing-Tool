# PDF Extraction and Table Parsing Tool

This project provides a Python-based tool to extract text and table data from PDF files. The extracted content is organized into a structured JSON format and made available for download. It uses `Streamlit` for the interface, and libraries like `PyPDF2` and `Camelot` for text and table extraction.

---

## Features

- **Upload PDFs**: Upload a PDF file to the app.
- **Extract Content**: Extract both textual content and tabular data from the uploaded PDF.
- **Organized JSON Output**: The extracted data is formatted into a JSON structure:
  - Text from pages as headers.
  - Tables as structured data in a `list_items` section.
- **Download Results**: The extracted JSON can be downloaded for further use.

---

## Installation

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8 or above
- pip (Python package manager)
- Java (required for `Camelot`)

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/karthikeyan200417/PDF-Extraction-and-Table-Parsing-Tool.git
   cd pdf-extraction-tool
2.**Create a virtual environment**:
python -m venv venv
source venv/bin/activate  
3.**Install dependencies**:
pip install -r requirements.txt
4.**Run the application**:
streamlit run Test1.py


