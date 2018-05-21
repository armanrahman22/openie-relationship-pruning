FROM python:3.6

RUN pip3 install --no-cache-dir numpy==1.14.2 nltk==3.1 \
  && python3 -c "import nltk; nltk.download('stopwords')"

ADD requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

ADD src /app/src

WORKDIR /app/src

ENV SANIC_WORKERS="1"
ENV TIMEOUT="3600"
ENV MIN_ENTITY_LENGTH="2"
ENV MATCH_RATIO="75"

EXPOSE 8000
CMD python3 -m sanic server.app --host=0.0.0.0 --workers=${SANIC_WORKERS}
