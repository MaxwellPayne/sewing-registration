FROM python:3.12.4

# please review all the latest versions here:
# https://googlechromelabs.github.io/chrome-for-testing/
ENV CHROMEDRIVER_VERSION=126.0.6478.182

# install chrome
RUN apt-get update && apt-get install -y wget && apt-get install -y zip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# install chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip && rm -dfr chromedriver_linux64.zip \
  && mv /chromedriver-linux64/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver

WORKDIR /usr/src/app

RUN pip install poetry==1.8.3

# install package dependencies
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY main.py .
COPY app ./app

CMD poetry run python main.py
