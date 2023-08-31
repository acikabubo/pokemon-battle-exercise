FROM python:3.11
WORKDIR /project
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
WORKDIR /project
