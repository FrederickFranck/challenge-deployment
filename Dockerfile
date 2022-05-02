FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python-is-python3 build-essential
COPY ./project /project
WORKDIR /project
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]