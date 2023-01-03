FROM python:3.10
ENV PYTHONDONTWRITEBYRECODE 1
ENV PYTHONDONTBUFFERED 1

WORKDIR code/

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .


ENTRYPOINT ["/code/entrypoint.sh"]