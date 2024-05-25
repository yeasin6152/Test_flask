FROM ubuntu 

RUN apt-get update 
RUN apt-get install python3-pip
RUN apt-get install flask
RUN pip3 install selenium==4.9.1
ADD my_flask.py /
WORKDIR /

EXPOSE 5000

CMD [“python3”,”my_flask.py”]




