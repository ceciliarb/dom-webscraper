FROM python:3

RUN apt update && \
    apt install -y libreoffice ghostscript wkhtmltopdf php && \
    pip install requests beautifulsoup4 html5lib

WORKDIR home

COPY . .