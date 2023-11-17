FROM python:3.11-slim as build

WORKDIR /usr/app

RUN python3 -m venv venv

ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

FROM python:3.11-slim

WORKDIR /usr/app

COPY --from=build /usr/app/venv ./venv

ENV PATH="/usr/app/venv/bin:$PATH"

COPY . .

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
