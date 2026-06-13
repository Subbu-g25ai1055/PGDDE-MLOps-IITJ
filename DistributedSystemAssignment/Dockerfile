FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app

RUN apt-get update && apt-get install -y \
    iputils-ping \
    net-tools \
    curl

CMD ["python3", "node.py"]
