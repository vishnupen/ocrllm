FROM python:3.8-slim-buster


# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN mkdir -p /usr/share/man/man1


RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libc-dev python3-dev openjdk-11-jre-headless libreoffice ghostscript curl

RUN pip install --upgrade pip
RUN pip install torch==1.11.0+cpu torchvision==0.12.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

WORKDIR /app

RUN apt-get install poppler-utils
RUN apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
RUN apt-get install -y --reinstall build-essential
RUN CPPFLAGS=-I/usr/local/include pip install tesserocr

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

# RUN apt-get install poppler-utils
# RUN apt-get install -y tesseract-ocr  

RUN apt-get install -y wget

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python" ]

CMD ["app.py" ]

EXPOSE 5003
