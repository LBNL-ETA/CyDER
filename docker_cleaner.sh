# Note this come from http://blog.yohanliyanage.com/2015/05/docker-clean-up-after-yourself/
# Note this will throw an error if nothing need to be removed
# Remove all docker that are not running anymore
docker rm -v $(docker ps -a -q -f status=exited)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes that are not in use
docker volume rm $(docker volume ls -qf dangling=true)
