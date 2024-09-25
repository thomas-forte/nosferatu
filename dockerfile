FROM python:3-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update \
    && apk upgrade\
    && apk add --update --no-cache gcc musl-dev

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install build

COPY . .

RUN python -m build --wheel

RUN ls dist/*.whl

FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY --from=builder /app/dist/*.whl .
RUN pip install *.whl

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "nosferatu:create_app()"]