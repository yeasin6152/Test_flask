FROM ubuntu 

RUN apt-get update 
RUN apt-get install python3-pip -y
RUN pip install Flask
RUN pip install selenium==4.9.1 
ADD my_flask.py /
WORKDIR /

EXPOSE 5000

CMD [“python3”,”my_flask.py”]




