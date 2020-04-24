FROM python:3.6
ADD . /aplication
WORKDIR /aplication
RUN pip install -r requirements.txt
CMD python run.py