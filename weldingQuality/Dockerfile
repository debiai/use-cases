FROM python:3.12-slim

WORKDIR /app

COPY requirements_deploy.txt requirements.txt
COPY data_provider.py data_provider.py
COPY metadata/ds_meta.parquet metadata/ds_meta.parquet

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "data_provider.py"]
