FROM python:3.11

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

#Env Variables
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

#Run the app
CMD ["flask", "run", "--host=0.0.0.0"]