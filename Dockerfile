ARG PORT=443
FROM cypress/browsers:latest
WORKDIR /app
RUN apt-get install python3 -y && apt-get install chromium-browser -y
COPY ./requirements.txt /app
RUN apt-get update && apt-get install -y python3-pip && pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=my_flask.py
CMD ["flask", "run", "--host", "0.0.0.0"]





