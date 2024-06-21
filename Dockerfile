FROM ubuntu:22.04

# Update and upgrade OS
RUN apt-get autoremove && apt autoclean -y
RUN apt-get update
RUN apt-get update --fix-missing
RUN apt-get install -y software-properties-common
RUN apt-get upgrade -y

# Install required ubuntu packages
RUN DEBIAN_FRONTEND="noninteractive" TZ="Asia/Kolkata" apt-get -y install tzdata
RUN apt-get install -y vim curl git net-tools nginx wget curl
RUN apt-get install -y libcurl4-openssl-dev libmysqlclient-dev build-essential libssl-dev

# Setup python and pip
RUN apt-get install -y python3.10 python3.10-dev python3.10-venv
RUN apt-get install -y python3-pip
RUN ln -svf /usr/bin/python3 /usr/bin/python
RUN pip install pip --upgrade

# Setup the project requirements
RUN pip install setuptools==57.5.0
RUN pip install newrelic
COPY nykaa-catalog/requirements.txt /var/www/app/
RUN pip install -r /var/www/app/requirements.txt
RUN pip install --no-cache-dir --compile --install-option="--with-openssl" pycurl

# Copy code
WORKDIR /var/www/app/
RUN mkdir catalog_uploads
RUN mkdir -p edna_feed
COPY nykaa-catalog/catalog-backend/config ./config
COPY config-files/config.json ./config/config.json
COPY nykaa-catalog/catalog-backend/run.py .
COPY nykaa-catalog/catalog-backend/src ./src
COPY nykaa-catalog/catalog-job/startup.sh .


CMD ["bash", "/var/www/app/startup.sh"]
