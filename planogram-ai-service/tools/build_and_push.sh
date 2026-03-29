set -e
echo 'Building image...'
docker-compose build
set +e
echo 'Stopping "test" container...'
docker stop test
docker container rm test
set -e
echo 'Starting "test" container...'
docker run --gpus all -p 127.0.0.1:7559:7552/tcp\
 --name test\
 --restart on-failure -d\
 registry.aif.nordasys.net/aif/planogram_ai_service:lastest
sleep 5s
echo 'Running tests...'
python3 ${HOME}/repos/planogram-ai-service/test/test_api.py 127.0.0.1:7559
echo 'Stopping "test" container...'
docker stop test
docker container rm test
echo 'Pushing to registry...'
docker login --username aifregistry https://registry.aif.nordasys.net
docker push registry.aif.nordasys.net/aif/planogram_ai_service:lastest
echo "Image succesfully uploaded"
