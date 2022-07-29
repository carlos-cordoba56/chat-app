FROM python:3.9

WORKDIR /chat-app

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1


# Copy the dependencies
COPY ./requirements.txt ./requirements.txt
COPY ./requirements-dev.txt ./requirements-dev.txt

# install packages
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements-dev.txt

# Define environment variables
ENV APP_NAME "super-app"

COPY ./ ./app
