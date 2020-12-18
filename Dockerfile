FROM python:3.9-alpine
LABEL author="Da Yang" email="dayang.phd@gmail.com"
LABEL version="0.1"

# Setting up Docker environment
WORKDIR /code
# Export env variables.
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000
###

#Run and install flask modules in container
RUN pip3 install flask

#Copy current directory files to containers code directory
COPY . .

EXPOSE 5000
#RUN app.
CMD flask run --host 0.0.0.0
