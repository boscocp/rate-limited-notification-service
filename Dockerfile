FROM python:3.12

ENV PYTHONPATH=/

WORKDIR /app

COPY src/db/db.py /src/db/
COPY src/db/generate_table.py /src/db/
COPY src/main.py .
COPY src/router_users.py /src/
COPY src/domain.py /src/
COPY src/repositories.py /src/

COPY requirements.txt .

RUN pip install -r requirements.txt

USER nobody

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]