#!/usr/bin/env python3

from pdf2docx import Converter
from docxcompose.composer import Composer
from docx import Document as Document_compose
import PyPDF2
import os
import sys

if(len(sys.argv) != 3):
    exit(1)

pdf_file = sys.argv[1]
docx_file = sys.argv[2]

def main():
    files_to_merge = list()

    # Open the original PDF
    inputpdf = PyPDF2.PdfFileReader(open(pdf_file, "rb"))

    def combine_all_docx(filename_master, files_list):
        number_of_sections=len(files_list)
        master = Document_compose(filename_master)
        composer = Composer(master)
        for i in range(0, number_of_sections):
            doc_temp = Document_compose(files_list[i])
            composer.append(doc_temp)
        composer.save(docx_file)

    # Iterate through the pages
    for i in range(inputpdf.numPages):
        # Create a PDF writer object for the output PDF
        output = PyPDF2.PdfFileWriter()
        # Copy the i-th page of the original PDF to the output
        output.addPage(inputpdf.getPage(i))
        # Write the output PDF
        with open("page_" + str(i) + ".pdf", "wb") as outputStream:
            output.write(outputStream)
        cv = Converter("page_" + str(i) + ".pdf")
        cv.convert("page_" + str(i) + ".docx")
        cv.close()
        files_to_merge.append(f"page_{str(i)}.docx")

    combine_all_docx(files_to_merge[0], files_to_merge[1:])

    for i, file in enumerate(files_to_merge):
        os.remove(file)
        os.remove("page_" + str(i) + ".pdf")

if __name__ == "__main__":
    sys.exit(main())