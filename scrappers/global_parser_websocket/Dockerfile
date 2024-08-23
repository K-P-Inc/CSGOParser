FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

COPY global_parser_websocket/ /app/global_parser_websocket/
COPY conf/ /app/conf/
COPY classes/ /app/classes/
COPY utils/ /app/utils/
COPY scripts/wait-for-it.sh /app/wait-for-it.sh
COPY requirements.txt /app/
COPY data/stickers_content.json /app/data/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Install dependencies
RUN chmod +x /app/wait-for-it.sh
RUN pip install -r requirements.txt

ENV DOCKER_RUN "a"
ENTRYPOINT ["python3", "-m", "global_parser_websocket.parser"]
