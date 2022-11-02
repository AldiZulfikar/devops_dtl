FROM python:3.8-slim-buster

WORKDIR /devops-dtl-app

# RUN apt-get update

# RUN apt install -y libgl1-mesa-glx

ENV STATIC_URL /static

ENV STATIC_PATH /devops-dtl-app/app/static

COPY requirements.txt .

RUN pip3install -r requirements.txt

COPY ./app ./app
COPY ./model ./model

EXPOSE 5000

# CMD ["python", "./app/main.py"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]