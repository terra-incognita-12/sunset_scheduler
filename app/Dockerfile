FROM python:3.10-alpine

WORKDIR /src/app/

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /src/app/entrypoint.sh

ENTRYPOINT ["/src/app/entrypoint.sh"]