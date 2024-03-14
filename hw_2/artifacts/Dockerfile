FROM texlive/texlive:latest

WORKDIR /data

COPY ./*.tex ./
COPY ./*.jpg ./

CMD pdflatex -shell-escape hw_2_2.tex 