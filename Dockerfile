FROM python:latest

WORKDIR /mybot

COPY . .

RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD ["python", "main.py"]