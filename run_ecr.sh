## copy three ecr commands here after you create an ecr repodc ros-humble-greengrass-minipupper-v2
#ECR_COMMANDS=""

# docker save ros-humble-greengrass-minipupper-v2:latest | gzip > minipupper_latest.tar.gz
wget https://github.com/lbaitemple/mini-pupper-aws/releases/download/v1.0.0/minipupper_latest.tar.gz
docker load < ./minipupper_latest.tar.gz
