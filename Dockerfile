FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
	libreoffice \
	libreoffice-writer \
	fonts-dejavu \
	fonts-liberation \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /code

RUN pip install --no-cache-dir fastapi uvicorn python-multipart

COPY . .

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
