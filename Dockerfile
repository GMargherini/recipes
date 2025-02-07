FROM python:3.12
WORKDIR .

RUN pip install nicegui

COPY src ./src
EXPOSE 8080

RUN useradd app
USER app

ARG data_path

CMD ["python", "src/main.py", data_path]