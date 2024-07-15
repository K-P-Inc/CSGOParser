FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

COPY market_csgo_parser/ /app/market_csgo_parser/
COPY conf/ /app/conf/
COPY classes/ /app/classes/
COPY utils/ /app/utils/
COPY scripts/wait-for-it.sh /app/wait-for-it.sh
COPY requirements.txt /app/

# Install dependencies
RUN chmod +x /app/wait-for-it.sh
RUN pip install -r requirements.txt

ENV DOCKER_RUN "a"
ENTRYPOINT ["./wait-for-it.sh", "-t", "20", "seleniarm-hub:4444", "--", "./wait-for-it.sh", "-t", "20", "db:5432", "--", "python3", "-m", "market_csgo_parser.parser"]