FROM python:3.7-alpine

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "/app/search.py" ]