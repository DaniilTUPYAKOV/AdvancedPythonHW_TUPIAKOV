FROM pandoc/latex:latest

WORKDIR /data

COPY artifacts/test_image.jpg /data/
COPY artifacts/hw_2_2.tex /data/

RUN pandoc hw_2_2.tex --pdf-engine=lualatex -o hw_2_2.pdf
