FROM python:3.6
ADD . /aplication
WORKDIR /aplication
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python run.py