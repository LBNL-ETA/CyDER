# stop all containers
docker-compose stop

# Remove all containers
docker rm -v $(docker ps -a -q)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)
