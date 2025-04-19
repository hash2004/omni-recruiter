import os
import gdown
from mistralai import Mistral
from pathlib import Path
from mistralai import DocumentURLChunk, ImageURLChunk, TextChunk
import json

def download_drive_folder_gdown(folder_url: str, output_dir: str = "output") -> None:
    """
    Downloads all files from a public Google Drive folder URL into a local directory.

    Args:
        folder_url: The sharable URL of the Google Drive folder
                    (e.g., https://drive.google.com/drive/folders/<folder_id>).
        output_dir: Local directory path to save downloaded files.
    """
    os.makedirs(output_dir, exist_ok=True)
    gdown.download_folder(folder_url, output=output_dir, quiet=False, use_cookies=False)

def concatenate_pdf_markdowns(
    directory: str,
    api_key: str,
    ocr_model: str = "mistral-ocr-latest",
    expiry: int = 1
) -> str:
    """
    Iterates through all PDF files in `directory`, processes each with Mistral OCR,
    and returns a single string containing concatenated markdown from all PDFs,
    wrapped between START/END markers per file.
    """
    client = Mistral(api_key=api_key)
    base_path = Path(directory)
    sections = []

    for pdf_file in base_path.glob("*.pdf"):  # discover PDFs 
        # Upload for OCR
        uploaded = client.files.upload(
            file={"file_name": pdf_file.stem, "content": pdf_file.read_bytes()},
            purpose="ocr"
        )
        signed = client.files.get_signed_url(file_id=uploaded.id, expiry=expiry)
        response = client.ocr.process(
            document=DocumentURLChunk(document_url=signed.url),
            model=ocr_model,
            include_image_base64=False  # focus on markdown
        )
        data = json.loads(response.model_dump_json())  # parse JSON 

        # Build markdown block
        md_content = "\n".join(page["markdown"] for page in data.get("pages", []))
        sections.append(
            f"START OF {pdf_file.name}\n{md_content}\nEND OF {pdf_file.name}"
        )

    # Concatenate all documents with blank lines in between :contentReference[oaicite:3]{index=3}
    return "\n\n".join(sections)


def get_resume_info_from_gdrive(
    folder_url: str,
    output_dir: str = "output",
    api_key: str = "edytn5mDI26B5eaqqM83ildOZDvVvTEG"):
    download_drive_folder_gdown(
        folder_url=folder_url,
        output_dir=output_dir
    )
    
    response = concatenate_pdf_markdowns(
        directory=output_dir,
        api_key=api_key
    )
    
    print(response)
    return response 





"""
response = get_resume_info_from_gdrive(
    folder_url="https://drive.google.com/drive/folders/1nrjOcMh0K-F6D5o3WBVxdmC4_Jh33bBd?usp=sharing",
    output_dir="output",
    api_key= "edytn5mDI26B5eaqqM83ildOZDvVvTEG"

"""