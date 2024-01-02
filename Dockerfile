FROM python:3.11.4-slim as base_build

WORKDIR /app
RUN mkdir bucket

#################################################
# Set environnement variable
#################################################
ENV DEBIAN_FRONTEND noninteractive

#################################################
# Install updates
#################################################
RUN apt-get update -y

FROM base_build as install_packages
#################################################
# install python packages
#################################################
COPY requirements.txt .
COPY main.py .

RUN pip install -r requirements.txt

#################################################
# Install ffmpeg
#################################################
RUN apt-get install -y --no-install-recommends ffmpeg

CMD [ "python", "main.py" ]
