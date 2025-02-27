FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/manage.py

EXPOSE 8000

CMD ["sh", "-c", "cd /app && python manage.py runserver 0.0.0.0:8000"]
