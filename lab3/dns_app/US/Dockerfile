FROM python:3.12-rc-bullseye

# Set up a working folder and install the pre-reqs
RUN mkdir -p /home/app

RUN pip install --upgrade pip
RUN pip install Flask
RUN pip install requests

COPY . /home/app

CMD [ "python", "./home/app/us.py" ]
