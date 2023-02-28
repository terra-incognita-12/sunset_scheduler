FROM python:3.10-alpine

WORKDIR /src/app/

COPY . .

RUN pip install -r requirements.txt
RUN chmod +x /src/app/entrypoint.sh

ENTRYPOINT ["/src/app/entrypoint.sh"]