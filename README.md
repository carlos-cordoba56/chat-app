for production
docker image build -t chat-app .
docker container run -it --rm -p 80:8080 chat-app

for development
docker image build -t chat-app -f Dockerfile.dev .
docker container run --net application-connection -it --rm -p 80:8080 -v ${pwd}:/chat-app chat-app

docker run --name postgresql -e POSTGRES_USER=myusername -e POSTGRES_PASSWORD=mypassword --net application-connection -it --rm -p 5432:5432 postgres


docker network create application-connection