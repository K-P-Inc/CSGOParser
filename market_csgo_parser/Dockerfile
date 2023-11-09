##################################
### Set the Pytest environment ###
##################################
FROM python:3.9.0-alpine

# Set the working directory
WORKDIR /app/

# Install dependencies
COPY items_parser/wait-for-it.sh market_csgo_parser/requirements.txt /app/
RUN chmod +x /app/wait-for-it.sh
RUN pip install -r requirements.txt

# Install additional requirements
RUN apk add bash
RUN apk add tk

ENTRYPOINT ["./wait-for-it.sh", "-t", "20", "seleniarm-hub:4444", "--", "./wait-for-it.sh", "-t", "20", "db:5432", "--", "python3", "/app/parser.py"]
