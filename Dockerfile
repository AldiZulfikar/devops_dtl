FROM python:3.8

WORKDIR /devops-dtl-app

RUN apt-get update

RUN apt install -y libgl1-mesa-glx

ENV STATIC_URL /static

ENV STATIC_PATH /devops-dtl-app/app/static

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

RUN rm /devops-dtl-app/app/torch_utils.py

COPY torch_utils.py /devops-dtl-app/app/torch_utils.py

EXPOSE 5000

CMD ["python", "./app/main.py"]