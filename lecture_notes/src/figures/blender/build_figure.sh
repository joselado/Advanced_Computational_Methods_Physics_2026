#!/bin/sh
# Turn a final render into the figure PDF of the notes:
#   ./build_figure.sh <name> <session folder>
# flattens out/<name>.png onto white as out/<name>.jpg, compiles ../src/<name>.tex (the TikZ
# overlay with the labels) and writes the compressed PDF to ../<session folder>/<name>.pdf.
set -e
cd "$(dirname "$0")"
python3 -c "
from PIL import Image
im = Image.open('out/$1.png'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
bg.alpha_composite(im); bg.convert('RGB').save('out/$1.jpg', quality=90)"
cd ../src
pdflatex -interaction=batchmode "$1.tex" > /dev/null
mkdir -p "../$2"
ps2pdf -dPDFSETTINGS=/printer "$1.pdf" "../$2/$1.pdf"
rm -f "$1.aux" "$1.log" "$1.pdf"
ls -la "../$2/$1.pdf"
