# pull official base image
FROM python:3.8.0-alpine

# set work directory
RUN mkdir /app
COPY . /app
WORKDIR /app

# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt app/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]

EXPOSE 5000