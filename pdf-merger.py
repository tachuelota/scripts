import argparse
from PyPDF2 import PdfMerger

parser = argparse.ArgumentParser()
parser.add_argument("files", help="files to merge", nargs='+', default=[])
args = parser.parse_args()

merger = PdfMerger()

for pdf in args.files:
    merger.append(pdf)

merger.write("merged-pdf.pdf")
merger.close()