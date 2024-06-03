FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

COPY template_parser_api/ /app/template_parser_api/
COPY conf/ /app/conf/
COPY classes/ /app/classes/
COPY utils/ /app/utils/
COPY scripts/wait-for-it.sh /app/wait-for-it.sh
COPY requirements.txt /app/

# Install dependencies
RUN chmod +x /app/wait-for-it.sh
RUN pip install -r requirements.txt

ENTRYPOINT ["./wait-for-it.sh", "-t", "20", "db:5432", "--", "python3", "-m", "template_parser_api.parser"]