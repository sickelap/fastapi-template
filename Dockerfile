FROM python:3.13-alpine

WORKDIR /app
ENV PATH=/py/bin:/bin:/usr/bin:/usr/local/bin

COPY . .

RUN python -m venv /py
RUN /py/bin/pip install -r requirements.txt

CMD ["/py/bin/python", "server.py", "prod"]
