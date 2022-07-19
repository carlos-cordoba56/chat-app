FROM python:3.9

WORKDIR /chat-app

# Copy the dependencies
COPY ./requirements.txt ./app/requirements.txt

# install packages
RUN pip install --no-cache-dir --upgrade -r ./app/requirements.txt

# Define environment variables
ENV APP_NAME "super-app"

COPY ./app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]