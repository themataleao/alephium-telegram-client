FROM python:3

WORKDIR /usr/src/app

ARG GITLAB_PWD
ARG GITLAB_USR

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python","-u", "scheduler.py" ]
