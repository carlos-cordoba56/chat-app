for production
docker image build -t chat-app .
docker container run -it --rm -p 80:8080 chat-app

for development
docker image build -t chat-app -f Dockerfile.dev .
docker container run -it --rm -p 80:8080 -v ${pwd}:/chat-app chat-app
