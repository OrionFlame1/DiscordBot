# Use an official Python runtime as a base image
FROM python:3.12.0-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app/
COPY requirements.txt ./

# Install the dependencies specified in requirements.txt
RUN apt-get update -y
RUN pip install --no-cache-dir -r requirements.txt

# Broken selenium package installation
RUN pip install selenium --user

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Chromedriver install
RUN apt-get update -y
RUN apt-get install -y wget gnupg unzip curl

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update -y && apt-get install --fix-missing
RUN apt-get install -y google-chrome-stable --fix-missing
RUN apt-get install libxi6 libgconf-2-4 -y

ENV CHROMEDRIVER_VERSION 100.0.4896.20
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir -p $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d .

# Run the bot
CMD ["python", "main.py"]
