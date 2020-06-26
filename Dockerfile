FROM python:3.7-alpine

WORKDIR /app
COPY . .
RUN ln -s /app/search.py /usr/bin/search

CMD ["sh"]