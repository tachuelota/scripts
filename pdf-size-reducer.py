import argparse
from PyPDF2 import PdfReader, PdfWriter

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to reduce size")
parser.add_argument("output", help="output file")
parser.add_argument("--remove-images", help="removes images from the file", action="store_true")
parser.add_argument("--compress", help="compresses the file", action="store_true")
args = parser.parse_args()

reader = PdfReader(args.file)
writer = PdfWriter()

for page in reader.pages:
    if(args.compress):
        page.compress_content_streams()
    writer.add_page(page)

writer.add_metadata(reader.metadata)

if(args.remove_images):
    writer.remove_images()

with open(args.output, "wb") as fp:
    writer.write(fp)