FROM python:3.10.2

WORKDIR /app

COPY app/requirements.txt .

RUN mkdir -p /app/app/output

RUN pip install --no-cache-dir --upgrade pip setuptools

RUN pip install --no-cache-dir -r requirements.txt

COPY  . .

CMD [ "python", "app/app.py" ]