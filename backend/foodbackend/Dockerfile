FROM python:3.9.5-slim

WORKDIR /foodbackend_build

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . ./

CMD ["gunicorn","foodbackend.wsgi:application","--bind","0:8000"]
