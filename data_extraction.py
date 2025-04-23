import os
import glob
from langchain_community.document_loaders import PyPDFLoader

def load_pdfs_from_folder(folder_path: str) -> dict:
  """Load all PDFs from a given folder and its subfolders, and store them in a dictionary.

  Args:
    folder_path: The path to the folder containing subfolders with PDF files.

  Returns:
    A dictionary with the subfolder names as keys and the content of all PDFs in each subfolder as values.
  """
  folder_dict = {}
  j=1
  for subfolder in os.listdir(folder_path):
    subfolder_path = os.path.join(folder_path, subfolder)
    if os.path.isdir(subfolder_path):
      pdf_files = glob.glob(os.path.join(subfolder_path, "*.pdf"))
      documents = []
      print(j, " ", subfolder)
      i = 1
      j+=1
      for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        print("  ",i, ".  ", pdf_file)
        documents.extend(loader.load())
        i += 1
      folder_dict[subfolder] = documents
  return folder_dict

folder_path = "/home/vaibhavksir01/Downloads/project/Knowledge Graph/Class 6 textbooks"
raw_document = load_pdfs_from_folder(folder_path)