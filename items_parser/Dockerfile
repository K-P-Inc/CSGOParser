FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        netcat && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY items_parser/parser.py items_parser/skins.json items_parser/wait-for-it.sh ./

RUN pip install requests pg8000 python-dotenv wait-for-it
RUN chmod +x wait-for-it.sh

CMD ["python", "parser.py"]
