FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        netcat && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY items_prices_parser/ /app/items_prices_parser/
COPY data/ /app/data/
COPY conf/ /app/conf/
COPY classes/ /app/classes/
COPY utils/ /app/utils/
COPY requirements.txt /app/
COPY scripts/wait-for-it.sh /app/wait-for-it.sh

# Install dependencies
RUN chmod +x /app/wait-for-it.sh
RUN pip install -r requirements.txt

CMD ["./wait-for-it.sh", "-t", "20", "seleniarm-hub:4444", "--", "sh", "-c", "while :; do python -m items_prices_parser.parser; sleep 600; done"]
