FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        netcat && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY items_parser/wait-for-it.sh market_csgo_link_parser/requirements.txt /app/
RUN chmod +x /app/wait-for-it.sh
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["./wait-for-it.sh", "-t", "20", "seleniarm-hub:4444", "--", "./wait-for-it.sh", "-t", "20", "db:5432", "--", "python3", "/app/parser.py"]
