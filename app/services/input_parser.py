# input_parser.py
import logging
import fitz

logger = logging.getLogger('input_parser')

def extract_text(pdf_bytes: bytes) -> str:
    """
    Extracts text from a PDF byte stream.

    Args:
        pdf_bytes (bytes): The byte content of a PDF file.

    Returns:
        str: Extracted text from all pages.
    """
    text = ""
    if pdf_bytes[:4] == b'%PDF':
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text")
    logger.debug("Resume parse completed")
    return text.strip()

