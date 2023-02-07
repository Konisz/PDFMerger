import tkinter as tk
import tkinter.font as font
import zipfile
import os
import glob
import datetime
from PyPDF2 import PdfMerger

def extract_and_delete_zip(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_file))
    os.remove(zip_file)

def merge_pdfs(pdf_files, output_file):
    merger = PdfMerger()
    for pdf in pdf_files:
        with open(pdf, 'rb') as file:
            merger.append(file)
    with open(output_file, 'wb') as file:
        merger.write(file)

def process_zip_files():
    zip_files = glob.glob('*.zip')

    for zip_file in zip_files:
        extract_and_delete_zip(zip_file)

        pdf_files = glob.glob('*.pdf')
        pdf_files.sort()

        current_date = datetime.datetime.now()
        month = f'{current_date.month:02d}'
        merged_pdf_folder = 'merged'
        if not os.path.exists(merged_pdf_folder):
            os.makedirs(merged_pdf_folder)
        merged_pdf = os.path.join(merged_pdf_folder, os.path.splitext(zip_file)[0] + f'_{month}_{current_date.year}.pdf')
        merge_pdfs(pdf_files, merged_pdf)

        for pdf in pdf_files:
            if pdf != merged_pdf:
                os.remove(pdf)

root = tk.Tk()
root.title("PDF Merger")
root.geometry("200x200")

frame = tk.Frame(root)
frame.pack()

myFont = font.Font(family='Helvetica', size=15, weight='bold')

button = tk.Button(frame,
                   text="Merge PDF Files",
                   command=process_zip_files,
                   height=50, width=50,
                   bg='#0052cc', fg='#ffffff')

button['font'] = myFont
button.pack()

root.mainloop()
