FROM python:3.12
WORKDIR /app

RUN pip install nicegui
RUN pip install pymongo

COPY src ./app/src
EXPOSE 8080

RUN useradd app
USER app

ARG data_path

CMD python /app/src/main.py $data_path