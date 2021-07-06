FROM python

WORKDIR /usr/src/app

RUN apt update && \
    apt install -y ghostscript libreoffice

# && \
#    pip install beautifulsoup4

COPY . .

#CMD python ./main.py input --no-clear
