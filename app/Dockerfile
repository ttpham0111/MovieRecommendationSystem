FROM alpine

MAINTAINER Tuan Pham <ttpham0111@gmail.com>

# Install python and pip
RUN apk add --no-cache curl \
                       musl-dev \
                       gcc \
                       libffi-dev \
                       python-dev==2.7.13-r0 && \
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && \
    python get-pip.py && \
    rm -f get-pip.py

# Install gunicorn and gevent
RUN pip install gunicorn \
                gevent==1.2.1

# Install requires first for better caching
COPY requirements.txt /app/requirements.txt

# Linking xlocale fixes a bug with installing numpy in alpine image
# scikit-surprise forces numpy to be installed before trying to run its setup.py
RUN ln -s locale.h /usr/include/xlocale.h && \
    pip install -r /app/requirements.txt && \
    pip install scikit-surprise

# Install app
COPY . /app
RUN pip install /app

# Environmental variables set by Heroku
ENV SECRET_KEY $SECRET_KEY

# Run app
CMD gunicorn --bind=0.0.0.0:$PORT \
             --access-logfile=- \
             --access-logformat="%(t)s %(r)s %(s)s" \
             --workers=1 \
             --worker-class='gevent' \
             --timeout=600 \
             server:app