FROM python:3.8-alpine

RUN adduser -D mypass

WORKDIR /home/mypass/

COPY requirements.txt requirements.txt

RUN python -m venv venv 
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY ./ ./ 
RUN chmod +x boot.sh

RUN chown -R mypass:mypass ./
USER mypass

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]