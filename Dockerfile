FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y chromium
COPY . .
EXPOSE 5001
CMD [ "python", "./my_flask.py" ]
