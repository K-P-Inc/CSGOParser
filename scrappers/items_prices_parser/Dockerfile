FROM python:3.10-slim-buster

WORKDIR /app

COPY items_prices_parser/ /app/items_prices_parser/
COPY data/ /app/data/
COPY conf/ /app/conf/
COPY classes/ /app/classes/
COPY utils/ /app/utils/
COPY requirements.txt /app/
COPY scripts/wait-for-it.sh /app/wait-for-it.sh

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Install dependencies
RUN chmod +x /app/wait-for-it.sh
RUN pip install -r requirements.txt

ENV DOCKER_RUN "a"

CMD ["sh", "-c", "while :; do python -m items_prices_parser.steamwebapi; sleep 10800; done"]
