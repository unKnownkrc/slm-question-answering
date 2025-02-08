import pdfplumber
import os
import re
import unicodedata
from config import BOOK_PATH  # Load from config

# Define extracted text save path dynamically
EXTRACTED_TEXT_PATH = os.path.join(os.path.dirname(BOOK_PATH), "extracted_text_cleaned.txt")

def extract_text(pdf_path, save_path=None, skip_first_n_pages=2):
    """
    Extracts and cleans text from a PDF file using pdfplumber.

    Args:
        pdf_path (str): Path of the PDF file.
        save_path (str, optional): Path to save extracted text. Defaults to None.
        skip_first_n_pages (int): Number of initial pages to skip.

    Returns:
        str: Cleaned extracted text from the PDF.
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        return ""

    extracted_text = []
    current_paragraph = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"📄 PDF Loaded Successfully: {pdf_path}")

            for page_num, page in enumerate(pdf.pages, start=1):
                if page_num <= skip_first_n_pages:
                    continue  # Skip unwanted pages

                text = page.extract_text()
                if not text:
                    continue

                lines = text.split("\n")

                for line in lines:
                    line = unicodedata.normalize("NFKC", line.strip())  # Normalize Unicode
                    line = re.sub(r"\s{2,}", " ", line)  # Remove extra spaces

                    # === Text Cleaning Rules ===
                    if re.match(r"^\d+\s*$", line):  # Skip standalone numbers (page numbers)
                        continue
                    if re.match(r"^\d+\..*", line):  # Skip numbered headings
                        continue  
                    if re.search(r"(PENGUIN BOOKS|Copyright|All rights reserved|References|Appendix|Contents|Preface|Acknowledgements)", 
                                 line, re.IGNORECASE):  # Skip unwanted metadata
                        continue

                    # Fix hyphenated words broken across lines
                    line = re.sub(r"(\w+)[\u00AD-]\n?(\w+)", r"\1\2", line)  
                    line = re.sub(r"(\w+)- (\w+)", r"\1\2", line)  

                    # Handle section titles
                    if re.match(r"^(CHAPTER|SECTION|PART|APPENDIX)", line, re.IGNORECASE):
                        if current_paragraph:
                            extracted_text.append(" ".join(current_paragraph))
                            current_paragraph = []
                        extracted_text.append("\n\n" + line.upper() + "\n")
                        continue

                    # Manage paragraph structure
                    if line.endswith("-"):  
                        current_paragraph.append(line[:-1])  # Remove hyphen, append
                    elif line:  
                        current_paragraph.append(line)
                    else:  
                        if current_paragraph:
                            extracted_text.append(" ".join(current_paragraph))
                            current_paragraph = []  # Reset buffer

            # Append remaining paragraph
            if current_paragraph:
                extracted_text.append(" ".join(current_paragraph))

        print(f"✅ Text Extraction Completed Successfully.")

    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

    final_text = "\n\n".join(extracted_text)

    # Save cleaned text
    if save_path:
        try:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(final_text)
            print(f"📂 Cleaned extracted text saved to: {save_path}")
        except Exception as e:
            print(f"❌ Error saving text to file: {e}")

    return final_text


# ✅ Testing the function
if __name__ == "__main__":
    text = extract_text(BOOK_PATH, EXTRACTED_TEXT_PATH)

    # Print first 1000 characters for verification
    print("\n🔍 Sample Extracted Text (First 1000 characters):\n")
    print(text[:1000])
