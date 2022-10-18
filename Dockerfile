FROM python:3.8

WORKDIR /devops-dtl-app

RUN apt-get update

RUN apt install -y libgl1-mesa-glx

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./model ./model

EXPOSE 5000

CMD ["python", "./app/main.py"]